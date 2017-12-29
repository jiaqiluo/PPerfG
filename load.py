import os
import re
import json
from pprint import pprint
from tree import Node


def get_filename(prompt):
    """ask for the name of a .json file

    Arg:
        prompt(string): the specific question showing to the user

    Return:
        string: the .json filename
    """
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
    """open the target file and read its conetent in

    Arg:
        filename(string): the name of the .json file to be opend

    Return:
        list: a list which contains everything readed from the file
    """
    with open(filename) as data_file:
        data = json.load(data_file)
        return data


def get_data(prompt):
    """returns the content of a .json file

    Arg:
        prompt(string): the specific question showing to the user

    Return:
        list: a list which contains everything readed from the file
    """
    fn = get_filename(prompt)
    if (fn):
        data = read_in(fn)
        return data


if __name__ == '__main__':
    # data = get_data("filename: ")
    data = read_in("sample1.json")
    for key in data.keys():
        pprint(key)
