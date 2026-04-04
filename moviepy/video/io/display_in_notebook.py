"""Implements ``display_in_notebook``, a function to embed images/videos/audio in the
Jupyter Notebook.
"""

# Notes:
# All media are physically embedded in the Jupyter Notebook
# (instead of simple links to the original files)
# That is because most browsers use a cache system and they won't
# properly refresh the media when the original files are changed.

import inspect
import os
from base64 import b64encode

from moviepy.audio.AudioClip import AudioClip
from moviepy.tools import extensions_dict
from moviepy.video.io.ffmpeg_reader import ffmpeg_parse_infos
from moviepy.video.VideoClip import ImageClip, VideoClip


try:  # pragma: no cover
    from IPython.display import HTML

    ipython_available = True

    class HTML2(HTML):  # noqa D101
        def __add__(self, other):
            return HTML2(self.data + other.data)

except ImportError:

    def HTML2(content):  # noqa D103
        pass

    ipython_available = False


sorry = "Sorry, seems like your browser doesn't support HTML5 audio/video"
templates = {
    "audio": (
        "<audio controls>"
        "<source %(options)s  src='data:audio/%(ext)s;base64,%(data)s'>"
        + sorry
        + "</audio>"
    ),
    "image": "<img %(options)s src='data:image/%(ext)s;base64,%(data)s'>",
    "video": (
        "<video %(options)s"
        "src='data:video/%(ext)s;base64,%(data)s' controls>" + sorry + "</video>"
    ),
}


def html_embed(
    clip, filetype=None, maxduration=60, rd_kwargs=None, center=True, **html_kwargs
):
    """Returns HTML5 code embedding the clip.

    Parameters
    ----------

    clip : moviepy.Clip.Clip
      Either a file name, or a clip to preview.
      Either an image, a sound or a video. Clips will actually be
      written to a file and embedded as if a filename was provided.

    filetype : str, optional
      One of 'video','image','audio'. If None is given, it is determined
      based on the extension of ``filename``, but this can bug.

    maxduration : float, optional
      An error will be raised if the clip's duration is more than the indicated
      value (in seconds), to avoid spoiling the browser's cache and the RAM.

    rd_kwargs : dict, optional
      Keyword arguments for the rendering, like ``dict(fps=15, bitrate="50k")``.
      Allow you to give some options to the render process. You can, for
      example, disable the logger bar passing ``dict(logger=None)``.

    center : bool, optional
      If true (default), the content will be wrapped in a
      ``<div align=middle>`` HTML container, so the content will be displayed
      at the center.

    html_kwargs
      Allow you to give some options, like ``width=260``, ``autoplay=True``,
      ``loop=1`` etc.

    Examples
    --------
    .. code:: python

        from moviepy import *
        # later ...
        html_embed(clip, width=360)
        html_embed(clip.audio)

        clip.write_gif("test.gif")
        html_embed('test.gif')

        clip.save_frame("first_frame.jpeg")
        html_embed("first_frame.jpeg")
    """
    pass


def display_in_notebook(
    clip,
    filetype=None,
    maxduration=60,
    t=None,
    fps=None,
    rd_kwargs=None,
    center=True,
    **html_kwargs,
):
    """Displays clip content in an Jupyter Notebook.

    Remarks: If your browser doesn't support HTML5, this should warn you.
    If nothing is displayed, maybe your file or filename is wrong.
    Important: The media will be physically embedded in the notebook.

    Parameters
    ----------

    clip : moviepy.Clip.Clip
      Either the name of a file, or a clip to preview. The clip will actually
      be written to a file and embedded as if a filename was provided.

    filetype : str, optional
      One of ``"video"``, ``"image"`` or ``"audio"``. If None is given, it is
      determined based on the extension of ``filename``, but this can bug.

    maxduration : float, optional
      An error will be raised if the clip's duration is more than the indicated
      value (in seconds), to avoid spoiling the browser's cache and the RAM.

    t : float, optional
      If not None, only the frame at time t will be displayed in the notebook,
      instead of a video of the clip.

    fps : int, optional
      Enables to specify an fps, as required for clips whose fps is unknown.

    rd_kwargs : dict, optional
      Keyword arguments for the rendering, like ``dict(fps=15, bitrate="50k")``.
      Allow you to give some options to the render process. You can, for
      example, disable the logger bar passing ``dict(logger=None)``.

    center : bool, optional
      If true (default), the content will be wrapped in a
      ``<div align=middle>`` HTML container, so the content will be displayed
      at the center.

    kwargs
      Allow you to give some options, like ``width=260``, etc. When editing
      looping gifs, a good choice is ``loop=1, autoplay=1``.

    Examples
    --------

    .. code:: python

        from moviepy import *
        # later ...
        clip.display_in_notebook(width=360)
        clip.audio.display_in_notebook()

        clip.write_gif("test.gif")
        display_in_notebook('test.gif')

        clip.save_frame("first_frame.jpeg")
        display_in_notebook("first_frame.jpeg")
    """
    pass
