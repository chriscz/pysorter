# How to contribute  (Hacktoberfest)
To contribute to pysorter you must do the following:

1. Create an issue or comment on one, to indicate your interest in 
solving a problem
2. If the maintainer says it's fine, the issue will be assigned to you.
3. Fork the repository, and clone it to your local machine.
4. Always develop on a new branch. Basically your workflow for development
would look as follows:
```
git checkout develop
git checkout -b issue_78
# hack hack hack
git add --all .
git commit -a
git push origin issue_78 --set-upstream
```
5. Write some tests to ensure that you covered your code.
6. Run `python setup.py coverage` to see if all your tests pass.
Open `coverage_report/index.html` in your browser. 
7. Push yur branch to github
8. Create a pull-request for merging your branch
