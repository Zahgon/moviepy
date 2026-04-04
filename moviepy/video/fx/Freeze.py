from dataclasses import dataclass

from moviepy.Clip import Clip
from moviepy.Effect import Effect
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips


@dataclass
class Freeze(Effect):
    """Momentarily freeze the clip at time t.

    Set `t='end'` to freeze the clip at the end (actually it will freeze on the
    frame at time clip.duration - padding_end seconds - 1 / clip_fps).
    With ``duration`` you can specify the duration of the freeze.
    With ``total_duration`` you can specify the total duration of
    the clip and the freeze (i.e. the duration of the freeze is
    automatically computed). One of them must be provided.

    With ``update_start_end`` you can define if the effect must preserve
    and/or update start and end properties of the original clip
    """

    t: float = 0
    freeze_duration: float = None
    total_duration: float = None
    padding_end: float = 0
    update_start_end: bool = True

    def apply(self, clip: Clip) -> Clip:
        """Apply the effect to the clip."""
        pass
