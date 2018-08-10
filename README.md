# python-spamexperts

This is a Python interface to the SpamExperts API.

# Usage

```python
from spamexperts.api import API
from spamexperts import controllers

se = API(
        url='https://yourcluster/',
        username='username',
        password='secure',
        debug=True,
     )

destination = controllers.Destination(api=se)
print(destination.read(
   params={'domain': 'sensson.net'},
))
```

## Controllers

SpamExperts uses controllers and actions and so does our interface. Our
classes are specific and structured, whereas SpamExperts can be generic
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
found in the SpamExperts API documentation.

If SpamExperts does not include a relevant action the method is still available
but raises an exception when used.

Additional methods may be added to support functionality that does not fit in a
CRUD-method. For example, to recover a password for a user.

## Current controllers

For a list of available controllers please see
[spamexperts/controllers.py](spamexperts/controllers.py).

# Error handling

* If a method is not supported it will raise an `ActionException`.
* If SpamExperts returns an error it will raise an `ApiException`.
* If a controller is not supported it will raise a `ControllerException`.

The `ApiException` will include the endpoint that returned an error. You can
use this to find more information in the SpamExperts API documentation.

# Tests

Sorry, this code doesn't come with tests yet.
