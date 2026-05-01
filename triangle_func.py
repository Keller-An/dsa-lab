class IncorrectTriangleSides(Exception):
    """Исключение для некорректных сторон треугольника"""
    pass

def get_triangle_type(a, b, c):
    if not all(isinstance(x, (int, float)) for x in [a, b, c]):
        raise IncorrectTriangleSides("Все стороны должны быть числами")
    
    if a <= 0 or b <= 0 or c <= 0:
        raise IncorrectTriangleSides("Длины сторон должны быть положительными числами")
    
    #проверка неравенства треугольника
    if a + b <= c or a + c <= b or b + c <= a:
        raise IncorrectTriangleSides("Стороны не образуют треугольник")
    
    #тип треугольника
    if a == b == c:
        return "equilateral"
    elif a == b or a == c or b == c:
        return "isosceles"
    else:
        return "nonequilateral"
    
