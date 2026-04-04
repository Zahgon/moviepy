from dataclasses import dataclass

import numpy as np

from moviepy.Clip import Clip
from moviepy.Effect import Effect
from moviepy.video.VideoClip import ImageClip


@dataclass
class Margin(Effect):
    """Draws an external margin all around the frame.

    Parameters
    ----------

    margin_size : int, optional
      If not ``None``, then the new clip has a margin size of
      size ``margin_size`` in pixels on the left, right, top, and bottom.

    left : int, optional
      If ``margin_size=None``, margin size for the new clip in left direction.

    right : int, optional
      If ``margin_size=None``, margin size for the new clip in right direction.

    top : int, optional
      If ``margin_size=None``, margin size for the new clip in top direction.

    bottom : int, optional
      If ``margin_size=None``, margin size for the new clip in bottom direction.

    color : tuple, optional
      Color of the margin.

    opacity : float, optional
      Opacity of the margin. Setting this value to 0 yields transparent margins.
    """

    margin_size: int = None
    left: int = 0
    right: int = 0
    top: int = 0
    bottom: int = 0
    color: tuple = (0, 0, 0)
    opacity: float = 1.0

    def add_margin(self, clip: Clip):
        """Add margins to the clip."""
        pass

    def apply(self, clip: Clip) -> Clip:
        """Apply the effect to the clip."""
        pass
