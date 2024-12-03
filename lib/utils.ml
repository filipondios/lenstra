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
