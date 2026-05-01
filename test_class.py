import pytest
from triangle_class import Triangle
from triangle_func import IncorrectTriangleSides

# Позитивные тесты
def test_create_triangle():
    t = Triangle(3, 4, 5)
    assert t.a == 3
    assert t.b == 4
    assert t.c == 5


def test_triangle_type_equilateral():
    t = Triangle(3, 3, 3)
    assert t.triangle_type() == "equilateral"


def test_triangle_type_isosceles():
    t = Triangle(5, 5, 3)
    assert t.triangle_type() == "isosceles"


def test_triangle_type_nonequilateral():
    t = Triangle(4, 5, 6)
    assert t.triangle_type() == "nonequilateral"


def test_perimeter():
    t = Triangle(3, 4, 5)
    assert t.perimeter() == 12


# Негативные тесты
def test_invalid_triangle():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(1, 2, 3)


def test_negative_side():
    with pytest.raises(IncorrectTriangleSides):
        Triangle(-1, 5, 5)


def test_wrong_type():
    with pytest.raises(IncorrectTriangleSides):
        Triangle("a", 5, 5)

