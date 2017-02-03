#!/usr/bin/env python

import os
import sys
import argparse

from vivialconnect import Resource

from messages import send_message, get_message, list_messages
from accounts import billing_status, list_subaccounts, update_account, \
    get_account, create_subaccount, delete_subaccount
from configurations import list_configurations, create_configuration, \
    get_configuration, delete_configuration
from numbers import list_associated_numbers, list_available_numbers, \
    buy_number, update_number_name
from users import list_users, get_user, update_user

home = os.path.dirname(os.path.abspath(__file__))

Resource.api_key = ""
Resource.api_secret = ""
Resource.api_account_id = "10007"


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        help='commands',
        dest='command')

    # Users command
    users_parser = subparsers.add_parser('user', help='Runs user examples')
    users_parser.add_argument('--list', '-l', default=False, action='store_true',
                              help='Lists message resources')
    users_parser.add_argument('--get', '-g', default=False, action='store_true',
                              help='Get message resource')
    users_parser.add_argument('--id', '-i', required=False,
                              type=str, action='store',
                              help='Resource id')

    # Mesages command
    messages_parser = subparsers.add_parser('message', help='Run messages example')
    messages_parser.add_argument('--list', '-l', default=False, action='store_true',
                                 help='Lists message resources')
    messages_parser.add_argument('--send', '-s', default=False, action='store_true',
                                 help='Send message')
    messages_parser.add_argument('--get', '-g', default=False, action='store_true',
                                 help='Get message resource')
    messages_parser.add_argument('--id', '-i', required=False,
                                 type=str, action='store',
                                 help='Resource id')

    # Config command
    config_parser = subparsers.add_parser('config', help='Run configuration examples')
    config_parser.add_argument('--list', '-l', default=False, action='store_true',
                               help='Lists configuration resources')
    config_parser.add_argument('--create', '-c', default=False, action='store_true',
                               help='Creates configuration resource')
    config_parser.add_argument('--id', '-i', required=False,
                               type=str, action='store',
                               help='Resource id')

    args = parser.parse_args()

    if args.command == 'message':
        if args.send:
            send_message(to_number='+11234567890',
                         from_number='+19132597591',
                         body='Howdy, from Vivial Connect!')
        if args.get:
            get_message(args.id)
        if args.list:
            list_messages()
    elif args.command == 'number':
        list_available_numbers()
        buy_number(name='(913) 259-7591',
                   phone_number='+19132597591',
                   area_code='913',
                   phone_number_type='local')
        list_associated_numbers()
        update_number_name(22, name="KS - (913) 259-7591")
    elif args.command == 'user':
        if args.list:
            list_users()
        if args.get:
            get_user(args.id)
    elif args.command == 'account':
        billing_status()
        list_subaccounts()
        get_account(Resource.api_account_id)
        delete_subaccount(10018)
        create_subaccount(company_name='Vivial Connect - IT')
        update_account(Resource.api_account_id,
                       company_name='Vivial Connect - Vivial, Inc')
    elif args.command == 'config':
        if args.list:
            list_configurations()
        if args.remove:
            delete_configuration(args.id)
        if args.create:
            create_configuration(name='Configuration 1',
                                 phone_number='+19132597591',
                                 phone_number_type='local',
                                 sms_url='https://localhost/receive')

if __name__ == "__main__":
    main()
