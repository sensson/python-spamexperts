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
domainuser    | get*        | This is only available in `user`.
emailusers    |             | This controller is plural.
emailusers    | get*        | This is only available in `user`.
report        | get*        | You cannot get a report, only update settings.

\* This action doesn't exist.

We encourage you to raise a support request at [support@spamexperts.com](support@spamexperts.com)
if this blocks your development.
