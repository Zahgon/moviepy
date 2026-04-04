from dataclasses import dataclass

import numpy as np

from moviepy.Effect import Effect


@dataclass
class BlackAndWhite(Effect):
    """Desaturates the picture, makes it black and white.
    Parameter RGB allows to set weights for the different color
    channels.
    If RBG is 'CRT_phosphor' a special set of values is used.
    preserve_luminosity maintains the sum of RGB to 1.
    """

    RGB: str = None
    preserve_luminosity: bool = True

    def apply(self, clip):
        """Apply the effect to the clip."""
        pass
