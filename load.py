# this file contains functions for loading and parsing Json file in the
# program.
import os
import re
import json
from pprint import pprint


def get_filename(prompt):
    count = 0
    regex = ".*json"
    while count < 3:
        fn = raw_input(prompt)
        print("input filename is " + fn)
        if (os.path.exists(fn) & bool(re.match(regex, fn))):
            return fn
        print("The file does not exist or not .json file")
        count += 1
    print("Falied 3 times, program ends.")


def read_in(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
        return data


def get_data(prompt):
    fn = get_filename(prompt)
    if(fn):
        data = read_in(fn)
        return data


if __name__ == '__main__':
    data = get_data("filename: ")
    # pprint(data)
    for key in data.keys():
        pprint(key)
