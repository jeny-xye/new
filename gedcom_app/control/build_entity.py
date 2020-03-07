"""
    author: Zituo Yan
    description: build individual and family entity
    date: 2/3/2020
"""
from collections import defaultdict

from gedcom_app.entity.individual import Individual
from gedcom_app.entity.family import Family


def build_individual(indi):
    indi_dict = defaultdict(Individual)
    for people in indi:
        new_indi = Individual(people["INDI"], people["NAME"], people["SEX"],
                              people["BIRTH"], people["DEAT"], people["FAMC"], people["FAMS"])
        indi_dict[people["INDI"][0]] = new_indi
    return indi_dict


def build_family(fam, indi_dict):
    fam_dict = defaultdict(Family)
    for family in fam:
        print(family)
        new_fam = Family(family["FAM"], family["MARR"], family["DIV"],
                         # add husband into family dictionary as an individual class
                         # which search from individual dictionary
                         (indi_dict[family["HUSB"][0]], family["HUSB"][1]),
                         (indi_dict[family["WIFE"][0]], family["WIFE"][1]))
        if family["CHIL"] != "N/A":
            for people in family["CHIL"]:
                new_child = indi_dict[people[0]]
                new_fam.children = new_child
        fam_dict[family["FAM"][0]] = new_fam
    return fam_dict
