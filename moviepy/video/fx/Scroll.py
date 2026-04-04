from moviepy.Effect import Effect


class Scroll(Effect):
    """Effect that scrolls horizontally or vertically a clip, e.g. to make end credits

    Parameters
    ----------
    w, h
      The width and height of the final clip. Default to clip.w and clip.h

    x_speed, y_speed
      The speed of the scroll in the x and y directions.

    x_start, y_start
      The starting position of the scroll in the x and y directions.


    apply_to
      Whether to apply the effect to the mask too.
    """

    def __init__(
        self,
        w=None,
        h=None,
        x_speed=0,
        y_speed=0,
        x_start=0,
        y_start=0,
        apply_to="mask",
    ):
        self.w = w
        self.h = h
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.x_start = x_start
        self.y_start = y_start
        self.apply_to = apply_to

    def apply(self, clip):
        """Apply the effect to the clip."""
        pass
