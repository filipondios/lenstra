exception NotCoprimes

let rec extended_euclides r_old r_new s_old s_new t_old t_new =
  match r_new with
  | 0L -> (s_old, t_old, r_old)
  | _  ->
    let quotient = Int64.div r_old r_new in
    extended_euclides
      r_new (Int64.sub r_old (Int64.mul quotient r_new))
      s_new (Int64.sub s_old (Int64.mul quotient s_new))
      t_new (Int64.sub t_old (Int64.mul quotient t_new))

let inv_mod (n: int64) (m: int64) =
  let (a, _, mcd) = extended_euclides n m 1L 0L 0L 1L in
  if mcd <> 1L then raise NotCoprimes else a 



type ec_point =
  | Zero
  | ECP of (int64 * int64)


let sum_pts (p: ec_point) (q: ec_point) a n =
  match p, q with
  | Zero, q -> q
  | p, Zero -> p 
  | ECP (px, py), ECP (qx, qy) ->
    if px <> qx then
      let s  = Int64.rem (Int64.mul (Int64.sub py qy) (inv_mod (Int64.sub px qx) n)) n in
      let rx = Int64.rem (Int64.sub (Int64.sub (Int64.mul s s) px) qx) n in
      let ry = Int64.rem (Int64.neg (Int64.add (Int64.mul (Int64.sub rx px) s) py)) n in
      ECP (rx, ry)
    else 
      if py = Int64.neg qy then
        Zero
      else
        let s  = Int64.rem (Int64.mul (Int64.add (Int64.mul (Int64.mul px px) 3L) a) (inv_mod (Int64.mul py 2L) n)) n in
        let rx = Int64.rem (Int64.sub (Int64.sub (Int64.mul s s) px) qx) n in
        let ry = Int64.rem (Int64.neg (Int64.add (Int64.mul (Int64.sub rx px) s) py)) n in
        ECP (rx, ry)


let ecp_to_string p = 
  match p with
  | Zero -> "Zero"
  | ECP (x, y) -> "(" ^ Int64.to_string x ^ ", " ^ Int64.to_string y ^ ")"


let () =
  let (a, _, n) = (2L, 3L, 97L) in
  let p = (17L, 10L) in
  let q = (95L, 31L) in
  ecp_to_string (sum_pts (ECP p) (ECP q) a n) |> print_string
