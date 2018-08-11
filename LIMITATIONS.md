# Limitations

We are aware of the following issues/limitations in the SpamExperts API.

Controller    | Action      | Description
----------    | -------     | ------------
destination   | getroute    | Returns two semicolons before the port number.
domain        | add         | Doesn't allow you to set the contact address.
domain        | exists      | Returns an error instead of `{"messages":[],"result":{"present":0}}`.
domain        | read*       | The read action is only available in `domainslist`.
domain        |             | You cannot get or set domain settings.
domain        |             | You cannot get or set filter settings.
domaincontact | get*        | You cannot get a domaincontact.
domainuser    | get*        | This is only available in `user/list/domain`.
emailusers    |             | This controller is plural.
emailusers    | get*        | This is only available in `user/list/email`.
report        | get*        | You cannot get a report, only update settings.
user          | list        | Returns an error instead of an empty list.
user          | list/domain | The domain user e-mail address is available in `/user/get/id`.

\* This action doesn't exist.

We encourage you to raise a support request at [support@spamexperts.com](support@spamexperts.com)
if this blocks your development.
