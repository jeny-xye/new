"""
    author: Zituo Yan
    description: this starts the verification part
    date: 3/2/2020
"""
from gedcom_app.control.child_birth import birth_before_marriage
from gedcom_app.control.US0203 import birth_b_marriage_us02,  birth_b_death_us03
from gedcom_app.control.US1217 import parents_not_too_old_us12, no_marriage_to_children_us17

def verification(indi_dict, fam_dict):
    birth_before_marriage(fam_dict)
    birth_b_marriage_us02(fam_dict)
    birth_b_death_us03(indi_dict)
    parents_not_too_old_us12(fam_dict)
    no_marriage_to_children_us17(fam_dict)
