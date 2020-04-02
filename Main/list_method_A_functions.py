from inspect import getmembers, isfunction
import main_modulev3

functions_list = [o[0] for o in getmembers(main_modulev3) if isfunction(o[1])]

running_total = 1
for function in functions_list:
    if function[:21] == 'prioritize_consistent':
        print('Option', running_total, ':', function)
        running_total += 1
