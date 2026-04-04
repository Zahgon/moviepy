"""Classes for easy interpolation of trajectories and curves."""

import numpy as np


class Interpolator:
    """Poorman's linear interpolator.

    Parameters
    ----------

    tt : list, optional
      List of time frames for the interpolator.

    ss : list, optional
      List of values for the interpolator.

    ttss : list, optional
      Lists of time frames and their correspondients values for the
      interpolator. This argument can be used instead of ``tt`` and ``ss``
      to instantiate the interpolator using an unique argument.

    left : float, optional
      Value to return when ``t < tt[0]``.

    right : float, optional
      Value to return when ``t > tt[-1]``.


    Examples
    --------

    .. code:: python

        # instantiate using `tt` and `ss`
        interpolator = Interpolator(tt=[0, 1, 2], ss=[3, 4, 5])

        # instantiate using `ttss`
        interpolator = Interpolator(ttss=[[0, 3], [1, 4], [2, 5]])  # [t, value]
    """

    def __init__(self, tt=None, ss=None, ttss=None, left=None, right=None):
        if ttss is not None:
            tt, ss = zip(*ttss)

        self.tt = 1.0 * np.array(tt)
        self.ss = 1.0 * np.array(ss)
        self.left = left
        self.right = right
        self.tmin, self.tmax = min(tt), max(tt)

    def __call__(self, t):
        """Interpolates ``t``.

        Parameters
        ----------

        t : float
          Time frame for which the correspondent value will be returned.
        """
        return np.interp(t, self.tt, self.ss, self.left, self.right)


class Trajectory:
    """Trajectory compound by time frames and (x, y) pixels.

    It's designed as an interpolator, so you can get the position at a given
    time ``t``. You can instantiate it from a file using the methods
    ``from_file`` and ``load_list``.


    Parameters
    ----------

    tt : list or numpy.ndarray
      Time frames.

    xx : list or numpy.ndarray
      X positions in the trajectory.

    yy : list or numpy.ndarray
      Y positions in the trajectory.


    Examples
    --------

    >>> trajectory = Trajectory([0, .166, .333], [554, 474, 384], [100, 90, 91])
    """

    def __init__(self, tt, xx, yy):
        self.tt = 1.0 * np.array(tt)
        self.xx = np.array(xx)
        self.yy = np.array(yy)
        self.update_interpolators()

    def __call__(self, t):
        """Interpolates the trajectory at the given time ``t``.

        Parameters
        ----------

        t : float
          Time for which to the corresponding position will be returned.
        """
        return np.array([self.xi(t), self.yi(t)])

    def addx(self, x):
        """Adds a value to the ``xx`` position of the trajectory.

        Parameters
        ----------

        x : int
          Value added to ``xx`` in the trajectory.


        Returns
        -------

        Trajectory : new instance with the new X position included.
        """
        pass

    def addy(self, y):
        """Adds a value to the ``yy`` position of the trajectory.

        Parameters
        ----------

        y : int
          Value added to ``yy`` in the trajectory.


        Returns
        -------

        Trajectory : new instance with the new Y position included.
        """
        pass

    def update_interpolators(self):
        """Updates the internal X and Y position interpolators for the instance."""
        pass

    def txy(self, tms=False):
        """Returns all times with the X and Y values of each position.

        Parameters
        ----------

        tms : bool, optional
          If is ``True``, the time will be returned in milliseconds.
        """
        pass

    def to_file(self, filename):
        """Saves the trajectory data in a text file.

        Parameters
        ----------

        filename : str
          Path to the location of the new trajectory text file.
        """
        pass

    @staticmethod
    def from_file(filename):
        """Instantiates an object of Trajectory using a data text file.

        Parameters
        ----------

        filename : str
          Path to the location of trajectory text file to load.


        Returns
        -------

        Trajectory : new instance loaded from text file.
        """
        pass

    @staticmethod
    def save_list(trajs, filename):
        """Saves a set of trajectories into a text file.

        Parameters
        ----------

        trajs : list
          List of trajectories to be saved.

        filename : str
          Path of the text file that will store the trajectories data.
        """
        pass

    @staticmethod
    def load_list(filename):
        """Loads a list of trajectories from a data text file.

        Parameters
        ----------

        filename : str
          Path of the text file that stores the data of a set of trajectories.


        Returns
        -------

        list : List of trajectories loaded from the file.
        """
        pass
