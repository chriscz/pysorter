# How to contribute
So you'd like to contribute to pysorter? There's 
a short procedure you'll need to follow before tackling an issue.

1. Create a new issue for the functionality, or
2. Comment on an existing issue

Now wait for the maintainer to reply in the affirmative. Then you can 
begin hacking!

## Setting up your environment
1. Fork the repository, and clone it to your  machine.
2. Create a virtual environment using one of the supported Python versions. 
    ```
    python3 -m venv venv
    ```
3. Activate the virtual environment:
    ```
    source venv/bin/activate
    ```
4. To ease development and testing, you can install pysorter as [editable][editable]. 
   `cd` into `pysorter/` and exexute the following
    ```
    pip install -e .
    pip install -e .[test]
    pip install -e .[develop]
    ```

### Developing
1. Activate your virtual environment
2. Create a new branch to develop on
```
git checkout -b issue_78 develop
```
3. Write some code
4. Write some tests and run them
```
python3 setup.py test 
```
5. Check your coverage
```
python3 setup.py coverage
# open the coverage_report/index.html in your browser
```
6. Commit your changes and push them up (many smaller commits are better than one big one) 
```
git push origin issue_78 --set-upstream
```
7. Create a pull request
8. Wait for feedback from the maintainer.

### General submission disclaimer
1. The coverage status should stay at *100%*


[editable]: http://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/pip.html#installing-from-a-vcs
