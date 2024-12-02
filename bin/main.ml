
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

let sum_pts (p: ec_point) (q: ec_point) b n =
  match p, q with
  | Zero, q -> q
  | p, Zero -> p 
  | ECP (xp, yp), ECP (xq, yq) -> 
    if xp <> xq then
      let s  = Int64.rem (Int64.mul (Int64.sub yp yp) (inv_mod (Int64.sub xp xq) n)) n in
      let xr = Int64.rem (Int64.sub (Int64.sub (Int64.mul s s) xp) xq)  n in
      let yr = Int64.rem (Int64.sub yp (Int64.mul s (Int64.sub xp xr))) n in
      ECP (xr, yr)
    else 
      if yp = Int64.neg yq then
        Zero
      else
        let s  = Int64.rem (Int64.div ((Int64.mul xp xp |> Int64.mul xp |> Int64.mul 3L) |> 
          Int64.add b) (inv_mod (Int64.mul yp 2L) n)) n in 
        let xr = Int64.rem (Int64.sub (Int64.sub (Int64.mul s s) xp) xq)  n in
        let yr = Int64.rem (Int64.sub yp (Int64.mul s (Int64.sub xp xr))) n in
        ECP (xr, yr)

let ecp_to_string p = 
  match p with
  | Zero -> "Zero"
  | ECP (x, y) -> "(" ^ Int64.to_string x ^ ", " ^ Int64.to_string y ^ ")"


let () =
  let (_, b, n) = (2L, 3L, 97L) in
  let p = (17L, 10L) in
  let q = (95L, 31L) in
  ecp_to_string (sum_pts (ECP p) (ECP q) b n) |> print_string


(*  
  b = 7
  n = 37
  (xp,yp) = (6,1)
  (xq,yq) = (8,1)
  
  s  = (yp - yq) * inv(xp-xq) = (1 - 1) * inv(...) = 0
  xr = 0 - xp - xq = -6 -8 = -14
  yr = 1 
*)
