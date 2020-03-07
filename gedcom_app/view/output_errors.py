"""
    author: Zituo Yan
    description: outputs of errors
    date: 7/3/2020
"""


def output_errors_fam(fam):
    """
                 {"error_type": self.__error_info[0],
                "indi_or_fam": self.__error_info[1],
                "user_story": self.__error_info[2],
                "error_line": self.__error_info[3],
                "entity_id": self.__error_info[4]}
                                # print(f"ANOMALY: FAMILY: US08: {bir_line}: {key}: "
                #       f"Child {child_id} born {birth} before marriage on {marr_date}")
    :param fam:
    :return:
    """
    for family in fam.values():
        error_list = family.error_list
        if len(error_list) != 0:
            for error in error_list:
                print(f"{error.error_info['error_type']}: {error.error_info['indi_or_fam']}: "
                      f"{error.error_info['user_story']}: {error.error_info['error_line']}: "
                      f"{error.error_info['entity_id']}: {error.error_message}")


def output_errors_indi(indi):
    for indi in indi.values():
        error_list = indi.error_list
        if len(error_list) != 0:
            for error in error_list:
                print(f"{error.error_info['error_type']}: {error.error_info['indi_or_fam']}: "
                      f"{error.error_info['user_story']}: {error.error_info['error_line']}: "
                      f"{error.error_info['entity_id']}: {error.error_message}")
