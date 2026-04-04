from dataclasses import dataclass

from moviepy.Clip import Clip
from moviepy.Effect import Effect


@dataclass
class MultiplySpeed(Effect):
    """Returns a clip playing the current clip but at a speed multiplied by ``factor``.

    Instead of factor one can indicate the desired ``final_duration`` of the clip, and
    the factor will be automatically computed. The same effect is applied to the clip's
    audio and mask if any.
    """

    factor: float = None
    final_duration: float = None

    def apply(self, clip: Clip) -> Clip:
        """Apply the effect to the clip."""
        pass
