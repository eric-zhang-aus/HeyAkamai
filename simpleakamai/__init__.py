import json
import requests
from akamai.edgegrid import EdgeGridAuth


class Client(object):

    def __init__(self, base_url, client_token, client_secret, access_token):
        """Authentication"""
        self.base_url = base_url
        self.client_token = client_token
        self.client_secret = client_secret
        self.access_token = access_token
        self.session = requests.Session()
        self.session.auth = EdgeGridAuth(
            client_token=self.client_token,
            client_secret=self.client_secret,
            access_token=self.access_token,
            max_body=128 * 1024
        )
        self.check_next = True
        self.default_origin = {}
        self.custom_origin = {}

    # PAPI
    def list_groups(self):
        """Get groups with contract"""
        response = self.session.get(self.base_url + '/papi/v1/groups',
                                    headers={'PAPI-Use-Prefixes': 'true'})
        groups = json.loads(response.text)['groups']['items']
        groups_with_contract = []
        for group in groups:
            if group.get('contractIds'):
                print(group)
                groups_with_contract.append(group)
        return groups_with_contract

    def search_property(self, hostname):
        """Search property that includes the hostname"""
        print('\nSearching the property for', hostname, '......')
        response = self.session.post(self.base_url + 'papi/v1/search/find-by-value',
                                     headers={'PAPI-Use-Prefixes': 'true'},
                                     json={'hostname': hostname})
        print(response.text)
        versions = json.loads(response.text)['versions']['items']
        if len(versions) == 0:
            print('Failed to find the property for', hostname)
            return False
        else:
            print('Property found:', versions[0]['propertyName'])
            return versions

    def get_active_version(self, versions, environment):
        """Find active staging and production version"""
        print('\nChecking the active versions of', environment, '...')
        version_info = {}
        for version in versions:
            if version['stagingStatus'] == 'ACTIVE':
                version_info['staging_propertyVersion'] = str(version['propertyVersion'])
                version_info['staging_propertyId'] = version['propertyId']
                version_info['staging_groupId'] = version['groupId']
                version_info['staging_contractId'] = version['contractId']
                version_info['staging_edgeHostname'] = version['edgeHostname'].replace('.net', '-staging.net')
                if not version.get('note'):
                    version['note'] = 'no comments found'
                version_info['staging_lastUpdate'] = version['updatedDate']\
                                                     + ' by ' + version['updatedByUser']\
                                                     + ' for ' + version['note']
            if version['productionStatus'] == 'ACTIVE':
                version_info['production_propertyVersion'] = str(version['propertyVersion'])
                version_info['production_propertyId'] = version['propertyId']
                version_info['production_groupId'] = version['groupId']
                version_info['production_contractId'] = version['contractId']
                version_info['production_edgeHostname'] = version['edgeHostname']
                if not version.get('note'):
                    version['note'] = 'no comments found'
                version_info['production_lastUpdate'] = version['updatedDate']\
                                                     + ' by ' + version['updatedByUser']\
                                                     + ' for ' + version['note']
        for k, v in version_info.items():
            if environment in k:
                print(k, ':', v)
        return version_info

    def download_config(self, propertyId, propertyVersion, contractId, groupId):
        """Download the property configuration"""
        print('\nDownloading the active version configuration ......')
        response = self.session.get(self.base_url + '/papi/v1/properties/' + propertyId + '/versions/'
                                    + propertyVersion + '/rules?contractId=' + contractId + '&groupId=' + groupId
                                    + '&validateRules=true&validateMode=fast&dryRun=true',
                                    headers={'PAPI-Use-Prefixes': 'true'})
        configuration = json.loads(response.text)
        print(response)
        return configuration

    def parse_config(self, hostname, rule):
        """Parse config to get origin"""
        if self.check_next:
            if rule['name'] == 'default':
                for behavior in rule['behaviors']:
                    if behavior['name'] == 'origin':
                        self.default_origin = behavior['options']
            if rule['name'] != 'default':
                criterias = rule['criteria']
                behaviors = rule['behaviors']
                if len(criterias) > 0 and len(behaviors) > 0:
                    for criteria in criterias:
                        if self.check_next:
                            if criteria['name'] == 'hostname' and hostname in criteria['options']['values']:
                                for behavior in behaviors:
                                    if self.check_next:
                                        if behavior['name'] == 'origin':
                                            self.custom_origin = behavior['options']
                                            self.check_next = False

            if self.check_next:
                if len(rule['children']) > 0:
                    for sub_rule in rule['children']:
                        self.parse_config(hostname, sub_rule)

    def check_rules(self, hostname, rule):
        """Read rules"""
        print("\nrule name:", rule['name'])
        behaviors = rule['behaviors']
        if rule['name'] == 'default':
            print('\tbehaviors:')
            for behavior in behaviors:
                for k, v in behavior.items():
                    print('\t\t',k, ':', v)
        if rule['name'] != 'default':
            criterias = rule['criteria']
            print('\tcriterias:')
            for criteria in criterias:
                for k, v in criteria.items():
                    print('\t\t',k, ':', v)
            print('\tbehaviors:')
            for behavior in behaviors:
                for k, v in behavior.items():
                    print('\t\t', k , ':', v)
        if len(rule['children']) > 0:
            for sub_rule in rule['children']:
                self.check_rules(hostname, sub_rule)

    def print_default_origin(self):
        for k, v in self.default_origin.items():
            print(k, ':', v)

    def print_custom_origin(self):
        for k, v in self.custom_origin.items():
            print(k, ':', v)

