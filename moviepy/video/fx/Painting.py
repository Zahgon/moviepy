from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageFilter

from moviepy.Clip import Clip
from moviepy.Effect import Effect


@dataclass
class Painting(Effect):
    """Transforms any photo into some kind of painting.

    Transforms any photo into some kind of painting. Saturation
    tells at which point the colors of the result should be
    flashy. ``black`` gives the amount of black lines wanted.

    np_image : a numpy image
    """

    saturation: float = 1.4
    black: float = 0.006

    def to_painting(self, np_image, saturation=1.4, black=0.006):
        """Transforms any photo into some kind of painting.

        Transforms any photo into some kind of painting. Saturation
        tells at which point the colors of the result should be
        flashy. ``black`` gives the amount of black lines wanted.

        np_image : a numpy image
        """
        pass

    def apply(self, clip: Clip) -> Clip:
        """Apply the effect to the clip."""
        pass
