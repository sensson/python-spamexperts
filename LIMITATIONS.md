# Limitations

We are aware of the following issues/limitations in the SpamExperts API. They
may affect our implementation in unexpected ways.

Controller    | Action      | Description
----------    | -------     | ------------
destination   | getroute    | Returns two semicolons before the port number.
domain        | add         | Doesn't allow you to set the contact address.
domain        | exists      | Returns an error instead of `{"messages":[],"result":{"present":0}}`.
domain        | read*       | The read action is only available in `domainslist`.
domaincontact | get*        | You cannot get a domaincontact.
domainuser    | get*        | This is only available in `user`.
emailusers    |             | This controller is plural.
emailusers    | get*        | This is only available in `user`.

\* This action doesn't exist.
