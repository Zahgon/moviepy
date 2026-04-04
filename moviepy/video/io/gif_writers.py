"""MoviePy video GIFs writing."""

import imageio.v3 as iio
import proglog

from moviepy.decorators import requires_duration, use_clip_fps_by_default


@requires_duration
@use_clip_fps_by_default
def write_gif_with_imageio(clip, filename, fps=None, loop=0, logger="bar"):
    """Writes the gif with the Python library ImageIO (calls FreeImage)."""
    pass
