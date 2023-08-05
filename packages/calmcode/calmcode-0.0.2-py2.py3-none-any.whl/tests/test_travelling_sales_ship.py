from calmcode.challenge import TravellingSalesmanShip


def test_base_usage():
    tour = list(range(100))

    result = TravellingSalesmanShip(100).score({"tour": tour})
    assert "score" in result.keys()
    assert "total_distance" in result.keys()
    assert "total_angle" in result.keys()
