import pytest

from sweeper.draw import draw


def test_draw():
    participants = ["Harold", "Jim", "Margaret"]
    teams = ["Bengals", "Bills", "Chiefs"]
    result = draw(participants=participants, teams=teams, delay=0)
    assert len(result) == 3
    assert list(result.keys()) == ["Harold", "Jim", "Margaret"]


def test_too_few_teams_raises_error():
    with pytest.raises(ValueError):
        participants = ["Harold", "Jim"]
        teams = ["Bengals"]
        draw(participants=participants, teams=teams, delay=0)


def test_too_few_participants_is_ok():
    participants = ["Jim"]
    teams = ["Bengals", "Bills"]
    result = draw(participants=participants, teams=teams, delay=0)
    assert len(result) == 1
    assert next(iter(result)) == "Jim"
