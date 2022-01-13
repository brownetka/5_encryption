import time


def time_t(f, *args):
    start_time = time.time()
    result = f(*args)
    finish_time = time.time()
    print(f"Время работы функции: {round(finish_time - start_time,2)}сек.")
    return result


def time_tracker(f):

    def wrapper(*args):
        start_time = time.time()
        result = f(*args)
        finish_time = time.time()
        print(f"Время работы функции: {round(finish_time - start_time, 2)}сек.")
        return result

    return wrapper


@time_tracker
def func(a, max_range=10000):
    total = 0
    for i in range(1, max_range):
        total += a ** i
    return total


func(5, 15000)