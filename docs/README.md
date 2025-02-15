# Elliptic Curve Point Addition over a Finite Field

## Elliptic Curve Definition

An elliptic curve over a finite field $\mathbb{F}_p$ (where $p$ is a prime number) is defined by the equation:

$$ y^2 \equiv x^3 + ax + b \pmod{p} $$

where $a, b \in \mathbb{F}_p$ and satisfy the non-singularity condition:

$$ 4a^3 + 27b^2 \not\equiv 0 \pmod{p} $$

## Point Addition

Let $P = (x_1, y_1)$ and $Q = (x_2, y_2)$ be two points on the curve. The addition of these points follows these rules:

### Adding Two Distinct Points ($P \neq Q$)
If $x_1 \neq x_2$, the slope $\lambda$ of the line connecting $P$ and $Q$ is given by:

$$ \lambda = \frac{y_2 - y_1}{x_2 - x_1} \pmod{p} $$

Using modular inversion, this is computed as:

$$ \lambda = (y_2 - y_1) \cdot (x_2 - x_1)^{-1} \pmod{p} $$

The coordinates of the resulting point $R = P + Q = (x_3, y_3)$ are:

$$ x_3 = \lambda^2 - x_1 - x_2 \pmod{p} $$
$$ y_3 = - (y_1 - \lambda (x_1 - x_3)) \pmod{p} $$

### Adding a Point to Itself ($P = Q$)
If $P = Q$, we use the tangent at $P$ to determine the slope:

$$ \lambda = \frac{3x_1^2 + a}{2y_1} \pmod{p} $$

computed as:

$$ \lambda = (3x_1^2 + a) \cdot (2y_1)^{-1} \pmod{p} $$

The new point $R = 2P$ has coordinates:

$$ x_3 = \lambda^2 - 2x_1 \pmod{p} $$
$$ y_3 = - (y_1 - \lambda (x_1 - x_3)) \pmod{p} $$

### Adding a Point to Its Inverse
If $Q = -P$, meaning $x_1 = x_2$ and $y_1 \equiv -y_2 \pmod{p}$, the result is the point at infinity:

$$ P + (-P) = \mathcal{O} $$

## Implementation

The `add_points` function defined at the `Curve` class implements the described behaviour:
```python
def add_points(self, p: Point, q: Point) -> Point:
    if p.inf: return q
    if q.inf: return p

    if p.x != q.x:
        slope = (p.y - q.y) * pow(p.x - q.x, -1, self.modulo)
        x = (pow(slope, 2) - p.x - q.x) % self.modulo
        y = (-(p.y - slope * (p.x - x))) % self.modulo
        return Point(x, y)

    if not ((p.y + q.y) % self.modulo):
        return Point.infinite()

    slope = (3 * pow(p.x, 2) + self.a) * pow(2*p.y, -1, self.modulo)
    x = (pow(slope, 2) - 2 * p.x) % self.modulo
    y = (-(p.y - slope * (p.x - x))) % self.modulo
    return Point(x, y)
```
