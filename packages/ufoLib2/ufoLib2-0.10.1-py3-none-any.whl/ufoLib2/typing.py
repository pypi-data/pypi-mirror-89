import os
import sys
from typing import Optional, TypeVar, Union

from fontTools.pens.basePen import AbstractPen

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol


T = TypeVar("T")
"""Generic variable for mypy for trivial generic function signatures."""

PathLike = Union[str, bytes, "os.PathLike[str]", "os.PathLike[bytes]"]
"""Represents a path in various possible forms."""


class Drawable(Protocol):
    """Stand-in for an object that can draw itself with a given pen.

    See :mod:`fontTools.pens.basePen` for an introduction to pens.
    """

    def draw(self, pen: AbstractPen) -> None:
        ...


class HasIdentifier(Protocol):
    """Any object that has a unique identifier in some context that can be
    used as a key in a public.objectLibs dictionary."""

    identifier: Optional[str]
