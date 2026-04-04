"""Implements all the functions to read a video or a picture using ffmpeg."""

import os
import re
import subprocess as sp
import warnings

import numpy as np

from moviepy.config import FFMPEG_BINARY  # ffmpeg, ffmpeg.exe, etc...
from moviepy.tools import (
    convert_to_seconds,
    cross_platform_popen_params,
    ffmpeg_escape_filename,
)


class FFMPEG_VideoReader:
    """Class for video byte-level reading with ffmpeg."""

    def __init__(
        self,
        filename,
        decode_file=True,
        print_infos=False,
        bufsize=None,
        pixel_format="rgb24",
        check_duration=True,
        target_resolution=None,
        resize_algo="bicubic",
        fps_source="fps",
    ):
        self.filename = filename
        self.proc = None
        infos = ffmpeg_parse_infos(
            filename,
            check_duration=check_duration,
            fps_source=fps_source,
            decode_file=decode_file,
            print_infos=print_infos,
        )
        # If framerate is unavailable, assume 1.0 FPS to avoid divide-by-zero errors.
        self.fps = infos.get("video_fps", 1.0)
        # If frame size is unavailable, set 1x1 divide-by-zero errors.
        self.size = infos.get("video_size", (1, 1))

        # ffmpeg automatically rotates videos if rotation information is
        # available, so exchange width and height
        self.rotation = abs(infos.get("video_rotation", 0))
        if self.rotation in [90, 270]:
            self.size = [self.size[1], self.size[0]]

        if target_resolution:
            if None in target_resolution:
                ratio = 1
                for idx, target in enumerate(target_resolution):
                    if target:
                        ratio = target / self.size[idx]
                self.size = (int(self.size[0] * ratio), int(self.size[1] * ratio))
            else:
                self.size = target_resolution
        self.resize_algo = resize_algo

        self.duration = infos.get("video_duration", 0.0)
        self.ffmpeg_duration = infos.get("duration", 0.0)
        self.n_frames = infos.get("video_n_frames", 0)
        self.bitrate = infos.get("video_bitrate", 0)

        self.infos = infos

        self.pixel_format = pixel_format
        self.depth = 4 if pixel_format[-1] == "a" else 3
        # 'a' represents 'alpha' which means that each pixel has 4 values instead of 3.
        # See https://github.com/Zulko/moviepy/issues/1070#issuecomment-644457274

        if bufsize is None:
            w, h = self.size
            bufsize = self.depth * w * h + 100

        self.bufsize = bufsize
        self.initialize()

    def initialize(self, start_time=0):
        """
        Opens the file, creates the pipe.

        Sets self.pos to the appropriate value (1 if start_time == 0 because
        it pre-reads the first frame).
        """
        pass

    def skip_frames(self, n=1):
        """Reads and throws away n frames"""
        pass

    def read_frame(self):
        """
        Reads the next frame from the file.
        Note that upon (re)initialization, the first frame will already have been read
        and stored in ``self.last_read``.
        """
        pass

    def get_frame(self, t):
        """Read a file video frame at time t.

        Note for coders: getting an arbitrary frame in the video with
        ffmpeg can be painfully slow if some decoding has to be done.
        This function tries to avoid fetching arbitrary frames
        whenever possible, by moving between adjacent frames.
        """
        pass

    @property
    def lastread(self):
        """Alias of `self.last_read` for backwards compatibility with MoviePy 1.x."""
        pass

    def get_frame_number(self, t):
        """Helper method to return the frame number at time ``t``"""
        pass

    def close(self, delete_lastread=True):
        """Closes the reader terminating the process, if is still open."""
        pass

    def __del__(self):
        self.close()


def ffmpeg_read_image(filename, with_mask=True, pixel_format=None):
    """Read an image file (PNG, BMP, JPEG...).

    Wraps FFMPEG_Videoreader to read just one image.
    Returns an ImageClip.

    This function is not meant to be used directly in MoviePy.
    Use ImageClip instead to make clips out of image files.

    Parameters
    ----------

    filename
      Name of the image file. Can be of any format supported by ffmpeg.

    with_mask
      If the image has a transparency layer, ``with_mask=true`` will save
      this layer as the mask of the returned ImageClip

    pixel_format
      Optional: Pixel format for the image to read. If is not specified
      'rgb24' will be used as the default format unless ``with_mask`` is set
      as ``True``, then 'rgba' will be used.

    """
    pass


class FFmpegInfosParser:
    """Finite state ffmpeg `-i` command option file information parser.
    Is designed to parse the output fast, in one loop. Iterates line by
    line of the `ffmpeg -i <filename> [-f null -]` command output changing
    the internal state of the parser.

    Parameters
    ----------

    filename
      Name of the file parsed, only used to raise accurate error messages.

    infos
      Information returned by FFmpeg.

    fps_source
      Indicates what source data will be preferably used to retrieve fps data.

    check_duration
      Enable or disable the parsing of the duration of the file. Useful to
      skip the duration check, for example, for images.

    decode_file
      Indicates if the whole file has been decoded. The duration parsing strategy
      will differ depending on this argument.
    """

    def __init__(
        self,
        infos,
        filename,
        fps_source="fps",
        check_duration=True,
        decode_file=False,
    ):
        self.infos = infos
        self.filename = filename
        self.check_duration = check_duration
        self.fps_source = fps_source
        self.duration_tag_separator = "time=" if decode_file else "Duration: "

        self._reset_state()

    def _reset_state(self):
        """Reinitializes the state of the parser. Used internally at
        initialization and at the end of the parsing process.
        """
        pass

    def parse(self):
        """Parses the information returned by FFmpeg in stderr executing their binary
        for a file with ``-i`` option and returns a dictionary with all data needed
        by MoviePy.
        """
        pass

    def parse_data_by_stream_type(self, stream_type, line):
        """Parses data from "Stream ... {stream_type}" line."""
        pass

    def parse_audio_stream_data(self, line):
        """Parses data from "Stream ... Audio" line."""
        pass

    def parse_video_stream_data(self, line):
        """Parses data from "Stream ... Video" line."""
        pass

    def parse_fps(self, line):
        """Parses number of FPS from a line of the ``ffmpeg -i`` command output."""
        pass

    def parse_tbr(self, line):
        """Parses number of TBS from a line of the ``ffmpeg -i`` command output."""
        pass

    def parse_duration(self, line):
        """Parse the duration from the line that outputs the duration of
        the container.
        """
        pass

    def parse_metadata_field_value(
        self,
        line,
    ):
        """Returns a tuple with a metadata field-value pair given a ffmpeg `-i`
        command output line.
        """
        pass

    def video_metadata_type_casting(self, field, value):
        """Cast needed video metadata fields to other types than the default str."""
        pass


def ffmpeg_parse_infos(
    filename,
    check_duration=True,
    fps_source="fps",
    decode_file=False,
    print_infos=False,
):
    """Get the information of a file using ffmpeg.

    Returns a dictionary with next fields:

    - ``"duration"``
    - ``"metadata"``
    - ``"inputs"``
    - ``"video_found"``
    - ``"video_fps"``
    - ``"video_n_frames"``
    - ``"video_duration"``
    - ``"video_bitrate"``
    - ``"video_metadata"``
    - ``"audio_found"``
    - ``"audio_fps"``
    - ``"audio_bitrate"``
    - ``"audio_metadata"``
    - ``"video_codec_name"``
    - ``"video_profile"``

    Note that "video_duration" is slightly smaller than "duration" to avoid
    fetching the incomplete frames at the end, which raises an error.

    Parameters
    ----------

    filename
      Name of the file parsed, only used to raise accurate error messages.

    infos
      Information returned by FFmpeg.

    fps_source
      Indicates what source data will be preferably used to retrieve fps data.

    check_duration
      Enable or disable the parsing of the duration of the file. Useful to
      skip the duration check, for example, for images.

    decode_file
      Indicates if the whole file must be read to retrieve their duration.
      This is needed for some files in order to get the correct duration (see
      https://github.com/Zulko/moviepy/pull/1222).
    """
    pass
