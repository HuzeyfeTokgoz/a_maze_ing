"""Colour themes used by the terminal renderer."""
from dataclasses import dataclass

RESET = "\033[0m"


@dataclass(frozen=True)
class Theme:
    """ANSI colours for each part of the maze.

    Attributes:
        name: Name shown to the user.
        wall: Colour of the walls.
        pattern: Colour of the closed cells drawing the '42'.
        path: Colour of the shortest path.
        marker: Colour of the entry (E) and exit (X) markers.
    """

    name: str
    wall: str
    pattern: str
    path: str
    marker: str


THEMES: list[Theme] = [
    Theme("Classic", wall="\033[39m", pattern="\033[93m",
          path="\033[92m", marker="\033[91m"),

    Theme("Ocean", wall="\033[94m", pattern="\033[96m",
          path="\033[93m", marker="\033[97m"),

    Theme("Forest", wall="\033[32m", pattern="\033[33m",
          path="\033[92m", marker="\033[91m"),

    Theme("Lava", wall="\033[91m", pattern="\033[93m",
          path="\033[97m", marker="\033[96m"),

    Theme("Neon", wall="\033[95m", pattern="\033[96m",
          path="\033[92m", marker="\033[93m"),

    Theme("Sand", wall="\033[33m", pattern="\033[91m",
          path="\033[94m", marker="\033[92m"),
]
