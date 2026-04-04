"""MoviePy audio writing with ffmpeg."""

import subprocess as sp

import proglog

from moviepy.config import FFMPEG_BINARY
from moviepy.decorators import requires_duration
from moviepy.tools import cross_platform_popen_params, ffmpeg_escape_filename


class FFMPEG_AudioWriter:
    """
    A class to write an AudioClip into an audio file.

    Parameters
    ----------

    filename
      Name of any video or audio file, like ``video.mp4`` or ``sound.wav`` etc.

    size
      Size (width,height) in pixels of the output video.

    fps_input
      Frames per second of the input audio (given by the AudioClip being
      written down).

    nbytes : int, optional
      Number of bytes per sample. Default is 2 (16-bit audio).

    nchannels : int, optional
      Number of audio channels. Default is 2 (stereo).

    codec : str, optional
        The codec to use for the output. Default is ``libfdk_aac``.

    bitrate:
      A string indicating the bitrate of the final video. Only
      relevant for codecs which accept a bitrate.

    input_video : str, optional
      Path to an input video file. If provided, the audio will be muxed with this video.
      If not provided, the output will be audio-only.

    logfile : file-like object or None, optional
      A file object where FFMPEG logs will be written. If None, logs are suppressed.

    ffmpeg_params : list of str, optional
      Additional FFMPEG command-line parameters to customize the output.
    """

    def __init__(
        self,
        filename,
        fps_input,
        nbytes=2,
        nchannels=2,
        codec="libfdk_aac",
        bitrate=None,
        input_video=None,
        logfile=None,
        ffmpeg_params=None,
    ):
        if logfile is None:
            logfile = sp.PIPE
        self.logfile = logfile
        self.filename = filename
        self.codec = codec
        self.ext = self.filename.split(".")[-1]

        # order is important
        cmd = [
            FFMPEG_BINARY,
            "-y",
            "-loglevel",
            "error" if logfile == sp.PIPE else "info",
            "-f",
            "s%dle" % (8 * nbytes),
            "-acodec",
            "pcm_s%dle" % (8 * nbytes),
            "-ar",
            "%d" % fps_input,
            "-ac",
            "%d" % nchannels,
            "-i",
            "-",
        ]
        if input_video is None:
            cmd.extend(["-vn"])
        else:
            cmd.extend(["-i", ffmpeg_escape_filename(input_video), "-vcodec", "copy"])

        cmd.extend(["-acodec", codec] + ["-ar", "%d" % fps_input])
        cmd.extend(["-strict", "-2"])  # needed to support codec 'aac'
        if bitrate is not None:
            cmd.extend(["-ab", bitrate])
        if ffmpeg_params is not None:
            cmd.extend(ffmpeg_params)
        cmd.extend([ffmpeg_escape_filename(filename)])

        popen_params = cross_platform_popen_params(
            {"stdout": sp.DEVNULL, "stderr": logfile, "stdin": sp.PIPE}
        )

        self.proc = sp.Popen(cmd, **popen_params)

    def write_frames(self, frames_array):
        """Send the audio frame (a chunck of ``AudioClip``) to ffmpeg for writting"""
        pass

    def close(self):
        """Closes the writer, terminating the subprocess if is still alive."""
        pass

    def __del__(self):
        # If the garbage collector comes, make sure the subprocess is terminated.
        self.close()

    # Support the Context Manager protocol, to ensure that resources are cleaned up.

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


@requires_duration
def ffmpeg_audiowrite(
    clip,
    filename,
    fps,
    nbytes,
    buffersize,
    codec="libvorbis",
    bitrate=None,
    write_logfile=False,
    ffmpeg_params=None,
    logger="bar",
):
    """
    A function that wraps the FFMPEG_AudioWriter to write an AudioClip
    to a file.
    """
    pass
