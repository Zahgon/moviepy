from dataclasses import dataclass

from moviepy.Clip import Clip
from moviepy.Effect import Effect
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx.Crop import Crop


@dataclass
class FreezeRegion(Effect):
    """Freezes one region of the clip while the rest remains animated.

    You can choose one of three methods by providing either `region`,
    `outside_region`, or `mask`.

    Parameters
    ----------

    t
      Time at which to freeze the freezed region.

    region
      A tuple (x1, y1, x2, y2) defining the region of the screen (in pixels)
      which will be freezed. You can provide outside_region or mask instead.

    outside_region
      A tuple (x1, y1, x2, y2) defining the region of the screen (in pixels)
      which will be the only non-freezed region.

    mask
      If not None, will overlay a freezed version of the clip on the current clip,
      with the provided mask. In other words, the "visible" pixels in the mask
      indicate the freezed region in the final picture.

    """

    t: float = 0
    region: tuple = None
    outside_region: tuple = None
    mask: Clip = None

    def apply(self, clip: Clip) -> Clip:
        """Apply the effect to the clip."""
        pass
