"""
    author: Xinyi Ye, Zituo Yan
    description: parse GEDCOM file and save records into database
    date: 21/02/2020
"""
from collections import defaultdict

from gedcom_app.control.build_entity import build_individual, build_family
from gedcom_app.control.verification import verification
from gedcom_app.view.output_errors import output_errors_indi, output_errors_fam
from gedcom_app.view.output_prettytable import individual_table, family_table


def parse_gedcom(path):
    """
    parse_GEDCOM() funtion:
    parse .ged file to collect all data into dict_indi dictionary and dict_fam dictionary
    """

    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError(f"can not open this path")
    else:
        with fp:

            """
            dicy_indi, dict_fam dictionaries: collect the results of data in .ged file
            """
            num = 0
            list = []
            sum = []
            date_b = 0
            """
            num: record the number of 'INDI' and 'FAM' as a parameter
            list: temporary list to add data into sum
            sum: collect all datas into sum list
            date_b : a variable to record number of 'DATE', it is used to judge 'BIRT' or 'DEAT', 'MARR' or 'DIV'
            """
            line_num = 0
            for line in fp:
                line_num += 1
                line = line.rstrip('\n').rstrip(' ')
                list_line = line.split(' ')
                level = list_line[0]

                if level == '0':
                    s_tag = list_line[len(list_line) - 1]
                    """ s_tag: the last word in the line, it used to judge 'INDI' or 'FAM"""
                    del list_line[0]
                    del list_line[len(list_line) - 1]
                    ID = ' '.join(list_line)
                    """ ID: argument"""

                    if num == 0:
                        """ 
                        num: record the number of 'INDI' and 'FAM' as a parameter
                        """
                        if s_tag == 'INDI':
                            num += 1
                            line_ID = line_num
                            list.append(['INDI', ID, line_ID])
                        elif s_tag == 'FAM':
                            num += 1
                            line_ID = line_num
                            list.append(['FAM', ID, line_ID])
                    else:
                        """
                        num != 0 which means there is already an 'INDI' or 'FAM'
                        when level == 0, it means an INDI or FAM is finished
                        """
                        num += 1
                        if num == 2:
                            """ an INDI or FAM is finished"""
                            sum.append(list)
                            list = []

                            if s_tag == 'INDI':
                                num = 1
                                line_ID = line_num
                                list.append(['INDI', ID, line_ID])

                            elif s_tag == 'FAM':
                                num = 1
                                line_ID = line_num
                                list.append(['FAM', ID, line_ID])
                            else:
                                num = 0
                elif level != '0':
                    tag = list_line[1]
                    del list_line[0: 2]
                    argument = ' '.join(list_line)
                    if tag == 'BIRT':
                        date_b = 1
                    elif tag == 'MARR':
                        date_b = 2
                    elif tag == 'DEAT':
                        date_b = 3
                    elif tag == 'DIV':
                        date_b = 4
                    elif date_b == 1:
                        if tag == 'DATE':
                            """ date_b == 1 which means it is birth date """
                            line_birth = line_num
                            list.append(['BIRTH', argument, line_birth])
                        else:
                            line_birth = line_num - 1

                            list.append(['BIRTH', '', line_birth])
                            list.append([tag, argument, line_num])
                        date_b = 0
                    elif date_b == 2:
                        if tag == 'DATE':
                            """ date_b == 2 which means it is married date"""
                            list.append(['MARR', argument, line_num])
                        else:
                            list.append(['MARR', '', line_num - 1])
                            list.append([tag, argument, line_num])
                        date_b = 0
                    elif date_b == 3:
                        if tag == 'DATE':
                            """ date_b == 3 which means it is death date """
                            line_death = line_num
                            list.append(['DEAT', argument, line_death])
                        else:
                            line_death = line_num - 1

                            list.append(['DEAT', '', line_death])
                            list.append([tag, argument, line_num])
                        date_b = 0
                    elif date_b == 4:
                        if tag == 'DATE':
                            """ date_b == 4 which means it is divorced date"""
                            list.append(['DIV', argument, line_num])
                        else:
                            list.append(['DIV', '', line_num - 1])
                            list.append([tag, argument, line_num])
                        date_b = 0
                    else:
                        list.append([tag, argument, line_num])
                        date_b = 0

            if level != '0':
                """ 
                whis situation is INDI or FAM ends without accompanying level 0
                """
                sum.append(list)
            return build_dictionary(sum)


def build_dictionary(sum):
    dict_indi = []
    dict_fam = []
    for item in sum:
        if item[0][0] == 'INDI':
            feat_IND = defaultdict(lambda: 'N/A')
            fams_s = []
            famc_s = []
            for q in item:
                if q[0] == 'FAMC':

                    famc_s.append((q[1], q[2]))

                    feat_IND['FAMC'] = famc_s
                    """ 
                    collect famc in indi level and put them into famc_s set
                    """
                elif q[0] == 'FAMS':

                    fams_s.append((q[1], q[2]))
                    feat_IND['FAMS'] = fams_s
                    """
                    collect fams in indi level and put them into fams_s set
                    """
                else:
                    feat_IND[q[0]] = (q[1], q[2])
            dict_indi.append(feat_IND)
            """ put feat_IND into the result dictionary dict_indi """
        elif item[0][0] == 'FAM':
            feat_FAM = defaultdict(lambda: 'N/A')
            child_s = []
            for q in item:
                if q[0] == 'CHIL':

                    child_s.append((q[1], q[2]))
                    feat_FAM['CHIL'] = child_s
                    """
                    collect children in fam level and put them into child_s set
                    """
                else:
                    feat_FAM[q[0]] = (q[1], q[2])
            dict_fam.append(feat_FAM)
            """ put feat_FAM into the result dictionary dict_fam """

    if len(dict_indi) < 5000 and len(dict_fam) < 1000:
        indi_list = build_individual(dict_indi)
        fam_list = build_family(dict_fam, indi_list)
        individual_table(indi_list)
        family_table(fam_list)
        verification(indi_list, fam_list)
        output_errors_indi(indi_list)
        output_errors_fam(fam_list)
        return dict_indi, dict_fam
    else:
        raise ValueError(f"Data overflow")

# def main():
#     path = r"/Users/zituoyan/Documents/GitHub/SSW555AP2020s/test.ged"
#     parse_gedcom(path)
#
#
# if __name__ == '__main__':
#     main()
