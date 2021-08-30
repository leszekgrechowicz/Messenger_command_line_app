#!/usr/bin/env python3
from models_db import User, Message
from psycopg2 import connect, Error
import sys
from crypt_pass import check_password

"""
Author : Leszek Grechowicz leszek_grechowicz@o2.pl
Date   : 28/08/2021
Purpose: Command Line Messenger - User/Main App 
"""

import argparse


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Command Line based "Messenger"',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

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

    parser.add_argument('-t',
                        '--to',
                        help='User_Name the message should be send to.',
                        metavar='str',
                        type=str)

    parser.add_argument('-s',
                        '--send',
                        help='Message text',
                        metavar='str',
                        type=str)

    parser.add_argument('-l',
                        '--list',
                        help='List all users messages',
                        action='store_true')

    return parser, parser.parse_args()


# --------------------------------------------------

def check_user(user, name, password):
    """Check if login details are correct and inform user if not"""

    if not user:
        print(f'\nUser: "{name}" does not exist!')

    elif not check_password(password, user.hashed_password):
        print(f'\nPassword for user: "{name}" is incorrect!')

    else:
        return True


def list_messages(cursor, name, password):
    """List all messages send by logged user"""

    user = User.load_user_by_name(cursor, name)
    user_ok = check_user(user, name, password)

    if user_ok:
        messages = Message().load_all_messages(cursor, user.id)

        if not messages:
            print("\nNo messages!")
        else:
            for message in messages:
                from_user = User().load_user_by_id(cursor, message.from_id)
                print(f"\nFrom: {from_user.username}\tOn: {str(message.creation_date)[:19]}"
                      f"\tMessage: {message.text}")


def send_message(cursor, name, password, to_user, message):
    """Checks sender credentials as well as if recipient exist, if so sends the message"""

    user = User.load_user_by_name(cursor, name)
    user_ok = check_user(user, name, password)

    if user_ok:
        recipient = User().load_user_by_name(cursor, to_user)
        if not recipient:
            print(f'\nUser "{to_user}" you want to send the message to, does not exist!')

        elif len(message) > 255:
            print('\nMessage to long - max length 255 characters.')

        else:
            message = Message(user.id, recipient.id, message)
            message.save_to_db(cursor)
            print(f'\nMessage to {recipient.username} has been sent!')


def main():
    """Connect to database and serv user queries"""

    db = 'messenger'
    USER = "postgres"
    HOST = "localhost"
    PASSWORD = "password"

    # create_db(db)

    try:
        cnx = connect(user=USER, password=PASSWORD, host=HOST, database=db)
        cnx.autocommit = True
        cursor = cnx.cursor()

        # --------------------------------------------------------------

        parser_, args = get_args()

        if args.username and args.password and args.list and not args.to \
                and not args.send:
            list_messages(cursor, args.username, args.password)

        elif args.username and args.password and not args.list and args.to \
                and args.send:
            send_message(cursor, args.username, args.password, args.to, args.send)

        else:
            parser_.print_help(sys.stderr)  # Print argparse help if non of the options above are chosen.
            sys.exit(1)

    # ---------------------------------------------------------------

    except Error as error:
        print(f"{error}")
    else:
        cursor.close()
        cnx.close()


if __name__ == '__main__':
    main()
