import os

def read_token_in_line(line):
    # go through each line and get all the tokens separated
    # if it is a space or a line terminator, it will be ignored

    # if the ( char is met, this means the expression has started, it requires a matching
    # ).  And the presence of ( actually will impact the meaning of the tokens:
    # (- -1 2):  first - is an operator and should be written down alone
    # second - is a sign and should be kept together with the number.
    tokens = []
    token = ''
    last_token = ''
    
    for x in line:
        if x == '(' or x == '+' or x == '*' or x == '/':
            token = x
            tokens.append(token)
            last_token = token
            token = ''
        elif x == ')':
            if token != '':
                tokens.append(token)
            
            tokens.append(x)
            token = ''
            last_token = x
        elif x == '-':
            if last_token == '(':
                # last token is (, this is an operator
                token = x
                tokens.append(token)
                last_token = token
                token = ''
            else:
                # can be ignored, this - should be kept
                token = token + x
        else:
            # non-space and end of line, append to the token
            if (not x.isspace()) and x != os.linesep:
                token = token + x
            else:
                if token != '':
                    tokens.append(token)
                    last_token = token
                    token = ''

    return tokens

def is_numeric(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def lookup_value_in_env(key, environment):
    # print 'looking up value...', key, '...in......', environment
    env = environment
    while not key in env:
        env = env['parent']

    return env[key]

def save_value_into_env(key, value, environment):
    environment[key] = value

# index to start points to the next block of expression after the specified position
# exp = (define i (x y z) (+ ....)) call get_next_expression(exp, 3) will get (x y z)
# exp = (set ac (+ (* ac 10) (* ac 20))) call get_next_expression(exp, 3) will get (+ (*ac 10) (*ac 20))
# exp = (+ (* 10 10) (* 20 20)) call next_expression = get_next_expression(exp, 2) will get (* 10 10).
#       after that, call get_next_expression(exp, 2 + len(next_expression)) will get (* 20 20)
# exp = (+ 10 10) call get...(exp, 2) will get 10
# this means, index_to_start points to the start of the next expression that you wish to get
# the next expression either starts with a (, or not a (, which can be any variable names or integer constants
# if the next expression does not start with (, it should be directly be returned, this is not a function call
# if the next expression starts with (, the embedded ( () ( () ())) should be fully retrieved by counting
#    numbers of left parenthesis and right parenthesis, if rp_encountered catches up with lp_encountered
#    it completes an operator (either primitive or user defined)
def get_next_expression(expression, index_to_start):
    # print 'GET NEXT EXPRESSION FOR ..', expression, ' FROM ', index_to_start
    # gets the next expression and put them into a list: [(, *, ac 7 )]
    lp_encountered = 0
    rp_encountered = 0

    # if index is put at the end of the list, return an empty list
    if index_to_start == len(expression) - 1:
        return []

    # (* 10 ()) type of expression, return directly if not started with (
    if expression[index_to_start] != '(':
        return expression[index_to_start:index_to_start + 1]

    # if started with (, decode it with lots of complexity...due to embedded structure
    for idx in range(index_to_start, len(expression)):
        if expression[idx] == '(':
            lp_encountered += 1

        if expression[idx] == ')':
            rp_encountered += 1

            if lp_encountered == rp_encountered:
                # (* (* a 8) (* b 9))
                # (set ac (* a 9)) -> (* a 9) should be returned
                return expression[index_to_start:idx + 1]
            elif lp_encountered < rp_encountered:
                # (set ac 7) ?
                # in this situation, only rp is counted, and lp is zero.
                # so 7 should be returned.
                return expression[index_to_start:index_to_start + 1]

# evaluate function calls itself recursively to evaluate all the expressions it contain
# some evaluations return values, some not (e.g. define / set / etc...)
# although the interpreter is supposed to deal with integer calculations,
# none of the strings were converted into integer form during the processes.
# because the Python built-in function eval() is used to perform primitive operations.
# even the eval() results are converted back to strings, because otherwise int and string mixed operations
# are not supported somewhere (e.g. 10+'abc'), even the eval() function won't be able to process it.
def evaluate(expression, environment):
    # print 'evaluate   ', expression, '   in   ', environment
    # recursively evaluate the expressions
    if expression[0] == '(':
        operator = expression[1]

        if operator in ['+', '-', '*', '/', '=', '<', '>', '<=', '>=']:
            # gets first expression
            first_expression = get_next_expression(expression, 2)
            first_value = evaluate(first_expression, environment)
            # print 'FIRST-VAL=', first_value, ' FIRST-EXP=', first_expression
            
            # gets second expression
            second_expression = get_next_expression(expression, 2 + len(first_expression))
            # print second_expression
            second_value = evaluate(second_expression, environment)
            # print second_value
            # print 'SECOND-VAL=', second_value, ' SECOND-EXP=', second_expression

            # eval using == instead of =
            if operator == '=':
                operator = '=='

            print 'eval:  ', first_value + operator + second_value  # , ' = ', result

            result = str(eval(first_value + operator + second_value))
            
            return result
        elif operator == 'define':
            # (define g (x y z) (* (+ x y) z))
            function_name = expression[2]
            formal_parameters = get_next_expression(expression, 3)
            # print 'FORMAL PARAM=', formal_parameters
            function_body = get_next_expression(expression, 3 + len(formal_parameters))
            # print 'FUNCTION BODY=', function_body
            save_value_into_env(function_name, formal_parameters + function_body, environment)

            # print environment
        elif operator == 'set':
            name = expression[2]
            # gets the next expression
            next_expression = get_next_expression(expression, 3)
            # print 'NEXT EXP DURING SET=', next_expression

            # evaluate the expression
            value = evaluate(next_expression, environment)
            print 'set var ', name, ' = ', value
            return save_value_into_env(name, value, environment)
        elif operator == 'begin':
            next_expression = []
            result = ''
            idx = 2
            next_expression = get_next_expression(expression, idx)
            # print 'NEXT EXPR=', next_expression
            
            while len(next_expression) > 0:
                result = evaluate(next_expression, environment)
                idx += len(next_expression)
                next_expression = get_next_expression(expression, idx)
                # print 'NEXT EXPR=', next_expression
            
            # return the last evaluated expression
            return result
        elif operator == 'if':
            condition_expression = get_next_expression(expression, 2)
            if_statement = get_next_expression(expression, 2 + len(condition_expression))
            else_statement = get_next_expression(expression, 2 + len(condition_expression) + len(if_statement))

            result = evaluate(condition_expression, environment)
            
            if result == 'True':
                return evaluate(if_statement, environment)
            else:
                return evaluate(else_statement, environment)
        else:
            # function call!
            # print 'Function call!'
            function_name = operator
            function = lookup_value_in_env(function_name, environment)
            # print 'FUNCTION=', function

            formal_parameters = get_next_expression(function, 0)
            # print 'FORMAL-PARAM=', formal_parameters

            function_body = get_next_expression(function, len(formal_parameters))
            # print 'FUNCTION-BODY', function_body

            # create a new environment
            function_env = {}
            function_env['parent'] = environment

            # stuff formal parameter into new environment
            # (g ac 10 10), value starts from index 2
            
            # BUT, every place that a variable appears, it could be an expression
            # SO, (g ac 10 10) can be (g (+ ac 10) 10 100)
            # get the parameter values directly is not correct.  it should be evaluated first!
            # Applicative Order will evaluate all the sub-expressions first, then invoke the
            # procedure.  Normal Order will fully expand the procedure call first, then evaluate
            # the formal parameters.
            value_expression_idx = 2
            for param in formal_parameters:
                if param != '(' and param != ')':
                    parameter_value_expression = get_next_expression(expression, value_expression_idx)
                    value_expression_idx += len(parameter_value_expression)
                    # save_value_into_env(param, evaluate([expression[value_expression_idx]], environment), function_env)
                    save_value_into_env(param, evaluate(parameter_value_expression, environment), function_env)

            # print 'FUNCTION-ENV', function_env
            
            # evaluate function with new environment
            return evaluate(function_body, function_env)
    else:
        # if is primitive
        if is_numeric(expression[0]):
            return expression[0]
        else:
            return lookup_value_in_env(expression[0], environment)

# main entry
def interpret(fpath):
    # this method reads file contents line by line
    # current assumption is, each line contains one completed expression
    # 
    # the tokens include:
    # ( and )
    # primitive integers: 0, -100, 100
    # primitive operators: +, -, *, /, =
    # keywords: set, def, if, begin
    # spaces are not included and should be treated as separators (end of token)

    parent_env = {}
    parent_env['parent'] = None

    with open(fpath, 'r') as f:
        for line in f:
            print line
            # the line below runs ok on windows:
            # if len(line) > 0 and line != '\n':
            # but it won't run on mac, because the empty line read is \r\n instead of \n
            # the file first.spy.py is created on windows, so it is having both \r\n as line terminator
            
            # win: CRLF
            # unix: LF
            # mac: CR (Really?)  os.linesep is '\n'
            
            # use file first.spy.py, you get: first.spy.py: ASCII text, with CRLF line terminators
            # create a new text file with mac and file it, you get: abc: ASCII text
            # so I'm thinking python maybe have a system defined end-of-line / terminator...
            # if you set the file format in vi by using: set ff=unix, it will work as well I think
            
            # but, it is said that python conver the line terminator into \n anyways, so I don't know 
            # why in my case it is still \r\n?
            
            # well, MUST NOTICE: even the OS treat the newline char in certain ways.  Handling files
            # created in another OS is a DIFFERENT STORY.  It is better to recognize the differences.
            if len(line) > 0 and line != os.linesep:
                tokens = read_token_in_line(line)
                print 'input=', line.replace(os.linesep, '')
                value = evaluate(tokens, parent_env)
                print 'output=', value

    # evaluation()
    
path = "first.spy.py"
interpret(path)

# this is just a test
with open('abc', 'r') as fs:
    for line in fs:
        print line
