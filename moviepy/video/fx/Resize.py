import numbers
from dataclasses import dataclass
from typing import Union

import numpy as np
from PIL import Image

from moviepy.Effect import Effect


@dataclass
class Resize(Effect):
    """Effect returning a video clip that is a resized version of the clip.

    Parameters
    ----------

    new_size : tuple or float or function, optional
        Can be either
        - ``(width, height)`` in pixels or a float representing
        - A scaling factor, like ``0.5``.
        - A function of time returning one of these.

    height : int, optional
        Height of the new clip in pixels. The width is then computed so
        that the width/height ratio is conserved.

    width : int, optional
        Width of the new clip in pixels. The height is then computed so
        that the width/height ratio is conserved.

    Examples
    --------

    .. code:: python

        clip.with_effects([vfx.Resize((460,720))]) # New resolution: (460,720)
        clip.with_effects([vfx.Resize(0.6)]) # width and height multiplied by 0.6
        clip.with_effects([vfx.Resize(width=800)]) # height computed automatically.
        clip.with_effects([vfx.Resize(lambda t : 1+0.02*t)]) # slow clip swelling
    """

    new_size: Union[tuple, float, callable] = None
    height: int = None
    width: int = None
    apply_to_mask: bool = True

    def resizer(self, pic, new_size):
        """Resize the image using PIL."""
        pass

    def apply(self, clip):
        """Apply the effect to the clip."""
        pass
