"""MoviePy audio reading with ffmpeg."""

import subprocess as sp
import warnings

import numpy as np

from moviepy.config import FFMPEG_BINARY
from moviepy.tools import cross_platform_popen_params, ffmpeg_escape_filename
from moviepy.video.io.ffmpeg_reader import ffmpeg_parse_infos


class FFMPEG_AudioReader:
    """A class to read the audio in either video files or audio files
    using ffmpeg. ffmpeg will read any audio and transform them into
    raw data.

    Parameters
    ----------

    filename
      Name of any video or audio file, like ``video.mp4`` or
      ``sound.wav`` etc.

    buffersize
      The size of the buffer to use. Should be bigger than the buffer
      used by ``write_audiofile``

    print_infos
      Print the ffmpeg infos on the file being read (for debugging)

    fps
      Desired frames per second in the decoded signal that will be
      received from ffmpeg

    nbytes
      Desired number of bytes (1,2,4) in the signal that will be
      received from ffmpeg
    """

    def __init__(
        self,
        filename,
        buffersize,
        decode_file=False,
        print_infos=False,
        fps=44100,
        nbytes=2,
        nchannels=2,
    ):
        # TODO bring FFMPEG_AudioReader more in line with FFMPEG_VideoReader
        # E.g. here self.pos is still 1-indexed.
        # (or have them inherit from a shared parent class)
        self.filename = filename
        self.nbytes = nbytes
        self.fps = fps
        self.format = "s%dle" % (8 * nbytes)
        self.codec = "pcm_s%dle" % (8 * nbytes)
        self.nchannels = nchannels
        infos = ffmpeg_parse_infos(filename, decode_file=decode_file)
        self.duration = infos["duration"]
        self.bitrate = infos["audio_bitrate"]
        self.infos = infos
        self.proc = None

        self.n_frames = int(self.fps * self.duration)
        self.buffersize = min(self.n_frames + 1, buffersize)
        self.buffer = None
        self.buffer_startframe = 1
        self.initialize()
        self.buffer_around(1)

    def initialize(self, start_time=0):
        """Opens the file, creates the pipe."""
        pass

    def skip_chunk(self, chunksize):
        """Skip a chunk of audio data by reading and discarding the specified number of
        frames from the audio stream. The audio stream is read from the `proc` stdout.
        After skipping the chunk, the `pos` attribute is updated accordingly.

        Parameters
        ----------
        chunksize (int):
          The number of audio frames to skip.
        """
        pass

    def read_chunk(self, chunksize):
        """Read a chunk of audio data from the audio stream.

        This method reads a chunk of audio data from the audio stream. The
        specified number of frames, given by `chunksize`, is read from the
        `proc` stdout. The audio data is returned as a NumPy array, where
        each row corresponds to a frame and each column corresponds to a
        channel. If there is not enough audio left to read, the remaining
        portion is padded with zeros, ensuring that the returned array has
        the desired length. The `pos` attribute is updated accordingly.

        Parameters
        ----------
        chunksize (float):
          The desired number of audio frames to read.

        """
        pass

    def seek(self, pos):
        """Read a frame at time t. Note for coders: getting an arbitrary
        frame in the video with ffmpeg can be painfully slow if some
        decoding has to be done. This function tries to avoid fectching
        arbitrary frames whenever possible, by moving between adjacent
        frames.
        """
        pass

    def get_frame(self, tt):
        """Retrieve the audio frame(s) corresponding to the given timestamp(s).

        Parameters
        ----------
        tt (float or numpy.ndarray):
          The timestamp(s) at which to retrieve the audio frame(s).
          If `tt` is a single float value, the frame corresponding to that
          timestamp is returned. If `tt` is a NumPy array of timestamps, an
          array of frames corresponding to each timestamp is returned.
        """
        pass

    def buffer_around(self, frame_number):
        """Fill the buffer with frames, centered on frame_number if possible."""
        pass

    def close(self):
        """Closes the reader, terminating the subprocess if is still alive."""
        pass

    def __del__(self):
        # If the garbage collector comes, make sure the subprocess is terminated.
        self.close()
