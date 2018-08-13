# python-spamexperts

This is a Python interface to the SpamExperts API.

# Usage

```python
from spamexperts.api import API
from spamexperts.controllers import Destination

se = API(
        url='https://yourcluster/',
        username='username',
        password='secure',
        debug=True,
     )

destination = Destination(api=se)
print(destination.read(
    params={'domain': 'sensson.net'},
))
```

## Controllers

SpamExperts uses controllers and actions and so does our interface. Our
classes are specific and structured, whereas the API itself can be generic
and unstructured. Our classes are flexible and capable of routing requests
to different SpamExperts controllers whenever needed.

The `spamexperts.controller.Controller`-class supports all CRUD-methods. Each
controller has the following methods available:

* `create(params)`
* `read(params)`
* `update(params)`
* `delete(params)`

`params` is expected to be a dictionary holding key/value information that
you want to pass to the API. More information on these parameters can be
found in the [SpamExperts API documentation](https://api.antispamcloud.com/api/help.php).

If SpamExperts does not include a relevant action the method is still available
but raises an exception when used.

Additional methods may be added to support functionality that does not fit in a
CRUD-method. For example, to recover a password for a user.

## Current controllers

For a list of available controllers and their methods please see
[spamexperts/controllers.py](spamexperts/controllers.py).

# Migrations

Unfortunately, SpamExperts doesn't allow you to migrate specific domains to
other clusters without a lot of manual work. We intend to solve that with a
custom migration method.

Most controllers have a `migrate_to`-method available. For example:

```python
from spamexperts.controllers import Domain

domain = 'sensson.net'

migration = Domain(api=api_source).migrate_to(
    api_destination=api_destination,
    params={
      'domain': domain,
    }
)
```

This example assumes you have set both `api_source` and `api_destination` to an
API object. This will migrate the domain without any other data to the new
cluster. It's similar as adding a domain through the web interface.

We can do more though.

`Domain.migrate_to` accepts `kwargs`. Why kwargs and not actual keywords? We
try to keep our methods similar across all controllers. There are two important
arguments `Domain.migrate_to` accepts:

* `migrate_dependencies` - boolean, either True or False, defaults to False.
* `ignore_list` - list, empty by default.

`migrate_dependencies` will migrate all data that we think is related to the
domain. We're still expanding this to be as complete as possible. If you
migrate dependencies too, be sure to read the output as it includes new
passwords for created users.

`ignore_list` is a list of addresses that you want to ignore during your
migration. This can be a requirement if the old cluster contains global
whitelists or blacklists that you don't want to migrate.

# Error handling

* If a method is not supported it will raise an `ActionException`.
* If SpamExperts returns an error it will raise an `ApiException`.
* If a controller is not supported it will raise a `ControllerException`.

The `ApiException` will include the endpoint that returned an error. You can
use this to find more information in the [SpamExperts API documentation](https://api.antispamcloud.com/api/help.php).

# Limitations

This module requires Python 3.6.

We are aware of some gaps in the SpamExperts API. All known limitations are
documented in [LIMITATIONS.md](LIMITATIONS.md). If you find any others, feel
free to report them, raise a pull request for it or send a message to
SpamExperts.

# Tests

Sorry, this code doesn't come with tests yet.
