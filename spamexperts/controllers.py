import json
import secrets
import string
from spamexperts.api import API
from spamexperts.exceptions import ActionException
from spamexperts.exceptions import ApiException
from spamexperts.exceptions import ControllerException
from spamexperts.mixins import AddressListMixin


class Controller(object):
    controller = None
    action_create = None
    action_read = None
    action_update = None
    action_delete = None

    def __init__(self, api):
        if not isinstance(api, API):
            raise ApiException('api does not contain any credentials')

        self.api = api

    def action(self, params={}, controller=None, action=None):
        if self.controller is None and controller is None:
            raise ControllerException("controller is required")

        if action is None:
            raise ActionException("action is not implemented for this class".
                                  format(action))

        if controller is None:
            controller = self.controller

        return self.api.get(
            controller,
            action,
            params,
        )

    def create(self, params={}):
        return self.action(params, action=self.action_create)

    def read(self, params={}):
        return self.action(params, action=self.action_read)

    def update(self, params={}):
        return self.action(params, action=self.action_update)

    def delete(self, params={}):
        return self.action(params, action=self.action_delete)

    def generate_password(self):
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for i in range(20))


class Domain(Controller):
    controller = 'domain'
    action_create = 'add'

    def read(self, params={}):
        # See LIMITATIONS.md: domain/read
        return self.action(params, controller='domainslist', action='get')

    def exists(self, params={}):
        # See LIMITATIONS.md: domain/exists
        try:
            self.action(params, action='exists')
            return True
        except ApiException:
            return False

    def migrate_to(self, api_destination, params={}, **kwargs):
        '''Migrate a domain -- this doesn't include all settings by
        default yet.

        api_destination - an instance of API.
        params - a dict having at least a 'domain'-key.
        '''

        if self.__class__(api=api_destination).exists(params) is False:
            self.__class__(api=api_destination).create(params)

            result = {
                'domain': params['domain'],
                'status': 'created',
            }
        else:
            result = {
                'domain': params['domain'],
                'status': 'exists',
            }

        if 'migrate_dependencies' in kwargs:
            # Migrate all other domain related data too when migrating a Domain
            migration_controllers = [
                Destination,
                DomainAlias,
                DomainAdminContact,
                EmailUser,
                EmailAlias,
                SenderBlacklist,
                SenderWhitelist,
                RecipientBlacklist,
                RecipientWhitelist,
            ]

            if kwargs['migrate_dependencies'] is True:
                migration_results = {}

                # Add the result of the Domain migration
                migration_results[self.__class__.__name__] = result

                for migration_controller in migration_controllers:
                    # Set up a controller based on migration_controller
                    controller = migration_controller(self.api)

                    # Run the migration
                    migration_result = controller.migrate_to(
                        api_destination,
                        # You would assume params can be used here too, but
                        # as it turned out to leak the adjusted params
                        # variable from the controller, we override it.
                        {
                            'domain': params['domain']
                        },
                        **kwargs
                    )

                    controller_name = migration_controller.__name__
                    migration_results[controller_name] = migration_result

                return migration_results

        return result


class Destination(Controller):
    controller = 'domain'
    action_read = 'getroute'
    action_update = 'edit'

    def migrate_to(self, api_destination, params={}, **kwargs):
        '''Migrate destinations

        api_destination - an instance of API.
        params - a dict having at least a 'domain'-key.'''
        destinations = self.read(params)
        destinations = json.dumps(destinations).replace("::", ":")

        # Create routes at api_destination
        params['destinations'] = destinations
        self.__class__(api=api_destination).update(params=params)

        return {
            'destinations': json.loads(destinations),
            'status': 'updated',
        }


class SenderBlacklist(Controller, AddressListMixin):
    controller = 'domain'
    action_create = 'blacklistsender'
    action_read = 'senderblacklist'
    action_delete = 'unblacklistsender'


class SenderWhitelist(Controller, AddressListMixin):
    controller = 'domain'
    action_create = 'whitelistsender'
    action_read = 'senderwhitelist'
    action_delete = 'unwhitelistsender'


class RecipientBlacklist(Controller, AddressListMixin):
    controller = 'domain'
    action_create = 'blacklistrecipient'
    action_read = 'recipientblacklist'
    action_delete = 'unblacklistrecipient'


class RecipientWhitelist(Controller, AddressListMixin):
    controller = 'domain'
    action_create = 'whitelistrecipient'
    action_read = 'recipientwhitelist'
    action_delete = 'unwhitelistrecipient'


class DomainAlias(Controller):
    controller = 'domainalias'
    action_create = 'add'
    action_read = 'list'
    action_delete = 'remove'

    def migrate_to(self, api_destination, params={}, **kwargs):
        '''Migrate domain aliases

        api_destination - an instance of API.
        params - a dict having at least a 'domain'-key.'''

        aliases = self.read(params)
        results = []
        if len(aliases) > 0:
            for alias in aliases:
                try:
                    params['alias'] = alias
                    self.__class__(api=api_destination).create(params)
                    results.append({
                        'alias': alias,
                        'status': 'created',
                    })
                except ApiException:
                    results.append({
                        'alias': alias,
                        'status': 'exists',
                    })
                    continue

        return results


class DomainUser(Controller):
    controller = 'domainuser'
    action_create = 'add'
    action_delete = 'remove'

    def read(self, params={}):
        # See LIMITATIONS.md: domainuser/get
        params['role'] = 'domain'
        domain_users = []

        # See LIMITATIONS.md: user/list/domain
        for user in self.action(params, controller='user', action='list'):
            domain_user_data = self.action(
                controller='user',
                action='get',
                params={
                    'id': user['id'],
                }
            )

            user['email'] = domain_user_data['email']
            domain_users.append(user)

        return domain_users


class DomainAdminContact(Controller):
    controller = 'domainadmincontact'
    action_create = 'set'
    action_read = 'get'
    action_update = 'set'

    def migrate_to(self, api_destination, params={}, **kwargs):
        '''Migrate the domain admin contact

        api_destination - an instance of API.
        params - a dict having at least a 'domain'-key.'''
        admin_contact = self.read(params)
        params['email'] = admin_contact
        self.__class__(api=api_destination).update(params)
        return {
            'admin_contact': admin_contact,
            'status': 'updated'
        }


class EmailAlias(Controller):
    controller = 'emailalias'
    action_create = 'add'
    action_read = 'list'
    action_delete = 'remove'

    def migrate_to(self, api_destination, params={}, **kwargs):
        '''Migrate email aliases

        api_destination - an instance of API.
        params - a dict having at least a 'domain'-key.'''

        aliases = self.read(params)
        results = []

        if len(aliases) > 0:
            for alias in aliases:
                try:
                    params['localpart'] = alias['email'].split('@')[0]
                    params['alias'] = alias['alias'].split('@')[0]
                    self.__class__(api=api_destination).create(params)
                    results.append({
                        'localpart': params['localpart'],
                        'alias': params['alias'],
                        'status': 'created',
                    })
                except ApiException:
                    results.append({
                        'localpart': params['localpart'],
                        'alias': params['alias'],
                        'status': 'exists',
                    })
                    continue

        return results


class EmailUser(Controller):
    controller = 'emailusers'
    action_create = 'add'
    action_delete = 'remove'

    def read(self, params={}):
        # See LIMITATIONS.md: emailusers/get
        params['role'] = 'email'

        # See LIMITATIONS.md: users/list/email
        try:
            return self.action(params, controller='user', action='list')
        except ApiException:
            return []

    def migrate_to(self, api_destination, params={}, **kwargs):
        '''Migrate email users

        api_destination - an instance of API.
        params - a dict having at least a 'domain'-key.

        returns a list of created email users and their passwords'''

        results = []
        users = self.read(params)

        if len(users) > 0:
            for user in users:
                try:
                    params['username'] = user['username'].split('@')[0]
                    params['password'] = self.generate_password()
                    self.__class__(api=api_destination).create(params)
                    results.append({
                        'username': params['username'],
                        'password': params['password'],
                        'status': 'created',
                    })
                except ApiException:
                    results.append({
                        'username': params['username'],
                        'status': 'exists',
                    })
                    continue

        return results
