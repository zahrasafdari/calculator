from .utils import operators, get_index, find
from .calculation import functions, Function
from math import pi


def tokenize(li):
    #   this function tokenize given list by operators
    #   example:
    #   [ '2+3.4*cos', ['pi/2'] ] -> [ '2','+','3.4','*','cos', ['pi','/','2'] ]

    buffer = ''
    result = []

    def flush_buffer(result, buffer):
        if buffer:
            result.append(buffer)
            buffer = ''
        return (result, buffer)

    for item in li:
        if not isinstance(item, str):
            result, buffer = flush_buffer(result, buffer)
            result.append(item)
        else:
            for i in item:
                if i in operators.keys():
                    result, buffer = flush_buffer(result, buffer)
                    result.append(i)
                else:
                    buffer += i
            result, buffer = flush_buffer(result, buffer)

    return result


def list_multiple_normalize(li):
    #   add '*' token if there is no operation
    #   between a list and it's before object
    #   example: 2(2+5) -  > 2*(2+5) , (3+3)6 -> (3+2)*6
    def condition(e): return isinstance(e, list)

    idx = find(li, condition)
    while idx is not None:
        before = get_index(li, idx-1, None)
        print(before)
        after = get_index(li, idx+1, None)

        if before and before not in operators.keys():
            li.insert(idx, '*')
            idx += 1
        if after and after not in operators.keys():
            li.insert(idx+1, '*')

        idx = find(li, condition, idx+1)

    return li


def function_normalize(li):
    #   check is a item in function list and if yes,
    #   create a Function obj then add it to stack
    #   example:
    #   [ '2' , '+' , 'cos', ['pi','/', '2'] ] -> [ '2' , '+' , Function(cos), "^", ["3.14", "*", "2i"] ]

    result = []
    i = 0
    while i < len(li):
        item = get_index(li, i+1, None)
        if isinstance(item, list) and li[i] in functions.keys():
            result.append(Function(functions[li[i]], item))
            i += 1
        else:
            result.append(li[i])
        i += 1

    return result


def pi_normalize(li):
    #   turn all 'pi' tokens to it's number
    result = []
    for i in li:
        if i == 'pi':
            result.append(str(pi))
        else:
            result.append(i)

    return result


def function_multiple_normalize(li):
    # [ '23pi56picos' ] --> ['23pi56pi', '*', 'cos']
    function_name = ''

    def condition(e):
        for i in functions.keys():
            if isinstance(e, str) and e.endswith(i) and e != i:
                return True
        return False

    idx = find(li, condition)
    while idx is not None:

        for i in functions.keys():
            if li[idx].endswith(i):
                function_name = i
        li[idx] = li[idx][:-len(function_name)]
        li.insert(idx+1, '*')
        li.insert(idx+2, function_name)
        idx = find(li, condition, idx+1)

    return li


def pi_multiple_normalize(li):
    # [ '23pi56pi' ] --> ['23', '*', 'pi', '*', '56', '*', 'pi']

    def condition(e): return bool('pi' in e)

    idx = find(li, condition)
    while idx is not None:
        if li[idx] != 'pi':
            mix = li[idx]
            mix = mix.split('pi')
            mix = "*pi*".join(mix)
            mix = mix.replace('**', '*')
            mix = mix.strip("*")
            del li[idx]
            for i, e in enumerate(tokenize([mix])):
                li.insert(idx+i, e)

        idx = find(li, condition, idx+1)

    return li


def minus_plus_normalize(li):
    # attach - or + to number if there be any in special cases
    # in first of list ['-', '23'] --> ['-1' , '*', '23']
    # in coordinate with another operators ['23', '*', '-', '35'] --> ['32', '*', '-1', '*','35']
    def condition(e): return bool(e == '+' or e == '-')

    idx = find(li, condition)

    while idx is not None:
        before = get_index(li, idx-1, None)

        if not before and li[idx] == '+':
            del li[idx]
            break

        elif ((not before) or (before in operators.keys())) and li[idx] == '-':
            li[idx] = '-1'
            li.insert(idx+1, '*')
            break

        idx = find(li, condition, idx+1)

    return li


def normalize(li):
    li = function_multiple_normalize(li)
    li = pi_multiple_normalize(li)
    li = pi_normalize(li)
    li = function_normalize(li)
    li = minus_plus_normalize(li)
    li = list_multiple_normalize(li)
    print(li)
    return li


# NOTE: this function use walker algorithm with recursion method
def stack_optimizer(li):
    for i in range(len(li)):
        if isinstance(li[i], list):
            li[i] = stack_optimizer(li[i])

    # now we are in the deepest stack
    return normalize(tokenize(li))


def parantes_stack_resolver(s):
    #  this function segmentate given string to
    #  nested arrays (by paranteses) to make solving sentence easier
    #  it's use stack and heap algorithm
    #  Graph of a example :
    #         1 + 2 * ( 4i + (1 / 5 ) + ( 2 ^ 2 * 5i) ) + 1
    #         [ "1+2*", ["4i+" , ["1/5",] , ["2^2*5i"] ], "+1" ]
    #                   ++++++++++++^+++++++++++++++++
    #                            +++^+++
    #                               ^
    #  row1:  -------\                                 /-----
    #  row2:          \------\       /--\             /
    #  row3:                  \-----/    \-----------/
    #  sentences will solve by stack_calculator function from bottom to top

    base_stack = []
    buf = ""
    heap = [
        base_stack,
    ]

    for i in range(len(s)):
        if s[i] == '(':
            if buf:  # if buf exists add this to last stack
                last_stack = heap[len(heap)-1]
                last_stack.append(buf)
                buf = ''
            # add new stack to heap
            heap.append([])

        elif s[i] == ')':
            # if heap have more than one stack (base stack)
            # add ended stack to its parent stack then clear ended stack
            if len(heap) > 1:
                last_stack = heap[len(heap)-1]

                if buf:
                    last_stack.append(buf)
                    buf = ''

                before_stack = heap[len(heap)-2]
                before_stack.append(last_stack)

            heap.pop()

        else:
            buf += s[i]

    if buf:
        base_stack.append(buf)

    return base_stack
