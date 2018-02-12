#!/usr/bin/env python3

import os
import sys
import simpleakamai

client = simpleakamai.Client(os.environ['AKAMAI_PAPI_URL'],
                             os.environ['AKAMAI_PAPI_CLIENT_TOKEN'],
                             os.environ['AKAMAI_PAPI_CLIENT_SECRET'],
                             os.environ['AKAMAI_PAPI_ACCESS_TOKEN'])

hostname = input("\nPlease type the hostname: ")
environment = input("\nPlease choose environment (0 for staging, 1 for production): ")

if environment != '0' and environment != '1':
    print('Invalid option, exit!\n')
    sys.exit()
else:
    versions = client.search_property(hostname)

if versions:
    if environment == '0':
        print("\nYou chose to check staging")
        version = client.get_active_version(versions, 'staging')
        configuration = client.download_config(version['staging_propertyId'], version['staging_propertyVersion'],
                                            version['staging_contractId'], version['staging_groupId'])
    if environment == '1':
        print("\nYou chose to check production")
        version = client.get_active_version(versions, 'production')
        configuration = client.download_config(version['production_propertyId'], version['production_propertyVersion'],
                                           version['production_contractId'], version['production_groupId'])

    rules = configuration['rules']

    print('\nChecking origin settings...')
    client.parse_config(hostname, rules)

    if client.custom_origin.get('hostname'):
        client.print_custom_origin()
    else:
        client.print_default_origin()

    choice = input("\nDo you want to read all rules? (y or n) ")
    if choice == 'y':
        print('\nChecking all rules...')
        client.check_rules(hostname, rules)
    else:
        print('Bye!')
else:
    sys.exit()


