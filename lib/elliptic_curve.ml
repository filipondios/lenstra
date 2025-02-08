
let ( +^ ) = Int64.add
let ( -^ ) = Int64.sub
let ( *^ ) = Int64.mul
let ( %^ ) = Int64.rem
let ( &^ ) = Int64.logand
let ( <<^ ) = Int64.shift_left


(** Elliptic curves are defined as the set of points (x,y) which 
    satisfy the elliptic curve equation of the form:  
    y² = x³ + ax + b. **)
type curve = { a : int64; b : int64; field: int64 }


(** A point can be either a coordinate (x,y) in a Two-Dimensional 
    Space or a point at the "infinite" (also called 0), working as 
    the identity element of the elliptic curve arithmetic. **)
type point = | Point of int64 * int64
             | Zero


(** Tests if a elliptic curve y² = x³ + ax + b satisfies 
    4a³ + 27b² != 0 **) 
let is_singular ({a = a; b = b; field = n} : curve) =
  (((4L*^a*^a*^a) +^ (27L*^b*^b)) %^ n) == 0L


(** Adds two points P and Q from a elliptic curve y² = x³ + ax + b in the field Zn.
    The field Zn is specified at the record being passed as value. *)


(** Adds two points (P, Q) that are supposedly contained in a  
    elliptic curve C(a, b, n), being n the field. **)
let add_points (p: point) (q: point) ({a = a; b = _; field = n} : curve) =
  match p, q with
  | Zero, q -> q
  | p, Zero -> p 
  | Point (px, py), Point (qx, qy) ->
    if px <> qx then
      (* Different points *)
      let s = ((py -^ qy) *^ (Utils.inv_mod (px -^ qx) n)) %^ n in
      let x = (s*^s -^ px -^ qx) %^ n in
      let y = (Int64.neg (py -^ s *^ (px -^ x))) %^ n in
      Point (x, y)
    else 
      (* Symetrical points *)
      if (py +^ qy) %^ n == 0L then
        Zero
      else
        (* Other case: Same point *)
        let s = ((3L*^px*^px +^ a) *^ (Utils.inv_mod (2L*^py) n)) %^ n in
        let x = (s*^s -^ 2L *^ px) %^ n in
        let y = (Int64.neg (py -^ s *^ (px -^ x))) %^ n in
        Point (x, y)


(** The mulPoint' and mulPoint functions calculate the multiplication 
    between a scalar and an elliptic curve point. mulPoint' is the 
    recursive version. 
    
    For calculating f.e 1000 times P, we do not need to calculate 1000 
    sums for P. Because of associativity, we can calculate 1000 times P 
    as 512P + 256P + 128P + 64P + 32P + 8P via its binary representation 
    doubling the point P. **)
let rec mul_point' curve point n bit_mask acc = 
  if bit_mask > n then
    acc
  else 
    let double = add_points point point curve in
    let mask   = bit_mask <<^ 1  in

    if (n &^ bit_mask) <> 0L then
      mul_point' curve double n mask (add_points point acc curve)
    else mul_point' curve double n mask acc      

let mul_point curve point n = 
  mul_point' curve point n 1L Zero
