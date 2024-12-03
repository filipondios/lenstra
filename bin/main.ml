open Lenstra.Elliptic_curve 

let ex_curve : curve = 
  { a = 2L;
    b = 3L;
    field = 97L }

let p : point = Point (17L, 10L)
let q : point = Point (95L, 31L)


let string_from_point (p: point) =
  match p with
  | Zero -> "Zero"
  | Point (x,y) -> "(" ^ (Int64.to_string x) ^ "," ^ (Int64.to_string y) ^ ")"


let () = 
  let r = add_points p q ex_curve in
    (string_from_point p) ^ " + " ^
    (string_from_point q) ^ " = " ^
    (string_from_point r) |> print_endline

