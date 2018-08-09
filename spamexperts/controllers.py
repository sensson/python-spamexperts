from spamexperts.api import API
from spamexperts.exceptions import ActionException
from spamexperts.exceptions import ApiException
from spamexperts.exceptions import ControllerException


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


class Domains(Controller):
    controller = 'domainslist'
    action_create = 'add'
    action_read = 'get'


class Domain(Controller):
    controller = 'domain'
    action_read = 'exists'


class Destination(Domain):
    action_read = 'getroute'
    action_update = 'edit'


class SenderBlacklist(Domain):
    action_create = 'blacklistsender'
    action_read = 'senderblacklist'
    action_delete = 'unblacklistsender'


class SenderWhitelist(Domain):
    action_create = 'whitelistsender'
    action_read = 'senderwhitelist'
    action_delete = 'unwhitelistsender'


class RecipientBlacklist(Domain):
    action_create = 'blacklistrecipient'
    action_read = 'recipientblacklist'
    action_delete = 'unblacklistrecipient'


class RecipientWhitelist(Domain):
    action_create = 'whitelistrecipient'
    action_read = 'recipientwhitelist'
    action_delete = 'unwhitelistrecipient'


class DomainAlias(Controller):
    controller = 'domainalias'
    action_create = 'add'
    action_read = 'list'
    action_delete = 'remove'


class DomainUser(Controller):
    controller = 'domainuser'
    action_create = 'add'
    action_delete = 'remove'

    def read(self, params={}):
        '''The dmoainuser controller in SpamExperts has no read method. This is
        available in the user controller. Override read to call a different
        controller. This call has no parameters'''
        params['role'] = 'domain'
        return self.action(params, controller='user', action='list')


class EmailAlias(Controller):
    controller = 'emailalias'
    action_create = 'add'
    action_read = 'list'
    action_delete = 'remove'


class EmailUser(Controller):
    controller = 'emailusers'
    action_create = 'add'
    action_delete = 'remove'

    def read(self, params={}):
        '''The emailusers controller in SpamExperts has no read method. This is
        available in the user controller. Override read to call a different
        controller and add the only supported parameter.'''

        params = {
            'role': 'email',
            'domain': params['domain'],
        }

        return self.action(params, controller='user', action='list')
