# Limitations

We are aware of the following issues/limitations in the SpamExperts API.

Controller    | Action      | Description
----------    | -------     | ------------
domain        | getroute    | Returns two semicolons before the port number.
domain        | add         | Doesn't allow you to set the contact address.
domain        | exists      | Returns an error instead of `{"messages":[],"result":{"present":0}}`.
domain        | read*       | The read action is only available in `domainslist`.
domain        |             | You cannot get or set domain settings.
domain        |             | You cannot get or set filter settings.
domain        |             | Whitelists and blacklists do not allow you to set a local part.
domain        | recipientwhitelist | The output is different from senderwhitelist.
domain        | whitelistrecipient | Doesn't return a notification if the address exists.
domain        | senderwhitelist    | Includes the global whitelist too.
domaincontact | get*        | You cannot get a domaincontact.
domainuser    | get*        | This is only available in `user/list/domain`.
emailusers    |             | This controller is plural.
emailusers    | get*        | This is only available in `user/list/email`.
report        | get*        | You cannot get a report, only update settings.
user          | list/email  | Returns an error instead of an empty list.
user          | list/domain | The domain user e-mail address is available in `/user/get/id`.

\* This action doesn't exist.

We encourage you to raise a support request at [support@spamexperts.com](support@spamexperts.com)
if this blocks your development.

# General concerns

The API does not always accept the data it exports. As a result, you need
to process data first before sending it back to the API (e.g. during a
migration). E.g. destinations are exported with two semicolons between
the host/ip and port, it needs a single semicolon when adding it.

The API does not accept JSON-payloads and passes ALL data through
urls, including passwords when creating users. Although urls are SSL
encrypted this data can be logged by either a load balancer or API
server. JSON-payloads can be logged too, but it's uncommon.

The API does not expose data when you expect it to. For example, the
`user`-controller can read user data but can't change it. The `domainuser`
and `emailusers`-controllers can change data but can't read it.

The API uses random data structures. If you ask the API if a domain exists,
it returns an error if it doesn't. It returns structured data when it does
exist. This also happens when you try to list email users.

The API almost always returns a 200 OK status. This also happens if it returns
an error. Combined with the random data structures this results in unreliable
error handling.
