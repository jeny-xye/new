"""
    author: Zituo Yan
    description: Start application
    date:21/02/2020
"""
from gedcom_app.control.parser import parse_gedcom


def main():
    path = ""
    while len(path) == 0:
        path = input("Please enter your GEDCOM file path:\n")
    parse_gedcom(path)


if __name__ == '__main__':
    main()
