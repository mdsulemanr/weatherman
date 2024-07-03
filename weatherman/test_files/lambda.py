def cub(my_func, iterable):
    result = []
    for item in iterable:
        cubbed = my_func(item)
        result.append(cubbed)
    return result


my_list = [1, 2, 3]

print(cub(lambda x: x ** 3, my_list))

square = lambda x: x ** 2
print(square(4))
