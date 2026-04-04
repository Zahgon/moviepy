"""Contains everything that can help automate the cuts in MoviePy."""

from collections import defaultdict

import numpy as np

from moviepy.decorators import convert_parameter_to_seconds, use_clip_fps_by_default


@use_clip_fps_by_default
@convert_parameter_to_seconds(["start_time"])
def find_video_period(clip, fps=None, start_time=0.3):
    """Find the period of a video based on frames correlation.

    Parameters
    ----------

    clip : moviepy.Clip.Clip
      Clip for which the video period will be computed.

    fps : int, optional
      Number of frames per second used computing the period. Higher values will
      produce more accurate periods, but the execution time will be longer.

    start_time : float, optional
      First timeframe used to calculate the period of the clip.

    Examples
    --------

    .. code:: python

        from moviepy import *
        from moviepy.video.tools.cuts import find_video_period

        clip = VideoFileClip("media/chaplin.mp4").subclipped(0, 1).loop(2)
        round(videotools.find_video_period(clip, fps=80), 6)
        1
    """
    pass


class FramesMatch:
    """Frames match inside a set of frames.

    Parameters
    ----------

    start_time : float
      Starting time.

    end_time : float
      End time.

    min_distance : float
      Lower bound on the distance between the first and last frames

    max_distance : float
      Upper bound on the distance between the first and last frames
    """

    def __init__(self, start_time, end_time, min_distance, max_distance):
        self.start_time = start_time
        self.end_time = end_time
        self.min_distance = min_distance
        self.max_distance = max_distance
        self.time_span = end_time - start_time

    def __str__(self):  # pragma: no cover
        return "(%.04f, %.04f, %.04f, %.04f)" % (
            self.start_time,
            self.end_time,
            self.min_distance,
            self.max_distance,
        )

    def __repr__(self):  # pragma: no cover
        return self.__str__()

    def __iter__(self):  # pragma: no cover
        return iter(
            (self.start_time, self.end_time, self.min_distance, self.max_distance)
        )

    def __eq__(self, other):
        return (
            other.start_time == self.start_time
            and other.end_time == self.end_time
            and other.min_distance == self.min_distance
            and other.max_distance == self.max_distance
        )


class FramesMatches(list):
    """Frames matches inside a set of frames.

    You can instantiate it passing a list of FramesMatch objects or
    using the class methods ``load`` and ``from_clip``.

    Parameters
    ----------

    lst : list
      Iterable of FramesMatch objects.
    """

    def __init__(self, lst):
        list.__init__(self, sorted(lst, key=lambda e: e.max_distance))

    def best(self, n=1, percent=None):
        """Returns a new instance of FramesMatches object or a FramesMatch
        from the current class instance given different conditions.

        By default returns the first FramesMatch that the current instance
        stores.

        Parameters
        ----------

        n : int, optional
          Number of matches to retrieve from the current FramesMatches object.
          Only has effect when ``percent=None``.

        percent : float, optional
          Percent of the current match to retrieve.

        Returns
        -------

        FramesMatch or FramesMatches : If the number of matches to retrieve is
          greater than 1 returns a FramesMatches object, otherwise a
          FramesMatch.

        """
        pass

    def filter(self, condition):
        """Return a FramesMatches object obtained by filtering out the
        FramesMatch which do not satistify a condition.

        Parameters
        ----------

        condition : func
          Function which takes a FrameMatch object as parameter and returns a
          bool.

        Examples
        --------
        .. code:: python

            # Only keep the matches corresponding to (> 1 second) sequences.
            new_matches = matches.filter(lambda match: match.time_span > 1)
        """
        pass

    def save(self, filename):
        """Save a FramesMatches object to a file.

        Parameters
        ----------

        filename : str
          Path to the file in which will be dumped the FramesMatches object data.
        """
        pass

    @staticmethod
    def load(filename):
        """Load a FramesMatches object from a file.

        Parameters
        ----------

        filename : str
          Path to the file to use loading a FramesMatches object.

        Examples
        --------
        >>> matching_frames = FramesMatches.load("somefile")
        """
        pass

    @staticmethod
    def from_clip(clip, distance_threshold, max_duration, fps=None, logger="bar"):
        """Finds all the frames that look alike in a clip, for instance to make
        a looping GIF.

        Parameters
        ----------

        clip : moviepy.video.VideoClip.VideoClip
          A MoviePy video clip.

        distance_threshold : float
          Distance above which a match is rejected.

        max_duration : float
          Maximal duration (in seconds) between two matching frames.

        fps : int, optional
          Frames per second (default will be ``clip.fps``).

        logger : str, optional
          Either ``"bar"`` for progress bar or ``None`` or any Proglog logger.

        Returns
        -------

        FramesMatches
            All pairs of frames with ``end_time - start_time < max_duration``
            and whose distance is under ``distance_threshold``.

        Examples
        --------

        We find all matching frames in a given video and turn the best match
        with a duration of 1.5 seconds or more into a GIF:

        .. code:: python

            from moviepy import VideoFileClip
            from moviepy.video.tools.cuts import FramesMatches

            clip = VideoFileClip("foo.mp4").resize(width=200)
            matches = FramesMatches.from_clip(
                clip, distance_threshold=10, max_duration=3,  # will take time
            )
            best = matches.filter(lambda m: m.time_span > 1.5).best()
            clip.subclipped(best.start_time, best.end_time).write_gif("foo.gif")
        """
        pass

    def select_scenes(
        self, match_threshold, min_time_span, nomatch_threshold=None, time_distance=0
    ):
        """Select the scenes at which a video clip can be reproduced as the
        smoothest possible way, mainly oriented for the creation of GIF images.

        Parameters
        ----------

        match_threshold : float
          Maximum distance possible between frames. The smaller, the
          better-looping the GIFs are.

        min_time_span : float
          Minimum duration for a scene. Only matches with a duration longer
          than the value passed to this parameters will be extracted.

        nomatch_threshold : float, optional
          Minimum distance possible between frames. If is ``None``, then it is
          chosen equal to ``match_threshold``.

        time_distance : float, optional
          Minimum time offset possible between matches.

        Returns
        -------

        FramesMatches : New instance of the class with the selected scenes.

        Examples
        --------

        .. code:: python

            from pprint import pprint
            from moviepy import *
            from moviepy.video.tools.cuts import FramesMatches

            ch_clip = VideoFileClip("media/chaplin.mp4").subclipped(1, 4)
            mirror_and_clip = [ch_clip.with_effects([vfx.TimeMirror()]), ch_clip]
            clip = concatenate_videoclips(mirror_and_clip)

            result = FramesMatches.from_clip(clip, 10, 3).select_scenes(
                1, 2, nomatch_threshold=0,
            )
            print(result)
            # [(1.0000, 4.0000, 0.0000, 0.0000),
            #  (1.1600, 3.8400, 0.0000, 0.0000),
            #  (1.2800, 3.7200, 0.0000, 0.0000),
            #  (1.4000, 3.6000, 0.0000, 0.0000)]
        """
        pass

    def write_gifs(self, clip, gifs_dir, **kwargs):
        """Extract the matching frames represented by the instance from a clip
        and write them as GIFs in a directory, one GIF for each matching frame.

        Parameters
        ----------

        clip : video.VideoClip.VideoClip
          A video clip whose frames scenes you want to obtain as GIF images.

        gif_dir : str
          Directory in which the GIF images will be written.

        kwargs
          Passed as ``clip.write_gif`` optional arguments.

        Examples
        --------

        .. code:: python

            import os
            from pprint import pprint
            from moviepy import *
            from moviepy.video.tools.cuts import FramesMatches

            ch_clip = VideoFileClip("media/chaplin.mp4").subclipped(1, 4)
            clip = concatenate_videoclips([ch_clip.time_mirror(), ch_clip])

            result = FramesMatches.from_clip(clip, 10, 3).select_scenes(
                1, 2, nomatch_threshold=0,
            )

            os.mkdir("foo")
            result.write_gifs(clip, "foo")
            # MoviePy - Building file foo/00000100_00000400.gif with imageio.
            # MoviePy - Building file foo/00000115_00000384.gif with imageio.
            # MoviePy - Building file foo/00000128_00000372.gif with imageio.
            # MoviePy - Building file foo/00000140_00000360.gif with imageio.
        """
        pass


@use_clip_fps_by_default
def detect_scenes(
    clip=None, luminosities=None, luminosity_threshold=10, logger="bar", fps=None
):
    """Detects scenes of a clip based on luminosity changes.

    Note that for large clip this may take some time.

    Returns
    -------

    tuple : cuts, luminosities
      cuts is a series of cuts [(0,t1), (t1,t2),...(...,tf)]
      luminosities are the luminosities computed for each
      frame of the clip.

    Parameters
    ----------

    clip : video.VideoClip.VideoClip, optional
      A video clip. Can be None if a list of luminosities is
      provided instead. If provided, the luminosity of each
      frame of the clip will be computed. If the clip has no
      'fps' attribute, you must provide it.

    luminosities : list, optional
      A list of luminosities, e.g. returned by detect_scenes
      in a previous run.

    luminosity_threshold : float, optional
      Determines a threshold above which the 'luminosity jumps'
      will be considered as scene changes. A scene change is defined
      as a change between 2 consecutive frames that is larger than
      (avg * thr) where avg is the average of the absolute changes
      between consecutive frames.

    logger : str, optional
      Either ``"bar"`` for progress bar or ``None`` or any Proglog logger.

    fps : int, optional
      Frames per second value. Must be provided if you provide
      no clip or a clip without fps attribute.
    """
    pass
