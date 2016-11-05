# How to contribute
To contribute to pysorter you must do the following:

1. Create an issue or comment on one, to indicate your interest in 
solving a problem
2. If the maintainer says it's fine, the issue will be assigned to you.
3. Fork the repository, and clone it to your local machine.
4. Create a virtual environment using one of the supported Python versions. 
Here are *three* example commands:

    ```
    $ python2 -m virtualenv venv
    ```
or
    ```
    $ python3 -m virtualenv venv
    ```
or
    ```
    $ virtualenv venv
    ```
5. Activate the virtual environment:
    ```
    $ source venv/bin/activate
    ```
6. Inside the `pysorter/` direcory, execute the following
```
    $ pip install -e .
    $ pip install -e .[test]
    $ pip install -e .[develop]
```

45 Always develop on a new branch. Your workflow for development
would look as follows:
```
    $ git checkout develop
    $ git checkout -b issue_78
# 1. hack hack hack
# 2. add tests

# test your code
    $ python setup.py test 

# check your coverage 
    $ python setup.py coverage

# submit your changes
    $ git add --all .
    $ git commit -a
    $ git push origin issue_78 --set-upstream
```
6. Write some tests to ensure that the code coverage for the project isn't lowered.
7. Run `python setup.py coverage` to see that your tests pass.  Open `coverage_report/index.html` for
a full coverage report.
8. Push your branch to github.
9. Create a pull-request for merging your branch.
10. Wait for feedback from the maintainer.
