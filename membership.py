def triangular_membership(x, a, b, c):
    # Triangular membership for middle ranges.
    if x <= a or x >= c:
        return 0.0
    if x == b:
        return 1.0
    if a < x < b:
        return (x - a) / (b - a)
    return (c - x) / (c - b)

def trapezoidal_membership(x, a, b, c, d):
    # Trapezoidal membership for edge ranges (shoulders).
    if b <= x <= c:
        return 1.0
    if a == b and x < a:     
        return 1.0
    if c == d and x > d:      
        return 1.0
    if x <= a or x >= d:
        return 0.0
    if a < x < b:
        return (x - a) / (b - a)
    return (d - x) / (d - c)