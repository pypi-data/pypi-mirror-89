"""Realization splitres.sh on python"""
import re
import os
import argparse
from statistics import mean


def splitres(file_path, result_dir):
    """
    Function calculates the min, max, average and sum of
    power consumption value and writes this data to a file.

    Args:
        file_path (str): path to the file or directory with files with the messtat-extension.
        result_dir (str): path to the directory in which will be written files.

    Returns:
        return_val (list): list of result which will be written to a file.(need it for testing)
    """
    if os.path.isdir(file_path):
        return_val = []
        for root, _pre_dir, files in os.walk(file_path):
            for file in files:
                if file.endswith('.messtat'):
                    return_val.append(splitres_for_file(root + '/' + file, result_dir))
    elif file_path.endswith('.messtat'):
        return_val = [splitres_for_file(file_path, result_dir)]

    else:
        print("File isn\'t exist!")
        return_val = None
    return return_val


def splitres_for_file(file_path, result_dir):
    """
    Function calculates the min, max, average and sum of
    power consumption value from messtat-file and writes this data to a file.

    Args:
        file_path (str): path to the file with the messtat-extension.
        result_dir (str): path to the directory in which will be written result-files.

    Returns:
        results_list (list): list of result which will be written to a file.(need it for testing)
    """
    data = parser_for_messtatfile(file_path)
    results_list = counting_values(data)
    write_to_file(file_path, result_dir, results_list)
    return results_list


def parser_for_messtatfile(file_name):
    """
    This function parse messtat files and cut from them
    necessary information(info about power consumption in J).

    Args:
        file_name (str): path to the file or directory with files with the messtat-extension.

    Returns:
        data (list): list of values which parsed from messtat file.
    """

    data = []
    for line in open(file_name, 'r').read().split('\n'):
        if 'package' in line:
            data.append(float(re.findall(r'\d+,\d+', line.split(' ')[1])[0].replace(",", ".")))
    return data


def counting_values(data):
    """
    Function that count min, max, average and sum of elements in data list.

    Args:
        data (list): list of values which parsed from messtat file.

    Returns:
        results_list (list): list which contain min, max, average and sum of data elements.
    """
    results_list = []
    results_list.append(min(data))
    results_list.append(max(data))
    results_list.append(mean(data))
    results_list.append(sum(data))
    return results_list


def write_to_file(file_name,result_dir, results_list):
    """
    Function that do writing information about power consumption and
     name of a file, which was parsed, to a file.

    Args:
        file_name (str): path to the file or directory with files with the messtat-extension.
        results_list (list): list which contain min, max, average and sum of data elements.
        result_dir (str): path ro the directory in which will be written files.

    Returns:
        None
    """
    out_file_name = str(result_dir + "/messtat_" + os.path.basename(file_name) + ".spliter")

    output_file = open(out_file_name, "a+")
    output_file.write(f'{file_name}\n'
                      f'Min: {results_list[0]}\n'
                      f'Max: {results_list[1]}\n'
                      f'Avg: {results_list[2]}\n'
                      f'Sum: {results_list[3]}\n\n')
    output_file.close()


def check_exist_dir(dir_name):
    """
    This function check result-directory, if it's doesn't exist function create that directory.

    Args:
        dir_name (str): name of directory in which we want write our files.

    Returns:
        dir_name (str): return name of directory in which files will be written.
    """
    if os.path.exists(dir_name) != 1:
        os.mkdir(dir_name)
    return dir_name


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='file_path', nargs='?',
                        help='Specifies the path to a file or directory '
                             'containing files with the required extension')
    parser.add_argument(dest='result_path', nargs='?', default='result',
                        help='Specifies the path to directory in which would '
                             'writting the spliter-files. By default it will be "result"')
    args = parser.parse_args()

    if args.file_path:
        path_name = os.path.abspath(args.file_path)
        DIR_NAME = str(args.result_path)
        check_exist_dir(DIR_NAME)
        splitres(path_name, DIR_NAME)
