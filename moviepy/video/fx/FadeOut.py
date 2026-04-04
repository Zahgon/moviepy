from dataclasses import dataclass

import numpy as np

from moviepy.Clip import Clip
from moviepy.Effect import Effect


@dataclass
class FadeOut(Effect):
    """Makes the clip progressively fade to some color (black by default),
    over ``duration`` seconds at the end of the clip. Can be used for masks too,
    where the final color must be a number between 0 and 1.

    For cross-fading (progressive appearance or disappearance of a clip over another
    clip), see ``CrossFadeOut``
    """

    duration: float
    final_color: list = None

    def apply(self, clip: Clip) -> Clip:
        """Apply the effect to the clip."""
        pass
