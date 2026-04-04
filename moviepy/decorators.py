"""Decorators used by moviepy."""

import inspect
import os

import decorator

from moviepy.tools import convert_to_seconds


@decorator.decorator
def outplace(func, clip, *args, **kwargs):
    """Applies ``func(clip.copy(), *args, **kwargs)`` and returns ``clip.copy()``."""
    pass


@decorator.decorator
def convert_masks_to_RGB(func, clip, *args, **kwargs):
    """If the clip is a mask, convert it to RGB before running the function."""
    pass


@decorator.decorator
def apply_to_mask(func, clip, *args, **kwargs):
    """Applies the same function ``func`` to the mask of the clip created with
    ``func``.
    """
    pass


@decorator.decorator
def apply_to_audio(func, clip, *args, **kwargs):
    """Applies the function ``func`` to the audio of the clip created with ``func``."""
    pass


@decorator.decorator
def requires_duration(func, clip, *args, **kwargs):
    """Raises an error if the clip has no duration."""
    pass


@decorator.decorator
def requires_fps(func, clip, *args, **kwargs):
    """Raises an error if the clip has no fps."""
    pass


@decorator.decorator
def audio_video_effect(func, effect, clip, *args, **kwargs):
    """Use an audio function on a video/audio clip.

    This decorator tells that the function func (audioclip -> audioclip)
    can be also used on a video clip, at which case it returns a
    videoclip with unmodified video and modified audio.
    """
    pass


def preprocess_args(preprocess_func, varnames):
    """Applies preprocess_func to variables in varnames before launching
    the function.
    """

    def decor(func):
        argnames = inspect.getfullargspec(func).args

        def wrapper(func, *args, **kwargs):
            new_args = [
                (
                    preprocess_func(arg)
                    if (name in varnames) and (arg is not None)
                    else arg
                )
                for (arg, name) in zip(args, argnames)
            ]
            new_kwargs = {
                kwarg: preprocess_func(value) if kwarg in varnames else value
                for (kwarg, value) in kwargs.items()
            }
            return func(*new_args, **new_kwargs)

        return decorator.decorate(func, wrapper)

    return decor


def convert_parameter_to_seconds(varnames):
    """Converts the specified variables to seconds."""
    return preprocess_args(convert_to_seconds, varnames)


def convert_path_to_string(varnames):
    """Converts the specified variables to a path string."""
    return preprocess_args(os.fspath, varnames)


@decorator.decorator
def add_mask_if_none(func, clip, *args, **kwargs):
    """Add a mask to the clip if there is none."""
    pass


def use_clip_fps_by_default(func):
    """Will use ``clip.fps`` if no ``fps=...`` is provided in **kwargs**."""
    pass
