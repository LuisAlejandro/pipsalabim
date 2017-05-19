================
Maintainer Guide
================

If you are reading this, you probably forgot how to release a new version. Keep
reading.

Making a new release
--------------------

1. Start your project with a cookiecutter template.
2. Start your git flow workflow::

    git flow init

3. Create a new milestone in GitHub. Plan the features of your new release. Assign
existing bugs to your new milestone.
4. Start a new feature::

    git flow feature start <feature name>

5. Code, code and code. More coding. Fuck it up several times. Push to feature
branch. Watch Travis go red. Write unit tests. Watch Travis go red again. Don't
leave uncommitted changes.
6. Finish your feature::

    git flow feature finish <feature name>

7. Repeat 4-6 for every other feature you have planned for this release.
8. When you're done with the features and ready to publish, start a new release::

    git flow release start <release number>

9. Bump your version (check everything before next step)::

    bumpversion --no-commit --new-version <release number> patch

10. Update your changelog (edit HISTORY.rst after to customize)::

    gitchangelog > HISTORY.rst

11. Commit your changes to version files and changelog::

    git commit -aS -m "Updating Changelog and version."

12. Delete the tag made by bumpversion::

    git tag -d <release number>

13. Finish your release::

    git flow release finish -s -p <release number>

14. Push your tags::

    git push --tags

15. Draft a new release in GitHub (based on the new version tag) and include
a description. Also pick a codename because it makes you cool.

16. Close the milestone in GitHub.

17. Publish your new version to PyPI::

    python setup.py sdist upload

18. Write about your new version in your blog. Tweet it, post it on facebook.

Making a new hotfix
-------------------

1. Create a new milestone in GitHub. Assign existing bugs to your new milestone.
2. Start a new hotfix::

    git flow hotfix start <new version>

3. Code your hotfix.
4. Bump your version (check everything before next step)::

    bumpversion --no-commit --new-version <new version> patch

5. Update your changelog (edit HISTORY.rst after to customize)::

    gitchangelog > HISTORY.rst

6. Commit your changes to version files and changelog::

    git commit -aS -m "Updating Changelog and version."

7. Delete the tag made by bumpversion::

    git tag -d <new version>

8. Finish your hotfix::

    git flow hotfix finish -s -p <new version>

9. Push your tags::

    git push --tags

10. Draft a new release in GitHub (based on the new version tag) and include
a description. Don't change the codename if it is a hotfix.

11. Close the milestone in GitHub.

12. Publish your new version to PyPI::

    python setup.py sdist upload

13. Write about your new version in your blog. Tweet it, post it on facebook.
