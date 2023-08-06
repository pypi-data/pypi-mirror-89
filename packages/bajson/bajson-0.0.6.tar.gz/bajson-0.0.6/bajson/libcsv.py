import json
import csv

from bajson.exceptions import InvalidParameterException, MissingParameterException


def object_to_csv_row(object, header, delim):
    row = []
    for col in header:
        row.append(object.get(col, ""))

    return delim.join(row)


def csv_row_to_object(row, header, delim):
    row_items = row.split(delim)
    obj = {}
    for i, col in enumerate(header):
        if row_items[i]:
            obj[col] = row_items[i]

    return obj


def find_csv_headers_from_list(json_list, prefix, header=set()):
    for i, value in enumerate(json_list):
        key = f"{i}"
        key_tree = []
        key_tree.extend(prefix)
        key_tree.append(key)
        if type(value) is dict:
            find_csv_headers_from_dict(value, key_tree, header=header)
        elif type(value) is list:
            find_csv_headers_from_list(value, key_tree, header=header)
        else:
            header.add(".".join(key_tree))


def find_csv_headers_from_dict(json_obj, prefix=[], header=set()):
    for item in json_obj.items():
        key = str(item[0])
        value = item[1]
        key_tree = []
        key_tree.extend(prefix)
        key_tree.append(key)
        if type(value) is dict:
            find_csv_headers_from_dict(value, key_tree, header=header)
        elif type(value) is list:
            find_csv_headers_from_list(value, key_tree, header=header)
        else:
            header.add(".".join(key_tree))
        value = item[1]


def create_row(obj, header):
    row_dict = {}
    for col in header:
        cols = col.split('.')
        val = None
        o = obj
        for c in cols:
            try:
                if c.isnumeric():
                    c = int(c)
                o = o[c]
            except:
                o = None
        row_dict[col] = o

    return row_dict


def row_to_obj(row, header):
    obj = {}
    for i, head in enumerate(header):
        if row[i]:
            temp = obj
            for h in head:
                if h not in temp.keys():
                    if h == head[-1]:
                        temp[h] = row[i]
                    else:
                        temp[h] = {}
                        temp = temp[h]
                else:
                    temp = temp[h]
    return obj

def json_to_csv(input_file=None, output_file=None, auto_id=False, header=None):
    if input_file == None or output_file == None:
        raise MissingParameterException(
            "parameters input_file and output_file must not be None")

    with open(input_file, "r") as input_file:
        input_json = json.load(input_file)
        if type(input_json) is not list:
            raise InvalidParameterException(
                "Input json must be list structure")
        header = set()
        for obj in input_json:
            find_csv_headers_from_dict(obj, header=header)

        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = sorted(list(header))
            writer = csv.DictWriter(csvfile,
                                    fieldnames=fieldnames,
                                    delimiter=";")
            writer.writeheader()
            for obj in input_json:
                row_dict = create_row(obj, header)
                writer.writerow(row_dict)


def csv_to_json(input_file=None,
                output_file=None,
                delimiter=';',
                header=None):
    if input_file == None or output_file == None:
        raise MissingParameterException(
            "parameters input_file and output_file must not be None")

    line_number = 0
    with open(input_file, "r") as input_file:
        csv_reader = csv.reader(input_file, delimiter=delimiter)
        result = []
        for row in csv_reader:
            if line_number == 0:
                header = list(map(lambda c: c.split('.'), row))
                line_number += 1
            else:
                json_obj = row_to_obj(row, header)
                result.append(json_obj)
        
        with open(output_file, "w") as output_file:
            json.dump(result, output_file, indent=2)