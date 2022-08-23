def func_sum(n=None):
    count = 0
    if n is None:
        print(count)
        return

    def first_func(x):
        nonlocal count
        count += x
        return first_func

    return first_func


func_sum(5)()
# > 5
func_sum(5)(90)()
# > 95
func_sum(5)(90)(-10)()
# > 85
