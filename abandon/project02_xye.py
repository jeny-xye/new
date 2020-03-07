"""
Project02
Author: Xinyi Ye
Date: 02/04/2020
"""


def test_GEDCOM(path):
    """ test_GEDCOM() funtion: test .ged file to determine whether the tag is valid """

    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        yield (f"can not open this path")
    else:
        with fp:
            list0 = ['INDI', 'HEAD', 'TRLR', 'NOTE', 'FAM']
            list1 = ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC',
                     'FAMS', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV']
            list2 = ['DATE']
            dict = {'0': list0, '1': list1, '2': list2}
            for line in fp:
                line = line.rstrip('\n').rstrip(' ')
                list_line = line.split(' ')
                yield(f"--> {line}")
                level = list_line[0]

                if list_line[len(list_line)-1] in ['INDI', 'FAM']:
                    """ the tag at end of line is 'INDI' or 'FAM' """
                    tag = list_line[len(list_line)-1]
                    del list_line[0]
                    del list_line[len(list_line)-1]
                    argument = ' '.join(list_line)
                    if level == '0':
                        """ the level is 0, tag is valid """
                        result = '|'.join([level, tag, 'Y', argument])
                    else:
                        """ the level is not 0, tag is invalid """
                        result = '|'.join([level, tag, 'N', argument])

                else:
                    """ the tag at end of line is not 'INDI' or 'FAM' """
                    tag = list_line[1]
                    del list_line[0: 2]
                    argument = ' '.join(list_line)
                    if level in ['0', '1', '2'] and tag in dict[level]:
                        """ level is 0/1/2, and tag corresponds to level """
                        if level == '0' and tag in ['INDI', 'FAM']:
                            """ the level is 0 and tag 'INDI' or 'FAM is not at end , Invalid"""
                            result = '|'.join([level, tag, 'N', argument])
                        else:
                            result = '|'.join([level, tag, 'Y', argument])

                    else:
                        """ level is not 0/1/2, or tag doesn't correspond to level """
                        result = '|'.join([level, tag, 'N', argument])

                yield(f"<-- {result}")


if __name__ == "__main__":
    path = input('Please input the path of GEDCOM file:')
    for i in test_GEDCOM(path):
        print(i)
        