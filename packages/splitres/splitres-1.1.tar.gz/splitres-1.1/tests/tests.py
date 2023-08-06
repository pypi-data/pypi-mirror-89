"""Testing with pytest"""

import src.splitres as split
import os
import shutil
from unittest.mock import patch

def setup_module(module):
    global FILE_1
    global FILE_2
    global FILE_3
    global DIR

    DIR = 'test_dir'
    FILE_1 = '%s/test1.messtat' % DIR
    FILE_2 = '%s/test2.messtat' % DIR
    FILE_3 = '%s/test3.messtat' % DIR

    os.mkdir(DIR)

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


def teardown_module(module):
    shutil.rmtree(DIR)


def test_parser_for_messtatfile():
    expect_1 = [51.83672, 68.42524, 42.836865, 56.918372]
    expect_2 = [43.681163, 52.444812, 42.841015, 56.222818, 167.287719, 159.156453]
    expect_3 = [198.265667, 178.879059, 198.888102, 178.416352, 198.785196, 179.179901,
                197.353255, 178.551606, 199.229043, 179.529569, 198.132672, 179.313994,
                200.303259, 181.665368, 200.515051, 185.86012, 198.124188, 177.684237]

    assert split.parser_for_messtatfile(FILE_1) == expect_1
    assert split.parser_for_messtatfile(FILE_2) == expect_2
    assert split.parser_for_messtatfile(FILE_3) == expect_3


def test_counting_values():
    expect_1 = [42.836865, 68.42524, 55.00429925, 220.017197]
    expect_2 = [42.841015, 167.287719, 86.93899666666667, 521.6339800000001]
    expect_3 = [177.684237, 200.515051, 189.37092438888888, 3408.676639]

    data = split.parser_for_messtatfile(FILE_1)
    assert split.counting_values(data) == expect_1

    data = split.parser_for_messtatfile(FILE_2)
    assert split.counting_values(data) == expect_2

    data = split.parser_for_messtatfile(FILE_3)
    assert split.counting_values(data) == expect_3


def test_splitres():
    expect_1 = [42.836865, 68.42524, 55.00429925, 220.017197]
    expect_2 = [42.841015, 167.287719, 86.93899666666667, 521.6339800000001]
    expect_3 = [177.684237, 200.515051, 189.37092438888888, 3408.676639]

    expect = [expect_3, expect_2, expect_1]

    with patch('os.path.isdir', return_value=False), \
         patch('builtins.print') as mm:
        split.splitres('not exist file', DIR)

        mm.assert_called_once_with('File isn\'t exist!')

    assert split.splitres(FILE_1, DIR) == [expect_1]
    assert split.splitres(FILE_2, DIR) == [expect_2]
    assert split.splitres(FILE_3, DIR) == [expect_3]

    assert split.splitres(DIR, DIR).sort() == expect.sort()


def test_check_exist_dir():
    exist_dir = DIR
    not_exist_dir = '%s/%s' % (DIR, 'test')

    assert split.check_exist_dir(exist_dir) == exist_dir
    assert split.check_exist_dir(not_exist_dir) == not_exist_dir

