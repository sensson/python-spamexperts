# Limitations

We are aware of the following issues/limitations in the SpamExperts API. We do
not always intend to work around them.

* destination/getroute - returns two semicolons before the port number, this
  can cause issues if you use it to create or update domains.
* domain/add - doesn't allow you to set the contact address.
* domain/exists - returns an error instead of `{"messages":[],"result":{"present":0}}`.
* domain/read - the read action is only available in `domainslist`.
* domaincontact/get - you can't get a domaincontact.
* domainuser/get - the read action is only available in `user`.
* emailusers - suddenly this controller is plural.
* emailusers/get - the read action is only available in `user`.
