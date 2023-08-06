from pyccolo.sorcery.spells import assigned_names


def test_assigned_names_basic():
    a, b = assigned_names()
    assert a == 'a'
    assert b == 'b'
