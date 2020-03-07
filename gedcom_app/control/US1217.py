"""
US12US17
Author: Xinyi Ye
Date: 03/04/2020
"""
from datetime import datetime
from collections import defaultdict
from gedcom_app.errors.gedcom_error import GedcomError


def parents_not_too_old_us12(fam):
    for key, value in fam.items():

        if value.children == ['N/A']:
            continue
        else:
            id_h = value.husband[0]
            birth_h = id_h.birthday
            h_birth_date = datetime.strptime(birth_h[0], "%d %b %Y")
            id_w = value.wife[0]
            birth_w = id_w.birthday
            w_birth_date = datetime.strptime(birth_w[0], "%d %b %Y")

            for child in value.children:
                id_c = child.indi_id[0]
                birth_c = child.birthday
                c_birth_date = datetime.strptime(birth_c[0], "%d %b %Y")

                num_hc = c_birth_date - h_birth_date
                l_hc = str(num_hc).split(' ')
                num_wc = c_birth_date - w_birth_date
                l_wc = str(num_wc).split(' ')

                if int(l_hc[0]) >= 80 * 365.25:

                    new_error = GedcomError(("ERROR", "FAMILY", "US12", birth_h[1], key),
                                            f"father {id_h.indi_id[0]} {birth_h[0]} "
                                            f"is not less than 80 years old than child {id_c} {birth_c[0]}")
                    value.error_list = new_error

                if int(l_wc[0]) >= 60 * 365.25:

                    new_error = GedcomError(("ERROR", "FAMILY", "US12", birth_w[1], key),
                                            f"mother {id_w.indi_id[0]} {birth_w[0]} "
                                            f"is not less than 60 years old than child {id_c} {birth_c[0]}")
                    value.error_list = new_error

                else:
                    continue


def no_marriage_to_children_us17(fam):
    dict_h = defaultdict(lambda: 'N/A')
    dict_w = defaultdict(lambda: 'N/A')
    for key, value in fam.items():
        l_c = []
        id_h = value.husband[0]

        id_w = value.wife[0]
        if value.children == ['N/A']:
            continue
        else:
            for child in value.children:
                id_c = child.indi_id[0]
                l_c.append(id_c)
        if dict_h[id_h.indi_id[0]] == 'N/A':
            dict_h[id_h.indi_id[0]] = l_c
        else:
            dict_h[id_h.indi_id[0]] = l_c + dict_h[id_h.indi_id[0]]

        if dict_w[id_w.indi_id[0]] == 'N/A':
            dict_w[id_w.indi_id[0]] = l_c
        else:
            dict_w[id_w.indi_id[0]] = l_c + dict_w[id_w.indi_id[0]]

    for key1, value1 in fam.items():
        husband_id = value1.husband[0]
        wife_id = value1.wife[0]
        if wife_id.indi_id[0] in dict_h[husband_id.indi_id[0]]:

            new_error = GedcomError(("ERROR", "FAMILY", "US17", wife_id.indi_id[1], key1),
                                    f"father {husband_id.indi_id[0]} married to his child {wife_id.indi_id[0]}")
            value1.error_list = new_error

        if husband_id.indi_id[0] in dict_w[wife_id.indi_id[0]]:

            new_error = GedcomError(("ERROR", "FAMILY", "US17", husband_id.indi_id[1], key1),
                                    f"mother {wife_id.indi_id[0]} married to her child {husband_id.indi_id[0]}")
            value1.error_list = new_error
        else:
            continue




