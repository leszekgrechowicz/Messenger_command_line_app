#!/usr/bin/env python3
from models_db import User
from psycopg2 import connect
from psycopg2.errors import UniqueViolation
from sys import stderr, exit

"""
Author : Leszek Grechowicz leszek_grechowicz@o2.pl
Date   : 28/08/2021
Purpose: Command Line Messenger
"""

import argparse


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Command Line based "Messenger"',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # parser.add_argument('positional',
    #                     metavar='str',
    #                     help='A positional argument')

    parser.add_argument('-u',
                        '--username',
                        help='User Name',
                        metavar='str',
                        type=str)

    parser.add_argument('-p',
                        '--password',
                        help='Password min. 8 characters',
                        metavar='str',
                        type=str)

    parser.add_argument('-n',
                        '--new_password',
                        help='New Password',
                        metavar='str',
                        type=str)

    parser.add_argument('-l',
                        '--list',
                        help='List all users',
                        action='store_true')

    parser.add_argument('-d',
                        '--delete',
                        help='Delete user',
                        action='store_true')

    parser.add_argument('-e',
                        '--edit',
                        help='Edit User',
                        action='store_true')

    return parser, parser.parse_args()


# --------------------------------------------------


def add_user(currsor, name, password):
    if len(password) <= 8:
        print("Password is to short, it must contain at least 8 characters. ")
    else:
        try:
            new_user = User(name, password)
            new_user.save_to_db(currsor)
        except UniqueViolation as error:
            print(f'User Name: "{name}" already exist in the database !')

        print(f'USER: {name} created !')


def main():
    """Connect to database and serv user queries"""

    db = 'messenger'
    USER = "postgres"
    HOST = "localhost"
    PASSWORD = "password"

    # create_db(db)

    # try:
    cnx = connect(user=USER, password=PASSWORD, host=HOST, database=db)
    cnx.autocommit = True
    cursor = cnx.cursor()

    # --------------------------------------------------------------

    parser_, args = get_args()

    if args.username and args.password and args.new_password and not args.list \
            and not args.delete and args.edit:
        print('OK')

    elif args.username and args.password and not args.new_password and not args.list \
            and not args.delete and not args.edit:
        add_user(cursor, args.username, args.password)

    else:
        parser_.print_help(stderr)
        exit(1)

    # ---------------------------------------------------------------

    # except:
    #    print("There is error in execute_sql")
    # else:
    cursor.close()
    cnx.close()


if __name__ == '__main__':
    main()
