# git-hooks

Some code to make some useful global hooks work properly globally with easy
updating.

# Features

* setting `JIRA_ISSUE` in environment will ensure commit message contains
  the `JIRA_ISSUE` in it

# Install

Simple:

    ...

Expert:

    mkdir ~/.git_template
    git clone https://github.com/dlamotte/git-hooks.git ~/.git_template/hooks
    cd ~/.git_template/hooks
    ./make-hooks
    git config --global init.templateDir ~/.git_template

## Almost there

All future cloned repositories will now have your global hooks installed
automatically.  For any repositories you already have cloned and want updated,
you need to re-initialize them.

    cd path/to/sandbox/
    ls -ld .git/        # make sure .git/ is in your current working directory
    git init            # re-initialize the clone
