(** A elliptic curve is expressed as y² = x³ + ax + b mod.
    It must satisfy: 16 * (4a³ + 27b²) != 0 *)
type curve = { a : int64; b : int64; field: int64 }

(** A point can be either a coordinate (x,y) or 
    a point at the infinite. *)
type point = | Point of int64 * int64 | Zero

(** Adds two points P and Q from a elliptic curve y² = x³ + ax + b in the field Zn.
    The field Zn is specified at the record being passed as value. *)
val add_points : point -> point -> curve -> point
