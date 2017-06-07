#!/usr/bin/env python

import os
import sys
import argparse

from vivialconnect import Resource

from messages import send_message, get_message, list_messages
from accounts import billing_status, list_subaccounts, update_account, \
    get_account, create_subaccount
from numbers import list_associated_numbers, list_available_numbers, \
    buy_number, update_number_name
from users import list_users, get_user, update_user

home = os.path.dirname(os.path.abspath(__file__))

Resource.api_key = ""
Resource.api_secret = ""
Resource.api_account_id = ""

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        help='commands',
        dest='command')

    # Accounts command
    account_parser = subparsers.add_parser('account', help='Runs account examples')
    account_parser.add_argument('--list', '-l', default=False, action='store_true',
                                help='Lists sub-accounts associated with the main account')
    account_parser.add_argument('--get', '-g', default=False, action='store_true',
                                help='Get account resource')
    account_parser.add_argument('--create', '-c', default=False, action='store_true',
                                help='Create sub-account resource')
    account_parser.add_argument('--update', '-u', default=False, action='store_true',
                                help='Upate account or sub-account resource')
    account_parser.add_argument('--billing-status', '-s', default=False, action='store_true',
                                help='Get account billing status')
    account_parser.add_argument('--id', '-i', required=False,
                                type=str, action='store',
                                help='Resource id')
    account_parser.add_argument('--company-name', '-n', required=False,
                                type=str, action='store',
                                help='Company name')

    # Users command
    users_parser = subparsers.add_parser('user', help='Runs user examples')
    users_parser.add_argument('--list', '-l', default=False, action='store_true',
                              help='Lists users associated with your account')
    users_parser.add_argument('--get', '-g', default=False, action='store_true',
                              help='Get user resource')
    users_parser.add_argument('--id', '-i', required=False,
                              type=str, action='store',
                              help='Resource id')

    # Mesages command
    messages_parser = subparsers.add_parser('message', help='Runs messages example')
    messages_parser.add_argument('--list', '-l', default=False, action='store_true',
                                 help='Lists message resources')
    messages_parser.add_argument('--send', '-s', default=False, action='store_true',
                                 help='Send message')
    messages_parser.add_argument('--get', '-g', default=False, action='store_true',
                                 help='Get message resource')
    messages_parser.add_argument('--id', '-i', required=False,
                                 type=str, action='store',
                                 help='Resource id')
    messages_parser.add_argument('--body', '-b', required=False,
                                 type=str, action='store',
                                 help='Message body')
    messages_parser.add_argument('--media-url', '-u', required=False,
                                 type=str, action='store',
                                 help='Media URL for MMS')
    messages_parser.add_argument('--from-number', '-f', required=False,
                                 type=str, action='store',
                                 help='From phone number (+12123456789)')
    messages_parser.add_argument('--to-number', '-t', required=False,
                                 type=str, action='store',
                                 help='To phone number (+12128765432)')

    # Number command
    number_parser = subparsers.add_parser('number', help='Runs number examples')
    number_parser.add_argument('--list-available', '-a', default=False, action='store_true',
                               help='Lists available numbers')
    number_parser.add_argument('--list-associated', '-l', default=False, action='store_true',
                               help='Lists associated numbers')
    number_parser.add_argument('--buy', '-b', default=False, action='store_true',
                               help='Buy number')
    number_parser.add_argument('--update', '-u', default=False, action='store_true',
                               help='Update number')
    number_parser.add_argument('--id', '-i', required=False,
                               type=str, action='store',
                               help='Resource id')
    number_parser.add_argument('--phone-number-name', '-n', required=False,
                               type=str, action='store',
                               help='Phone number name')
    number_parser.add_argument('--phone-number', '-p', required=False,
                               type=str, action='store',
                               help='Phone number (+12124567890)')

    args = parser.parse_args()

    if args.command == 'message':
        if args.send:
            # https://imgs.xkcd.com/comics/lisp_cycles.png
            message = send_message(to_number=args.to_number,
                                   from_number=args.from_number,
                                   body=args.body,
                                   media_urls=[args.media_url] if args.media_url else None)
            print(message.id, message.from_number, message.to_number)
        if args.get:
            message = get_message(args.id)
            print(message.id, message.from_number,
                  message.to_number, message.body)
        if args.list:
            for message in list_messages():
                print(message.id, message.to_number,
                      message.from_number, message.body)

    elif args.command == 'number':
        if args.list_available:
            for number in list_available_numbers():
                print(number.name, number.phone_number_type,
                      number.phone_number)
        if args.list_associated:
            for number in list_associated_numbers():
                print(number.id, number.name,
                      number.phone_number_type,
                      number.phone_number)
        if args.buy:
            area_code = args.phone_number[2:5] if args.phone_number.startswith('+') \
                else args.phone_number[1:4]
            number = buy_number(name=args.phone_number_name,
                                phone_number=args.phone_number,
                                area_code=area_code,
                                phone_number_type='local')
            print(number.id, number.name, number.phone_number)
        if args.update:
            number = update_number_name(args.id, name=args.phone_number_name)
            print(number.id, number.name, number.phone_number)
    elif args.command == 'user':
        if args.list:
            for user in list_users():
                print(user.id, user.first_name, user.last_name)
        if args.get:
            user = get_user(args.id)
            print(user.id, user.first_name, user.last_name)
    elif args.command == 'account':
        if args.billing_status:
            status = billing_status()
            print(status)
        if args.list:
            for account in list_subaccounts():
                print(account.id, account.company_name)
        if args.get:
            account = get_account(args.id)
            print(account.id, account.company_name)
        if args.create:
            account = create_subaccount(company_name=args.company_name)
            print(account.id, account.company_name)
        if args.update:
            account = update_account(args.id, company_name=args.company_name)
            print(account.id, account.company_name)

if __name__ == "__main__":
    main()
