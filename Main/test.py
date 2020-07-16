# from datetime import datetime
#
# dictionary_of_dates_on_files = {'2019-12-23': 123, '2018-12-23': 345}
# sorted_dates = sorted(dictionary_of_dates_on_files, key=lambda date: datetime.strptime(date, '%Y-%m-%d'))
#
# print(sorted_dates)
#
# date = '2019-12-23'
# year = int(date[0:4])
# month = int(date[5:7])
# day = int(date[8:10])
# print(year)
# print(month)
# print(day)
# print(datetime(2019, 4, 3, 2).timestamp())

# import os
#
# print(os.environ['output_folder'])
# print(os.environ['prioritize_consistent'])
# print(os.environ['prioritize_new'])
# print(os.environ['only_todays_ips'])
# print(os.environ['eval_data_folder'])
# from inspect import getmembers, isfunction
# import main_modulev3
#
# # This is a test
#
#
# functions_list = [o[0] for o in getmembers(main_modulev3) if isfunction(o[1])]
#
# method_to_call = getattr(main_modulev3, functions_list[1])
# result = method_to_call()
#
updated_entry = {'2': 2}
dictionary = {'2': 1, '3': 3 }

dictionary.update(updated_entry)

print(dictionary)
