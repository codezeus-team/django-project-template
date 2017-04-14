# {{project_name|title}}

The following project provides an excellent start for you to begin a Django
project with a modern frontend build kit enabled. By using this project
template, you will be able to jump directly into your application without
worrying about the small details in setting things up. Out of the box, you'll
have the following features enabled:

- Django 1.11.*: The latest stable version of [Django](https://www.djangoproject.com/)
- User authentication, authorization, and management ready to go
- User profiles with support for an Avatar
- Smart environment specific configuration
- Testing with [py.test](http://pytest.org/latest/) and coverage testing with Python coverage
- [SCSS](http://sass-lang.com/) for frontend efficiency
- Build script using [Gulp](http://gulpjs.com/)
- Browser [LiveReload](https://www.npmjs.com/package/livereload) for .js, .scss, and Django Template files
- Templates written in [Bootstrap 3](http://getbootstrap.com/) with [Crispy Forms](https://github.com/maraujop/django-crispy-forms) support for forms

All of this is ready to go and will be loaded on your first `runserver` command. {% comment %}

---

#Contents
- [Getting Started](#getting-started)
  - [Set up your environment](#set-up-your-environment)
  -  [Automated Installation](#automated-installation) - **Recommended**
  -  [Manual Installation](#manual-installation)
      - [Install Django](#install-django)
      - [Use Project Template](#use-project-template)
- [Development Notes](#development-notes)
  - [Running the Project](#running-the-project)
  - [Editing the Settings](#editing-the-settings)
    - [Django Settings](#django-settings)
    - [Gulp Config](#gulp-config)
    - [Gulp Tasks](#gulp-tasks) - **Recommended**
  - [Running Tests](#running-tests)
  - [Utility Scripts](#utility-scripts)
    - [Generate a 32-Character Secret String](#generate-a-32-character-secret-string)

---

##Getting Started

###Set up your environment

Before getting anything done, you need to start by setting up your working
directory. We recommend virtualenv and virtualenvwrapper for this process and
a detailed introduction can be found [here](https://github.com/codezeus/virtualenv-setup).

Once you have this setup, you're ready to install the dependencies. Depending
on your operating system, you will need the following dependencies for this
project (apt-get used for example):

```
sudo apt-get install build-essential libssl-dev libffi-dev python-dev libjpeg-dev libjpeg8-dev
```

###Automated Installation

If you are using virtualenv and virtualenvwrapper, you can automate the setup
process by using our [template hook](https://github.com/codezeus/virtualenvwrapper.codezeus).
This gives the added benefit of creating future projects much faster as well.
The steps are outlined in the repository or can be followed below. First,
install our hook globally:

```
pip install virtualenvwrapper.codezeus
```

Then any project you want to start with this template can be created running:

```
mkproject -t codezeus_django SITE_NAME
```

###Manual Installation

If you prefer installing the project manually, the following steps will get
everthing done for you.

####Install Django

Using pip, we can install Django itself in order to use the `startproject`
command. We can do this by running:

```
pip install Django==1.11
```

This will build Django into our virtualenv and give us full access to the
management commands.

{% endcomment %}

####Use Project Template

With Django we can now use this template to build our skeleton project. We do
so by running (NOTE: Change the `project_name` portion of the following
command to your project name.):

```
django-admin.py startproject --template=https://github.com/codezeus/django-project-template/archive/master.zip --extension=py,gitignore,coveragerc,json,md,sh,js,example,ini --name=Makefile,postactivate project_name .
```

This will clone the repo and build the skeleton into the current working
directory. Once cloned, you can run the Make script to finish the setup:

```
make init
```

##Development Notes

The following notes detail how we can work with this project.

###Running the Project

When working with this application, there is a frontend and backend which can
interact with each other and allow a very smooth development experience. It's
best to have two terminal buffers open at once. In our first terminal, we
will want to run Django:

```
python manage.py runserver_plus
```

This will spawn the development server at `127.0.0.1:8000`. Moving to the next
terminal, we will want to run Gulp to watch our files:

```
gulp
```

The default Gulp task is to watch. This task will build the application
with Browserify, Compile SASS files, Compile JS files, gather Third
Party CSS and Fonts, listen for changes to SCSS, JavaScript, and Django
Template files and create a proxy at `127.0.0.1:8001`. Upon change, the server
will reload with BrowserSync.

###Editing the Settings

In the case that you want to change settings, edit the frontend things, or
customize it, the following guide will help.

####Django Settings

The Django settings are located in the `{{project_name}}/settings/` directory. They
inherit from one another with the final output being:

```
      -- Development --
     /                  \
Base ---  Production  --- Local
     \                  /
      --   Staging   --
```

The three centerpieces are interchangable based on the current environment you
are working in. In most cases, you will edit an environment file. The
`local.py` file will be for all secret variables as it is referenced in the
`.gitignore`.

####Gulp Config

The Gulp master config is a JavaScript Object that lives in `gulp/config.js`.
In here, we have a reference to all build paths which should all just work.
All active development for the frontend should be done within the
`{{project_name}}/dev/` directory. If you want to add any third-party scripts,
they should exist in the `{{project_name}}/static/` directory and included in
the base template file (`{{project_name}}/templates.base.html`).

###Gulp Tasks

The following Gulp tasks can all be run:

```
gulp                      - Will run watcher
gulp build                - Will build dependencies and run watchify
gulp build --production   - Will build dependencies and exit on finish
gulp browserify           - Will only run browserify
gulp javascript           - Will only compile JS files
gulp sass                 - Will only compile scss into css
gulp templates            - Will only reload browsersync
gulp watch                - Will run watcher
```

Typically, you should stick with only two commands: `gulp` and `gulp build
--production`. These tasks will be most efficient.

##Running Tests

Tests are currently ready for Python code based on pytest and coverage. We are
using [Factory Boy](http://factoryboy.readthedocs.io/en/latest/) for text
fixtures. To run just the test suite:

```
py.test
```

In order to run the tests and get a coverage report:

```
make test
```

These two tasks will give you a detailed output of the Python code.

##Utility Scripts

A few utility scripts are provided via the Makefile. The following commands are
available:

###Generate a 32-Character Secret String

This is good to use for a Secret key or other random hashes.

```
make secret
```
