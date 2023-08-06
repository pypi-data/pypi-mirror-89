from datetime import datetime

"""
Description:
Function takes 2 dictionaries with times and abbreviations. Returns list with calculated time difference.
"""


def count_time(start, end):
    result = []
    for abbr, start_time in start.items():
        end_time = end.get(abbr)
        try:
            if not end_time:
                raise ValueError("\n--- Can't find '{}' in 'end' dict  --- \n".format(abbr))
        except ValueError as err:
            print(err)
            continue
        d1 = datetime.strptime(end_time, '%Y-%m-%d_%H:%M:%S.%f')
        d2 = datetime.strptime(start_time, '%Y-%m-%d_%H:%M:%S.%f')
        time = d1 - d2
        result.append({"abbr": abbr, "time": str(time)[:-3]})
    return result
