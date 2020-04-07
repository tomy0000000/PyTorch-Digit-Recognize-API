# PyTorch Digit Recognize API

A simple web server which accept single-digit image and output recognized result.

Built with Flask and PyTorch.

## Install

* Clone Repo

```bash
git clone https://github.com/tomy0000000/PyTorch-Digit-Recognizer-API.git
```

* Install Environment

```bash
# Standard Install
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt

# Using Pipenv (with requirements.txt)
# Since urlencoded-wheel-dependencies is malfunctioning (pipenv #4089)
# Pipfile will be back after patch is released 
pipenv install
```

* Configure Flask

```bash
export FLASK_APP="src"
export FLASK_ENV=development
```

* Run Server

```bash
flask run
```

## Work in Progress

- [x] Basic flask app
- [x] flask app with pre-trained model api
- [ ] self-trained model
- [ ] flask app with self-trained model api
- [ ] HTML Interface for webcam

## References & Credits

* [aaron-xichen/pytorch-playground](https://github.com/aaron-xichen/pytorch-playground) (Pre-trained Model)
* [avinassh/pytorch-flask-api-heroku](https://github.com/avinassh/pytorch-flask-api-heroku) (HTML Interface)
* [Deploying PyTorch in Python via a REST API with Flask](https://pytorch.org/tutorials/intermediate/flask_rest_api_tutorial.html)

