import random
from pathlib import Path
from typing import Union, List

import torch

from ..core.transforms_interface import BaseWaveformTransform, EmptyPathException
from ..utils.dsp import calculate_rms
from ..utils.file import find_audio_files
from ..utils.io import Audio


class AddBackgroundNoise(BaseWaveformTransform):
    """
    Add background noise to the input audio.
    """

    # Note: This transform has only partial support for multichannel audio. Noises that are not
    # mono get mixed down to mono before they are added to all channels in the input.
    supports_multichannel = True
    requires_sample_rate = True

    def __init__(
        self,
        background_paths: Union[List[Path], List[str], Path, str],
        min_snr_in_db: float = 3.0,
        max_snr_in_db: float = 30.0,
        mode: str = "per_example",
        p: float = 0.5,
        p_mode: str = None,
        sample_rate: int = None,
    ):
        """

        :param background_paths: Either a path to a folder with audio files or a list of paths
            to audio files.
        :param min_snr_in_db: minimum SNR in dB.
        :param max_snr_in_db: maximium SNR in dB.
        :param mode:
        :param p:
        :param p_mode:
        """

        super().__init__(mode, p, p_mode, sample_rate)

        if isinstance(background_paths, (list, tuple, set)):
            # TODO: check that one can read audio files
            self.background_paths = list(background_paths)
        else:
            self.background_paths = find_audio_files(background_paths)

        if sample_rate is not None:
            self.audio = Audio(sample_rate=sample_rate, mono=True)

        if len(self.background_paths) == 0:
            raise EmptyPathException("There are no supported audio files found.")

        self.min_snr_in_db = min_snr_in_db
        self.max_snr_in_db = max_snr_in_db
        if self.min_snr_in_db > self.max_snr_in_db:
            raise ValueError("min_snr_in_db must not be greater than max_snr_in_db")

    def random_background(self, audio: Audio, target_num_samples: int) -> torch.Tensor:
        pieces = []

        # TODO: support repeat short samples instead of concatenating from different files

        missing_num_samples = target_num_samples
        while missing_num_samples > 0:
            background_path = random.choice(self.background_paths)
            background_num_samples = audio.get_num_samples(background_path)

            if background_num_samples > missing_num_samples:
                sample_offset = random.randint(
                    0, background_num_samples - missing_num_samples
                )
                num_samples = missing_num_samples
                background_samples = audio(
                    background_path, sample_offset=sample_offset, num_samples=num_samples
                )
                missing_num_samples = 0
            else:
                background_samples = audio(background_path)
                missing_num_samples -= background_num_samples

            pieces.append(background_samples)

        #  the inner call to rms_normalize ensures concatenated pieces share the same RMS (1)
        #  the outer call to rms_normalize ensures that the resulting background has an RMS of 1
        #  (this simplifies "apply_transform" logic)
        return audio.rms_normalize(
            torch.cat([audio.rms_normalize(piece) for piece in pieces], dim=1)
        )

    def randomize_parameters(
        self, selected_samples: torch.Tensor, sample_rate: int = None
    ):
        """

        :params selected_samples: (batch_size, num_channels, num_samples)
        """

        batch_size, _, num_samples = selected_samples.shape

        # (batch_size, num_samples) RMS-normalized background noise
        audio = self.audio if hasattr(self, "audio") else Audio(sample_rate, mono=True)
        self.transform_parameters["background"] = torch.stack(
            [self.random_background(audio, num_samples) for _ in range(batch_size)]
        )

        # (batch_size, ) SNRs
        snr_distribution = torch.distributions.Uniform(
            low=torch.tensor(
                self.min_snr_in_db, dtype=torch.float32, device=selected_samples.device
            ),
            high=torch.tensor(
                self.max_snr_in_db, dtype=torch.float32, device=selected_samples.device
            ),
            validate_args=True,
        )
        self.transform_parameters["snr_in_db"] = snr_distribution.sample(
            sample_shape=(batch_size,)
        )

    def apply_transform(self, selected_samples: torch.Tensor, sample_rate: int = None):
        batch_size, num_channels, num_samples = selected_samples.shape

        # (batch_size, num_samples)
        background = self.transform_parameters["background"].to(selected_samples.device)

        # (batch_size, num_channels)
        background_rms = calculate_rms(selected_samples) / (
            10 ** (self.transform_parameters["snr_in_db"].unsqueeze(dim=-1) / 20)
        )

        return selected_samples + background_rms.unsqueeze(-1) * background.view(
            batch_size, 1, num_samples
        ).expand(-1, num_channels, -1)
