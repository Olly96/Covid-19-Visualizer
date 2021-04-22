#INFO 6205 Course Project : Covid-19-Visualizer (Group 16)

Instructions to setup Enviroment

Basic requirements: Python3 and pip3

pip3 install pipenv

clone the repo and open terminal in repo

pipenv --python 3.9
pipenv install

Once the installation is done we open pipenv shell we consists our virtual environment
pipenv shell
python main.py

If we update config.py then we need to run

python config.py (This will generate the new dev.ini file)

To Run Unit tests and view coverage

coverage run -m --source src unittest discover (By line)
coverage run -m --branch --source src unittest discover (Branch Coverage)

coverage report -m

Link for the video:

https://web.microsoftstream.com/video/c2a9e751-75d0-4495-8b2c-fe4e78e5f184
