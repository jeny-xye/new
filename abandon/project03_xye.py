"""
project03
Date: 02.14.2020
"""
from prettytable import PrettyTable
from collections import defaultdict


def parse_GEDCOM(path):
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

            dict_indi = {}
            dict_fam = {}
            """
            dicy_indi, dict_fam dictionaries: collect the results of data in .ged file
            """
            child_s = set()
            famc_s = set()
            fams_s = set()
            """
            child_s sets: collect children in FAM level, 
            famc_s, fams_s sets: collect children and spouses in INDI level
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
            feat_IND = defaultdict(lambda: 'N/A')
            feat_FAM = defaultdict(lambda: 'N/A')
            """ 
            feat_IND, feat_FAM are defaultdict, the default value is 'N/A'
            used to record characteristics of INDI and FAM excepting ID
            """

            for line in fp:

                line = line.rstrip('\n').rstrip(' ')
                list_line = line.split(' ')
                level = list_line[0]

                if level == '0':
                    s_tag = list_line[len(list_line)-1]
                    """ s_tag: the last word in the line, it used to judge 'INDI' or 'FAM"""
                    del list_line[0]
                    del list_line[len(list_line)-1]
                    ID = ' '.join(list_line)
                    """ ID: argument"""

                    if num == 0:
                        """ 
                        num: record the number of 'INDI' and 'FAM' as a parameter
                        """
                        if s_tag == 'INDI':
                            num += 1
                            list.append(['INDI', ID])
                        elif s_tag == 'FAM':
                            num += 1
                            list.append(['FAM', ID])

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
                                list.append(['INDI', ID])

                            elif s_tag == 'FAM':
                                num = 1
                                list.append(['FAM', ID])
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
                    elif date_b == 1:
                        if tag == 'DATE':
                            """ date_b == 1 which means it is birth date """    
                            list.append(['BIRTH', argument])        
                        else:
                            list.append(['BIRTH', ''])
                            list.append([tag, argument])
                        date_b = 0
                    elif date_b == 2:
                        if tag == 'DATE':
                            """ date_b == 2 which means it is married date"""
                            list.append(['MARR', argument])    
                        else:
                            list.append(['MARR', ''])
                            list.append([tag, argument])
                        date_b = 0
                    else:
                        list.append([tag, argument])
                        date_b = 0
                    
            if level != '0':
                """ 
                whis situation is INDI or FAM ends without accompanying level 0
                """
                sum.append(list)

            for item in sum:

                if item[0][0] == 'INDI':
                    m = item.pop(0)
                    for q in item:
                        if q[0] == 'FAMC':
                            famc_s.add(q[1])
                            feat_IND['FAMC'] = famc_s
                            """ 
                            collect famc in indi level and put them into famc_s set
                            """
                        elif q[0] == 'FAMS':
                            fams_s.add(q[1])
                            feat_IND['FAMS'] = fams_s
                            """
                            collect fams in indi level and put them into fams_s set
                            """
                        else:
                            feat_IND[q[0]] = q[1]

                    dict_indi[m[1]] = feat_IND
                    """ put feat_IND into the result dictionary dict_indi """
                    famc_s = set()
                    fams_s = set()
                    feat_IND = defaultdict(lambda: 'N/A')

                elif item[0][0] == 'FAM':
                    n = item.pop(0)
                    for q in item:
                        if q[0] == 'CHIL':
                            child_s.add(q[1])
                            feat_FAM['CHIL'] = child_s
                            """
                            collect children in fam level and put them into child_s set
                            """
                        else:
                            feat_FAM[q[0]] = q[1]

                    dict_fam[n[1]] = feat_FAM
                    """ put feat_FAM into the result dictionary dict_fam """
                    child_s = set()
                    feat_FAM = defaultdict(lambda: 'N/A')
            
            if len(dict_indi) < 5000 and len(dict_fam) < 1000:
                return dict_indi, dict_fam
            else:
                raise ValueError(f"Data overflow")


if __name__ == "__main__":
    """ 
    main() function: input path, print two tables
    if data lost, it will view '' in table
    if no record of items, it will view'N/A'
    """
    path = input("please input the .ged file path:")
    try:
        indi, fam = parse_GEDCOM(path)
    except FileNotFoundError as e:
        print(e)
    except ValueError as m:
        print(m)
    else:
        table_indi = PrettyTable(
            ['ID', 'Name', 'Gender', 'Birthday', 'Alive', 'Death', 'Child', 'Spouse'])
        table_fam = PrettyTable(['ID', 'Married', 'Divorced', 'Husband ID',
                                 'Husband Name', 'Wife ID', 'Wife Name', 'Children'])

        for key, value in indi.items():            
            if value['DEAT'] == 'N/A':
                alive = 'TRUE'
            else:
                if value['DATE'] not in ['', 'N/A']:
                    alive = 'FALSE'
                else:   
                    alive = 'FALSE'
                    value['DATE'] = ''
                
            table_indi.add_row([key, value['NAME'], value['SEX'], value['BIRTH'],
                                alive, value['DATE'], value['FAMC'], value['FAMS']])

        for key, value in fam.items():
            id_h = value['HUSB']
            id_w = value['WIFE']
            """ husband id and wife id """
            if id_h not in ['N/A', '']:
                name_h = indi[id_h]['NAME']
            else:
                name_h = 'N/A'
            """ get husband's name"""
            if id_w not in['N/A', '']:
                name_w = indi[id_w]['NAME']
            else:
                name_w = 'N/A'
            """ get wife's name"""

            if value['DIV'] == 'N/A':
                value['DATE'] = 'N/A'
            elif value['DATE'] in ['', 'N/A']:
                value['DATE'] = ''
            """ 
            if div record lost, print''
            if no divorce, print'N/A'
            """
            table_fam.add_row([key, value['MARR'], value['DATE'],
                               id_h, name_h, id_w, name_w, value['CHIL']])

        print(table_indi)
        print(table_fam)
