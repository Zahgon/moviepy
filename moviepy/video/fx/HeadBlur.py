from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from moviepy.Clip import Clip
from moviepy.Effect import Effect


@dataclass
class HeadBlur(Effect):
    """Returns a filter that will blur a moving part (a head ?) of the frames.

    The position of the blur at time t is defined by (fx(t), fy(t)), the radius
    of the blurring by ``radius`` and the intensity of the blurring by ``intensity``.
    """

    fx: callable
    fy: callable
    radius: float
    intensity: float = None

    def apply(self, clip: Clip) -> Clip:
        """Apply the effect to the clip."""
        pass
