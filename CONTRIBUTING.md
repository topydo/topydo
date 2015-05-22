If you're reading this, you may have interest in enhancing topydo. Thank you!

Please read the following guidelines to get your enhancement / bug fixes
smoothly into topydo:

* This Github page defaults to the **stable** branch which is for **bug fixes
  only**. If you would like to add a new feature, make sure to make a Pull
  Request on the `master` branch.
* Run tests with:

        ./run-tests.sh [python2|python3]

  Obviously, I won't accept anything that makes the tests fail. When you submit
  a Pull Request, Travis CI will automatically run all tests for various Python
  versions, but it's better if you run the tests locally first.

  Make sure you have the `mock` package installed if you test on a Python
  version older than 3.3.
* Add tests for your change(s):
  * Bugfixes: add a testcase that covers your bugfix, so the bug won't happen
    ever again.
  * Features: add testcases that checks various inputs and outputs of your
    feature. Be creative in trying to break the feature you've just implemented.
* Use descriptive commit messages.

### Coding style

* Please try to adhere to the coding style dictated by `pylint` as much
  possible. I won't be very picky about long lines, but please try to avoid
  them.
* I strongly prefer simple and short functions, doing only one thing. I'll
  request you to refactor functions with massive indentation or don't fit
  otherwise on a screen.
