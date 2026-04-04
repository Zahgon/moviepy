from dataclasses import dataclass

from moviepy.Clip import Clip
from moviepy.Effect import Effect


@dataclass
class LumContrast(Effect):
    """Luminosity-contrast correction of a clip."""

    lum: float = 0
    contrast: float = 0
    contrast_threshold: float = 127

    def apply(self, clip: Clip) -> Clip:
        """Apply the effect to the clip."""
        pass
