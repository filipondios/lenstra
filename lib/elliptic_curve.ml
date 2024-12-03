(** A elliptic curve is expressed as y² = x³ + ax + b mod.
    It must satisfy: 16 * (4a³ + 27b²) != 0 *)
type curve = { a : int64; b : int64; field: int64 }

(** A point can be either a coordinate (x,y) or 
    a point at the infinite. *)
type point = | Point of int64 * int64
             | Zero

(** Adds two points P and Q from a elliptic curve y² = x³ + ax + b in the field Zn.
    The field Zn is specified at the record being passed as value. *)
let add_points (p: point) (q: point) ({a = a; b = _; field = n} : curve) =
  match p, q with
  | Zero, q -> q
  | p, Zero -> p 
  | Point (px, py), Point (qx, qy) ->
    if px <> qx then
      let s  = Int64.rem (Int64.mul (Int64.sub py qy) (Utils.inv_mod (Int64.sub px qx) n)) n in
      let rx = Int64.rem (Int64.sub (Int64.sub (Int64.mul s s) px) qx) n in
      let ry = Int64.rem (Int64.neg (Int64.add (Int64.mul (Int64.sub rx px) s) py)) n in
      Point (rx, ry)
    else 
      if py = Int64.neg qy then
        Zero
      else
        let s  = Int64.rem (Int64.mul (Int64.add (Int64.mul (Int64.mul px px) 3L) a) (Utils.inv_mod (Int64.mul py 2L) n)) n in
        let rx = Int64.rem (Int64.sub (Int64.sub (Int64.mul s s) px) qx) n in
        let ry = Int64.rem (Int64.neg (Int64.add (Int64.mul (Int64.sub rx px) s) py)) n in
        Point (rx, ry)
