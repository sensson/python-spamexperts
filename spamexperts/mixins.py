from spamexperts.exceptions import ApiException


class AddressListMixin(object):
    def migrate_to(self, api_destination, params={}, **kwargs):
        '''Migrate address lists (whitelist/blacklist)

        api_destination - an instance of API.
        params - a dict having at least a 'domain'-key. 'ignore_list' is
                 optional'''

        address_params = {
            'SenderBlacklist': 'sender',
            'SenderWhitelist': 'sender',
            'RecipientWhitelist': 'recipient',
            'RecipientBlacklist': 'recipient',
        }

        if self.__class__.__name__ not in address_params:
            raise ApiException('AddressListMixin does not support {}'.format(
                self.__class__.__name__,
            ))

        address_list = self.read(params)
        controller = self.__class__(api=api_destination)

        results = []

        if len(address_list) > 0:
            for address in address_list:
                # The address key should only exist in Sender lists
                if 'address' in address:
                    address = address['address']

                # Ignore some addresses, useful as read() will always include
                # global addresses too. ignore_list will still be passed on
                # to the api but it will be ignored.
                if 'ignore_list' in kwargs:
                    if address in kwargs['ignore_list']:
                        continue

                try:
                    param = address_params[self.__class__.__name__]
                    params[param] = address
                    controller.create(params=params)
                    results.append({
                        'address': address,
                        'status': 'created',
                    })
                except ApiException:
                    results.append({
                        'address': address,
                        'status': 'exists',
                    })
                    continue

        return results
