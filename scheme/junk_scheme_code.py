#make call frame implementation, early (and successful) attempt
        frame = Frame(self)
        checked_parameter_list = []
        number_of_unique_arguments = 0
        for parameter in vals:
            if not parameter in checked_parameter_list:
                checked_parameter_list.append(parameter)
                number_of_unique_arguments += 1
        assert len(formals) == number_of_unique_arguments, 'Uneven number of arguments and formal parameters' 
        
        curr_formal = formals
        curr_vals = vals
        while curr_formal.second != nil:
            frame.define(curr_formal.first, curr_vals.first)
            curr_formal = curr_formal.second
            curr_vals = curr_vals.second
        frame.define(curr_formal.first, curr_vals.first)
        return frame

#count-change scheme function implementaion recursive call

        ((>= total (car denoms))
            (+ (count-change total (cdr denoms) max-coins) (count-change (- total (car denoms)) denoms (- max-coins 1))))
        (else (count-change total (cdr denoms) max-coins))))

(define (count-change total denoms max-coins)
  (cond 
        ((= total 0) 
            1)
        ((or (= max-coins 0)(< total 0))
            0)
        ((null? denoms)
            0)
        (else
            (+ (count-change (- total (car denoms)) denoms (- max-coins 1)) (count-change total (cdr denoms) max-coins)))
))