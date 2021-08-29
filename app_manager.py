#!/usr/bin/env python3
from models_db import User
from psycopg2 import connect
from psycopg2.errors import UniqueViolation
import sys
from crypt_pass import check_password

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


def add_user(cursor, name, password):
    """Add user and password to the database, check password if 8 characters long"""

    if len(password) <= 8:
        print("Password is to short, it must contain at least 8 characters. ")
    else:
        try:
            new_user = User(name, password)
            new_user.save_to_db(cursor)
        except UniqueViolation as error:
            print(f'User Name: "{name}" already exist in the database !')

        print(f'USER: {name} created !')


def manage_user_password(cursor, name, password, new_password):
    """Edit user password if given user_name and password is correct also check if new password is 8 characters long"""

    user = User.load_user_by_name(cursor, name)

    if not user:
        print(f'User: "{name}" does not exist !')

    elif not check_password(password, user.hashed_password):
        print(f'Password for user: "{name}" is incorrect!')

    else:
        if len(new_password) < 8:
            print('New password is to short, it must be at least 8 characters long.')

        else:
            user.set_password(new_password)
            user.save_to_db(cursor)
            print(f'New password for user: "{name}" has been set!')


def delete_user(cursor, username, password):
    pass


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
        manage_user_password(cursor, args.username, args.password, args.new_password)

    elif args.username and args.password and not args.new_password and not args.list \
            and not args.delete and not args.edit:
        add_user(cursor, args.username, args.password)

    elif args.username and args.password and not args.new_password and not args.list \
            and args.delete and not args.edit:
        delete_user(cursor, args.username, args.password)

    else:
        parser_.print_help(sys.stderr)  # Print argparse help if non of the options above are chosen.
        sys.exit(1)

    # ---------------------------------------------------------------

    # except:
    #    print("There is error in execute_sql")
    # else:
    cursor.close()
    cnx.close()


if __name__ == '__main__':
    main()
