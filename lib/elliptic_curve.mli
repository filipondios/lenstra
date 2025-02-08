type curve = { a : int64; b : int64; field: int64 }
type point = | Point of int64 * int64 | Zero

val is_singular : curve -> bool
val add_points  : point -> point -> curve -> point
val mul_point   : curve -> point -> int64 -> point
