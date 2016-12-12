(set ac    7)
ac
(- ac -8   )
(+ 10 (+ 10 10))
(+ ac (+ ac 10))
(set ac (+ (* ac 10) (* ac 20)))
(* ac 23)
(/ ac 100)

(define g (x y z) (* (+ x y) z))
(g ac 10 10)

(define h (x y z) (+ 10 (g x y z)))
(h ac 10 10)

(define i (x y z) (+ (g x y z) 10))
(i ac 10 10)

(define j () (+ 10 10))
(j)


(begin (define k (x y z) (* (+ x y) z)) (k 1 2 3))

(if (= 3 3) (* 10 10) (+ 10 10))

(if (= 3 4) (* 10 10) (+ 10 10))

(if (< 3 4) (* 10 10) (+ 10 10))

(if (> 3 4) (* 10 10) (+ 10 10))

(if (>= 3 4) (* 10 10) (+ 10 10))

(if (<= 3 4) (* 10 10) (+ 10 10))

(if (<= 4 4) (* 10 10) (+ 10 10))

(define fact (n) (if (= n 1) 1 (* n (fact (- n 1)) )))

(fact 5)