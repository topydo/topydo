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
  ask you to refactor functions with massive indentation or don't fit
  otherwise on a screen.

### Testing

* First make sure to have the prerequisites installed to perform the tests:

        pip install .[test]

* Then, run the tests with:

        green -r

  Obviously, I won't accept anything that makes the tests fail. When you submit
  a Pull Request, Travis CI will automatically run all tests for various Python
  versions, but it's better if you run the tests locally first.
* Travis CI will also run `pylint` and fail when new errors are introduced. You
  may want to add a `pre-push` script to your topydo clone before pushing to
  Github (.git/hooks/pre-push):

       #!/bin/sh
       remote="$1"

       if [ $remote = "origin" ]; then
           if ! green; then
               exit 1
           fi
      
          if ! python3 -m pylint --errors-only topydo test; then
              exit 1
          fi
      fi
      
      exit 0

  Make sure to run `chmod +x .git/hooks/pre-push` to activate the hook.

* Add tests for your change(s):
  * Bugfixes: add a test case that covers your bugfix, so the bug won't happen
    ever again.
  * Features: add test cases that checks various inputs and outputs of your
    feature. Be creative in trying to break the feature you've just implemented.
* Check the test coverage of your contributed code, in particular if you touched
  code in the topydo.lib or topydo.command packages:

      coverage report -m

  Or alternatively, for a more friendly output, run:

      coverage html

  which will generate annotated files in the *htmlcov* folder. The new code
  should be marked green (i.e. covered).
  
  When you create a Pull Request, code coverage will be automatically checked
  and reported by [Codecov.io](https://codecov.io/github/topydo/topydo).
