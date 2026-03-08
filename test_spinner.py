import textwrap
from map import map_extract
from spinner import compute_horizontal_limits, compute_vertical_limits


def test_horizontal_limits()-> None:

    doc = textwrap.dedent("""
    width: 5
    height: 3
    ---
    XXXXX
    X s X
    XXXXX
    """)

    game_map = map_extract(doc)

    limits = compute_horizontal_limits(game_map, 2, 1)

    assert limits.min_pos == 1
    assert limits.max_pos == 3


def test_vertical_limits() -> None:

    doc = textwrap.dedent("""
    width: 3
    height: 5
    ---
    XXX
    X S X
    X   X
    X   X
    XXX
    """)

    game_map = map_extract(doc)

    limits = compute_vertical_limits(game_map, 1, 3)

    assert limits.min_pos == 1
    assert limits.max_pos == 3