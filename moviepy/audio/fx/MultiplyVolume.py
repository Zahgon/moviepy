from dataclasses import dataclass

import numpy as np

from moviepy.Clip import Clip
from moviepy.decorators import audio_video_effect
from moviepy.Effect import Effect
from moviepy.tools import convert_to_seconds


@dataclass
class MultiplyVolume(Effect):
    """Returns a clip with audio volume multiplied by the
    value `factor`. Can be applied to both audio and video clips.

    Parameters
    ----------

    factor : float
      Volume multiplication factor.

    start_time : float, optional
      Time from the beginning of the clip until the volume transformation
      begins to take effect, in seconds. By default at the beginning.

    end_time : float, optional
      Time from the beginning of the clip until the volume transformation
      ends to take effect, in seconds. By default at the end.

    Examples
    --------

    .. code:: python

        from moviepy import AudioFileClip

        music = AudioFileClip("music.ogg")
        # doubles audio volume
        doubled_audio_clip = music.with_effects([afx.MultiplyVolume(2)])
        # halves audio volume
        half_audio_clip = music.with_effects([afx.MultiplyVolume(0.5)])
        # silences clip during one second at third
        effect = afx.MultiplyVolume(0, start_time=2, end_time=3)
        silenced_clip = clip.with_effects([effect])
    """

    factor: float
    start_time: float = None
    end_time: float = None

    def __post_init__(self):
        if self.start_time is not None:
            self.start_time = convert_to_seconds(self.start_time)

        if self.end_time is not None:
            self.end_time = convert_to_seconds(self.end_time)

    def _multiply_volume_in_range(self, factor, start_time, end_time, nchannels):
        pass

    @audio_video_effect
    def apply(self, clip: Clip) -> Clip:
        """Apply the effect to the clip."""
        pass
