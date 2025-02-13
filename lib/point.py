class Point:
    inf: bool
    x: int
    y: int

    def __init__(self, x, y, inf=False):
        self.inf = inf
        self.x = x
        self.y = y

    def infinite():
        return Point(0, 0, True)
    
    def __str__(self):
        x = hex(self.x)
        y = hex(self.y)
        return '(' + x + ', ' + y + ')'