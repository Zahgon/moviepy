from dataclasses import dataclass

import numpy as np

from moviepy.Clip import Clip
from moviepy.decorators import audio_video_effect
from moviepy.Effect import Effect
from moviepy.tools import convert_to_seconds


@dataclass
class AudioFadeOut(Effect):
    """Return a sound clip where the sound fades out progressively
    over ``duration`` seconds at the end of the clip.

    Parameters
    ----------

    duration : float
      How long does it take for the sound to reach the zero level at the end
      of the clip.

    Examples
    --------

    .. code:: python

        clip = VideoFileClip("media/chaplin.mp4")
        clip.with_effects([afx.AudioFadeOut("00:00:06")])
    """

    duration: float

    def __post_init__(self):
        self.duration = convert_to_seconds(self.duration)

    def _mono_factor_getter(self, clip_duration):
        pass

    def _stereo_factor_getter(self, clip_duration, nchannels):
        pass

    @audio_video_effect
    def apply(self, clip: Clip) -> Clip:
        """Apply the effect to the clip."""
        pass
