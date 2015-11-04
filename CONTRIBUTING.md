If you're reading this, you may have interest in enhancing topydo. Thank you!

Please read the following guidelines to get your enhancement / bug fixes
smoothly into topydo.

### General

* Use descriptive commit messages. The post
  [How to write a commit message](http://chris.beams.io/posts/git-commit/) by
  Chris Beams has some good guidelines.

### Coding style

* Please try to adhere to the coding style dictated by `pylint` as much
  possible. I won't be very picky about long lines, but please try to avoid
  them.
* I strongly prefer simple and short functions, doing only one thing. I'll
  request you to refactor functions with massive indentation or don't fit
  otherwise on a screen.

### Testing

* Run tests with:

        green

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
* Check the test coverage of your contributed code, in particular if you
  touched code in the topydo.lib or topydo.command packages:

      pip install coverage
      coverage run setup.py test
      coverage report

  Or alternatively, for a more friendly output, run:

      coverage html

  Which will generate annotated files in the *htmlcov* folder. The new code
  should be marked green (i.e. covered).
