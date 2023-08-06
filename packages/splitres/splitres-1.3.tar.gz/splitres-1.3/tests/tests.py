"""Testing with pytest"""

import src.splitres as split
import os
import shutil
from unittest.mock import patch
import sys


def setup_module(module):
    global FILE_1
    global FILE_2
    global FILE_3
    global EMPTY_FILE
    global DIR
    global PERM_DEN_DIR
    global PERM_DEN_FILE
    global DIR_2

    DIR = 'test_dir'
    DIR_2 = 'test_dir_2'
    FILE_1 = os.path.join(DIR, 'test1.messtat')
    FILE_2 = os.path.join(DIR, 'test2.messtat')
    FILE_3 = os.path.join(DIR, 'test3.messtat')
    EMPTY_FILE = os.path.join(DIR, 'empty.messtat')
    PERM_DEN_DIR = os.path.join(DIR, 'not_write_dir')
    PERM_DEN_FILE = os.path.join(DIR_2, 'perm_err.messtat')

    os.mkdir(DIR)
    os.mkdir(PERM_DEN_DIR)
    os.mkdir(DIR_2)
    os.chmod(PERM_DEN_DIR, 0)

    with open(PERM_DEN_FILE, 'w'):
        pass

    os.chmod(PERM_DEN_FILE, 0)

    text1 = 'package-1: 51,836720J	dram: 8,094236J\n' \
            'package-0: 68,425240J	dram: 8,174866J\n' \
            '4,44	0,00	5,88	5,88	2,35\n' \
            'package-1: 42,836865J	dram: 7,959978J\n' \
            'package-0: 56,918372J	dram: 8,001456J\n' \
            '1,37	0,00	0,00	0,00	0,00\n'

    text2 = 'package-1: 43,681163J	dram: 7,947218J\n' \
            'package-0: 52,444812J	dram: 8,068944J\n' \
            '1,30	0,00	0,00	0,99	0,00\n' \
            'package-1: 42,841015J	dram: 7,921116J\n' \
            'package-0: 56,222818J	dram: 8,190028J\n' \
            '1,40	0,98	0,00	0,00	0,00\n' \
            'package-1: 167,287719J	dram: 12,783380J\n' \
            'package-0: 159,156453J	dram: 13,485451J\n' \
            '42,99	87,00	83,00	83,00	82,83\n'
    text3 = 'package-1: 198,265667J	dram: 14,127928J\n' \
            'package-0: 178,879059J	dram: 14,898742J\n' \
            '51,41	33,67	68,63	100,00	100,00\n' \
            'package-1: 198,888102J	dram: 14,104994J\n' \
            'package-0: 178,416352J	dram: 14,885095J\n'\
            '51,44	0,00	0,00	100,00	100,00\n' \
            'package-1: 198,785196J	dram: 14,178663J\n' \
            'package-0: 179,179901J	dram: 14,945790J\n' \
            '51,43	1,01	0,00	85,29	58,42\n' \
            'package-1: 197,353255J	dram: 13,970721J\n' \
            'package-0: 178,551606J	dram: 14,769733J\n' \
            '51,44	0,00	0,00	15,84	43,56\n' \
            'package-1: 199,229043J	dram: 14,228219J\n' \
            'package-0: 179,529569J	dram: 15,028548J\n' \
            '51,45	0,00	0,00	0,00	0,00\n' \
            'package-1: 198,132672J	dram: 14,107212J\n' \
            'package-0: 179,313994J	dram: 14,880428J\n' \
            '51,42	0,00	10,89	0,00	0,00\n' \
            'package-1: 200,303259J	dram: 14,569823J\n' \
            'package-0: 181,665368J	dram: 15,319860J\n' \
            '51,18	2,06	10,00	0,00	0,00\n' \
            'package-1: 200,515051J	dram: 15,946578J\n' \
            'package-0: 185,860120J	dram: 16,409235J\n' \
            '50,06	0,00	0,00	0,00	0,00\n' \
            'package-1: 198,124188J	dram: 14,178572J\n' \
            'package-0: 177,684237J	dram: 14,618844J\n' \
            '50,06	0,00	0,00	0,00	0,00\n'

    with open(FILE_1, 'w') as file:
        file.write(text1)

    with open(FILE_2, 'w') as file:
        file.write(text2)

    with open(FILE_3, 'w') as file:
        file.write(text3)

    with open(EMPTY_FILE, 'w'):
        pass


def teardown_module(module):
    os.chmod(PERM_DEN_DIR, 777)
    os.chmod(PERM_DEN_FILE, 777)
    shutil.rmtree(DIR)
    shutil.rmtree(DIR_2)
    os.remove('messtat_.spliter')


def test_parser_for_messtatfile():
    expect_1 = (0, [51.83672, 68.42524, 42.836865, 56.918372])
    expect_2 = (0, [43.681163, 52.444812, 42.841015, 56.222818, 167.287719, 159.156453])
    expect_3 = (0, [198.265667, 178.879059, 198.888102, 178.416352, 198.785196, 179.179901,
                197.353255, 178.551606, 199.229043, 179.529569, 198.132672, 179.313994,
                200.303259, 181.665368, 200.515051, 185.86012, 198.124188, 177.684237])
    expect_4 = (0, [])

    path_5 = PERM_DEN_FILE
    path_6 = os.path.join('test', 'test', 'test', 'test_write_to_file_1.messtat')

    expect_5 = (-1, "[Errno 13] Permission denied: 'test_dir_2/perm_err.messtat'")
    expect_6 = (-1, "[Errno 2] No such file or directory: "
                    "'test/test/test/test_write_to_file_1.messtat'")

    assert split.parser_for_messtatfile(FILE_1) == expect_1
    assert split.parser_for_messtatfile(FILE_2) == expect_2
    assert split.parser_for_messtatfile(FILE_3) == expect_3
    assert split.parser_for_messtatfile(EMPTY_FILE) == expect_4
    assert split.parser_for_messtatfile(path_5) == expect_5
    assert split.parser_for_messtatfile(path_6) == expect_6


def test_counting_values():
    expect_1 = {
        'Min': 42.836865,
        'Max': 68.42524,
        'Mean': 55.00429925,
        'Sum': 220.017197
    }
    expect_2 = {
        'Min': 42.841015,
        'Max': 167.287719,
        'Mean': 86.93899666666667,
        'Sum': 521.6339800000001
    }
    expect_3 = {
        'Min': 177.684237,
        'Max': 200.515051,
        'Mean': 189.37092438888888,
        'Sum': 3408.676639,
    }
    expect_4 = {}

    exp_err = 0

    data_empty = []
    data_incorrect = 123
    expect_empty = (0, {})
    expect_incorrect = (-1, "'int' object is not iterable")

    assert split.counting_values(data_empty) == expect_empty
    assert split.counting_values(data_incorrect) == expect_incorrect

    _, data = split.parser_for_messtatfile(FILE_1)
    assert split.counting_values(data) == (exp_err, expect_1)

    _, data = split.parser_for_messtatfile(FILE_2)
    assert split.counting_values(data) == (exp_err, expect_2)

    _, data = split.parser_for_messtatfile(FILE_3)
    assert split.counting_values(data) == (exp_err, expect_3)

    _, data = split.parser_for_messtatfile(EMPTY_FILE)
    assert split.counting_values(data) == (exp_err, expect_4)


def test_splitres():
    expect_1 = {
        'Min': 42.836865,
        'Max': 68.42524,
        'Mean': 55.00429925,
        'Sum': 220.017197
    }
    expect_2 = {
        'Min': 42.841015,
        'Max': 167.287719,
        'Mean': 86.93899666666667,
        'Sum': 521.6339800000001
    }
    expect_3 = {
        'Min': 177.684237,
        'Max': 200.515051,
        'Mean': 189.37092438888888,
        'Sum': 3408.676639,
    }

    expect = [expect_3, expect_2, expect_1, {}]

    with patch('os.path.isdir', return_value=False), \
         patch('builtins.print') as mm:
        split.splitres('not exist file', DIR)

        mm.assert_called_once_with('File isn\'t exist!', file=sys.stderr)

    assert split.splitres(FILE_1, DIR) == [expect_1]
    assert split.splitres(FILE_2, DIR) == [expect_2]
    assert split.splitres(FILE_3, DIR) == [expect_3]

    data = split.splitres(DIR, DIR)
    for item in data:
        assert item in expect


def test_splitres_error():
    file_path_1 = EMPTY_FILE
    result_dir_1 = os.path.join('test', 'test', 'test')
    expect_1 = None

    file_path_2 = DIR_2
    result_dir_2 = DIR
    expect_2 = []

    assert split.splitres(file_path_1, result_dir_1) == expect_1
    assert split.splitres(file_path_2, result_dir_2) == expect_2


def test_check_exist_dir():
    exist_dir = DIR
    not_exist_dir = os.path.join(DIR, 'test')
    incorrect_value = 123
    empty_string = ''
    perm_err = '/perm_err'

    expect_1 = (0, '')
    expect_2 = (0, '')
    expect_3 = (-1, 'Your enter incorrect value')
    expect_4 = (-1, "[Errno 2] No such file or directory: ''")
    expect_5 = (-1, "[Errno 13] Permission denied: '/perm_err'")

    assert split.check_exist_dir(exist_dir) == expect_1
    assert split.check_exist_dir(not_exist_dir) == expect_2
    assert split.check_exist_dir(incorrect_value) == expect_3
    assert split.check_exist_dir(empty_string) == expect_4
    assert split.check_exist_dir(perm_err) == expect_5


def test_write_to_file():
    results_1_incorrect = [12, 123, 23]
    path_1 = 'file.txt'
    expect_1 = (-1, 'Incorrect type results')

    results_2 = {
        'Min': 177.684237,
        'Max': 200.515051,
        'Mean': 189.37092438888888,
        'Sum': 3408.676639,
    }
    path_2_incorrect = 123
    expect_2 = (-1, 'Incorrect type path')

    results_3_empty = {}
    path_3 = os.path.join(DIR, 'test_write_to_file_1.messtat')
    expect_3 = (0, '')

    results_4 = {
        'Min': 177.684237,
        'Max': 200.515051,
        'Mean': 189.37092438888888,
        'Sum': 3408.676639,
        }
    path_4_empty = ''
    expect_4 = (0, '')

    results_5 = {
        'Min': 177.684237,
        'Max': 200.515051,
        'Mean': 189.37092438888888,
        'Sum': 3408.676639,
    }
    path_5 = os.path.join(DIR, 'test_write_to_file_1.messtat')
    expect_5 = (0, '')

    results_6 = {
        'Min': 177.684237,
        'Max': 200.515051,
        'Mean': 189.37092438888888,
        'Sum': 3408.676639,
    }
    path_6 = os.path.join('/', 'permission_error.messtat')
    expect_6 = (-1, "[Errno 13] Permission denied: '/messtat_permission_error.messtat.spliter'")

    results_7 = {
        'Min': 177.684237,
        'Max': 200.515051,
        'Mean': 189.37092438888888,
        'Sum': 3408.676639,
    }
    path_7 = os.path.join('test', 'test', 'test', 'test_write_to_file_1.messtat')
    expect_7 = (-1, "[Errno 2] No such file or directory: "
                    "'test/test/test/messtat_test_write_to_file_1.messtat.spliter'")

    assert split.write_to_file(path_1, results_1_incorrect) == expect_1
    assert split.write_to_file(path_2_incorrect, results_2) == expect_2
    assert split.write_to_file(path_3, results_3_empty) == expect_3
    assert split.write_to_file(path_4_empty, results_4) == expect_4
    assert split.write_to_file(path_5, results_5) == expect_5
    assert split.write_to_file(path_6, results_6) == expect_6
    assert split.write_to_file(path_7, results_7) == expect_7


def test_splitres_for_file():
    path_1 = PERM_DEN_FILE
    result_dir_1 = DIR
    expect_1 = (-1, "[Errno 13] Permission denied: 'test_dir_2/perm_err.messtat'")

    path_2 = EMPTY_FILE
    result_dir_2 = os.path.join('test', 'test', 'test')
    expect_2 = (-1, "[Errno 2] No such file or directory: "
                    "'test/test/test/messtat_empty.messtat.spliter'")

    assert split.splitres_for_file(path_1, result_dir_1) == expect_1
    assert split.splitres_for_file(path_2, result_dir_2) == expect_2
