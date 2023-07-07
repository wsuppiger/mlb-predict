from main import get_winner_map

test_points_data = {
    "options": {
        "hit": {"suboptions": ["single", "double"], "points": 100},
        "out": {"suboptions": ["strikeout"], "points": 15},
        "other": {"suboptions": ["walk"], "points": 100},
    },
    "suboptions": {
        "single": {"events": ["Single"], "points": 40},
        "double": {"events": ["Double"], "points": 5},
        "strikeout": {"events": ["Strikeout"], "points": 40},
        "walk": {"events": ["Walk"], "points": 100},
    },
}


def test_get_winner_map_single():
    lastAtBatEvent = "Single"
    expected_winner_map = {"single": 140, "double": 100}

    winner_map = get_winner_map(test_points_data, lastAtBatEvent)

    assert winner_map == expected_winner_map


def test_get_winner_map_double():
    lastAtBatEvent = "Double"
    expected_winner_map = {"single": 100, "double": 105}

    winner_map = get_winner_map(test_points_data, lastAtBatEvent)

    assert winner_map == expected_winner_map


test_get_winner_map_single()
test_get_winner_map_double()
