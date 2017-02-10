# auxo
Little agents for finding and reporting.

## Dependencies

* Python 3.2
* httplib2
* Beautiful Soup 4 (only for HTML parsing agents)

## Tests

Run the tests with the `bin/auxo_test.sh` script. They should all pass if
you have all the dependencies.

## Examples

There is an example python script `bin/auxo` which demonstrates some of
the typical usage.

You can run it with the `bin/auxo_runner.sh` wrapper _if_ you supply a
file `bin/auxo_runner.env` which defines all the required environment
variables.

The most useful agents are:

* HashWebAgent - checks for any changes in a web page.
* KinchAgent - checks the ranking and score of a person on the Kinch Ranks.

