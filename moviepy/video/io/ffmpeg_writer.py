"""
On the long term this will implement several methods to make videos
out of VideoClips
"""

import subprocess as sp

import numpy as np
from proglog import proglog

from moviepy.config import FFMPEG_BINARY
from moviepy.tools import cross_platform_popen_params, ffmpeg_escape_filename


class FFMPEG_VideoWriter:
    """A class for FFMPEG-based video writing.

    Parameters
    ----------

    filename : str
      Any filename like ``"video.mp4"`` etc. but if you want to avoid
      complications it is recommended to use the generic extension ``".avi"``
      for all your videos.

    size : tuple or list
      Size of the output video in pixels (width, height).

    fps : int
      Frames per second in the output video file.

    codec : str, optional
      FFMPEG codec. It seems that in terms of quality the hierarchy is
      'rawvideo' = 'png' > 'mpeg4' > 'libx264'
      'png' manages the same lossless quality as 'rawvideo' but yields
      smaller files. Type ``ffmpeg -codecs`` in a terminal to get a list
      of accepted codecs.

      Note for default 'libx264': by default the pixel format yuv420p
      is used. If the video dimensions are not both even (e.g. 720x405)
      another pixel format is used, and this can cause problem in some
      video readers.

    audiofile : str, optional
      The name of an audio file that will be incorporated to the video.

    audio_codec : str, optional
      FFMPEG audio codec. If None, ``"copy"`` codec is used.

    preset : str, optional
      Sets the time that FFMPEG will take to compress the video. The slower,
      the better the compression rate. Possibilities are: ``"ultrafast"``,
      ``"superfast"``, ``"veryfast"``, ``"faster"``, ``"fast"``,  ``"medium"``
      (default), ``"slow"``, ``"slower"``, ``"veryslow"``, ``"placebo"``.

    bitrate : str, optional
      Only relevant for codecs which accept a bitrate. "5000k" offers
      nice results in general.

    with_mask : bool, optional
      Set to ``True`` if there is a mask in the video to be encoded.

    pixel_format : str, optional
      Optional: Pixel format for the output video file. If is not specified
      ``"rgb24"`` will be used as the default format unless ``with_mask`` is
      set as ``True``, then ``"rgba"`` will be used.

    logfile : int, optional
      File descriptor for logging output. If not defined, ``subprocess.PIPE``
      will be used. Defined using another value, the log level of the ffmpeg
      command will be "info", otherwise "error".

    threads : int, optional
      Number of threads used to write the output with ffmpeg.

    ffmpeg_params : list, optional
      Additional parameters passed to ffmpeg command.
    """

    def __init__(
        self,
        filename,
        size,
        fps,
        codec="libx264",
        audiofile=None,
        audio_codec=None,
        preset="medium",
        bitrate=None,
        with_mask=False,
        logfile=None,
        threads=None,
        ffmpeg_params=None,
        pixel_format=None,
    ):
        if logfile is None:
            logfile = sp.PIPE
        self.logfile = logfile
        self.filename = filename
        self.codec = codec
        self.audio_codec = audio_codec
        self.ext = self.filename.split(".")[-1]

        pixel_format = "rgba" if with_mask else "rgb24"

        # order is important
        cmd = [
            FFMPEG_BINARY,
            "-y",
            "-loglevel",
            "error" if logfile == sp.PIPE else "info",
            "-f",
            "rawvideo",
            "-vcodec",
            "rawvideo",
            "-s",
            "%dx%d" % (size[0], size[1]),
            "-pix_fmt",
            pixel_format,
            "-r",
            "%.02f" % fps,
            "-an",
            "-i",
            "-",
        ]
        if audiofile is not None:
            if audio_codec is None:
                audio_codec = "copy"
            cmd.extend(["-i", audiofile, "-acodec", audio_codec])

        if codec == "h264_nvenc":
            cmd.extend(["-c:v", codec])
        else:
            cmd.extend(["-vcodec", codec])

        cmd.extend(["-preset", preset])

        if ffmpeg_params is not None:
            cmd.extend(ffmpeg_params)

        if bitrate is not None:
            cmd.extend(["-b", bitrate])

        if threads is not None:
            cmd.extend(["-threads", str(threads)])

        # Disable auto alt ref for transparent webm and set pix format yo yuva420p
        if codec == "libvpx" and with_mask:
            cmd.extend(["-pix_fmt", "yuva420p"])
            cmd.extend(["-auto-alt-ref", "0"])
        elif (
            (codec == "libx264" or codec == "h264_nvenc")
            and (size[0] % 2 == 0)
            and (size[1] % 2 == 0)
        ):
            cmd.extend(["-pix_fmt", "yuva420p"])

        cmd.extend([ffmpeg_escape_filename(filename)])

        popen_params = cross_platform_popen_params(
            {"stdout": sp.DEVNULL, "stderr": logfile, "stdin": sp.PIPE}
        )

        self.proc = sp.Popen(cmd, **popen_params)

    def write_frame(self, img_array):
        """Writes one frame in the file."""
        pass

    def close(self):
        """Closes the writer, terminating the subprocess if is still alive."""
        pass

    # Support the Context Manager protocol, to ensure that resources are cleaned up.

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


def ffmpeg_write_video(
    clip,
    filename,
    fps,
    codec="libx264",
    bitrate=None,
    preset="medium",
    write_logfile=False,
    audiofile=None,
    audio_codec=None,
    threads=None,
    ffmpeg_params=None,
    logger="bar",
    pixel_format=None,
):
    """Write the clip to a videofile. See VideoClip.write_videofile for details
    on the parameters.
    """
    pass


def ffmpeg_write_image(filename, image, logfile=False, pixel_format=None):
    """Writes an image (HxWx3 or HxWx4 numpy array) to a file, using ffmpeg.

    Parameters
    ----------

    filename : str
        Path to the output file.

    image : np.ndarray
        Numpy array with the image data.

    logfile : bool, optional
        Writes the ffmpeg output inside a logging file (``True``) or not
        (``False``).

    pixel_format : str, optional
        Pixel format for ffmpeg. If not defined, it will be discovered checking
        if the image data contains an alpha channel (``"rgba"``) or not
        (``"rgb24"``).
    """
    pass
