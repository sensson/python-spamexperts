# python-spamexperts

This is a Python interface to the SpamExperts API.

The SpamExperts API is not machine-friendly. We have implemented CRUD (create,
read, update and delete) functions for the API calls SpamExperts supports.

Every class supports 4 methods:

* create(params)
* read(params)
* update(params)
* delete(params)

# Usage

```python
from spamexperts.api import API
from spamexperts import controllers

se = API(
        url='https://yourcluster/',
        username='username',
        password='secure',
     )

destination = controllers.Destination(api=se)
print(destination.read(
   params={'domain': 'sensson.net'},
))
```

`params` is expected to be a dictionary holding key/value information that
you want to pass to the API. More information on these parameters can be
found in the SpamExperts API documentation.

`debug` is available in the API-class.

# Error handling

* If a method is not supported it will raise an `ActionException`.
* If SpamExperts returns an error it will raise an `ApiException`.
* If a controller is not supported it will raise a `ControllerException`.

The `ApiException` will include the endpoint that returned an error. You can
use this to find more information in the SpamExperts API documentation.

# Tests

Sorry, this code doesn't come with tests yet.
