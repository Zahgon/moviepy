from dataclasses import dataclass

from moviepy.Clip import Clip
from moviepy.Effect import Effect
from moviepy.video.fx.FadeOut import FadeOut


@dataclass
class CrossFadeOut(Effect):
    """Makes the clip disappear progressively, over ``duration`` seconds.
    Only works when the clip is included in a CompositeVideoClip.
    """

    duration: float

    def apply(self, clip: Clip) -> Clip:
        """Apply the effect to the clip."""
        pass
