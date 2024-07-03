empty_str = ''
empty_list = []
empty_dict = {}
empty_int = int()
empty_tupple = ()
empty_set = set()
boolean = False
none_type = None
zero = 0

false_list = [empty_str, empty_list, empty_dict, empty_int, empty_tupple, empty_set, boolean, none_type, zero]
for ele in false_list:
    if ele:
        print(type(ele), True)
    else:
        print(type(ele), False)

