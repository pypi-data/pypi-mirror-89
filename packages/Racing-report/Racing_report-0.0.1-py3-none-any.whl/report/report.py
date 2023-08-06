import re
import operator


def read_logs(path):
    f = open(path, 'r')
    file_data = f.read()
    f.close()
    score_list = file_data.split("\n")
    return score_list


def parse_logs(score_list):
    result = {}
    for lap in score_list:
        abbr = lap[:3]
        time = lap[3:]
        result.update({abbr: time})
    return result


def parse_abbr(abbr_list):
    result = {}
    for lap in abbr_list:
        abbr = lap[:3]
        car = lap[3:]
        result.update({abbr: car})
    return result


def print_report(data, order, driver=None):
    data.sort(key=operator.itemgetter("time"))
    if order == "desc":
        data = data[::-1]
    output(data, order, driver)


def output(output_list, order, driver):
    for elem in output_list:
        index = output_list.index(elem) + 1
        name = elem["name"]
        car = elem["car"]
        time = elem["time"]
        if "-" in time:
            print("Wrong time data in '{0} {1}'".format(name, car))
            continue
        if driver:
            if driver == name:
                print("{0}. {1} | {2} | {3}".format(index, name, car, time))
        else:
            if order == "desc":
                if index == len(output_list) - 15:
                    print("-" * 63)
            else:
                if index == 16:
                    print("-" * 63)
            print("{0:2}. {1:17} | {2:25} | {3:25}".format(index, name, car, time))


def built_report(time_dict, abbr_list):
    for lap in time_dict:
        abbr = lap["abbr"]
        string = abbr_list.get(abbr)
        driver = re.split(r'_', string)  # split return list like ['', 'Lance Stroll', 'WILLIAMS MERCEDES']
        lap.update({"name": driver[1], "car": driver[2]})
    return time_dict
