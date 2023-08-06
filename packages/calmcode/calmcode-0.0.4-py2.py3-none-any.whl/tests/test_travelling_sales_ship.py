import pytest

from calmcode.challenge import TravellingSalesmanShip


def test_base_usage():
    """
    Just to check we get the basic outputs we expect.
    """
    tour = list(range(100))

    result = TravellingSalesmanShip(100).score({"tour": tour})
    assert "score" in result.keys()
    assert "total_distance" in result.keys()
    assert "total_angle" in result.keys()


def test_raise_error_no_tour():
    """
    If no tour is passed, raise error.
    """

    tour = list(range(100))

    with pytest.raises(ValueError):
        _ = TravellingSalesmanShip(100).score({"t": tour})


@pytest.mark.parametrize('t', [[1, 2, 3], list(range(11)), list(range(5, 10))])
def test_raise_error_bad_tour(t):
    """
    If bad tour is passed, raise error.
    """

    with pytest.raises(ValueError):
        _ = TravellingSalesmanShip(10).score({"t": t})
