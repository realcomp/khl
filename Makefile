PROJECT_DIR=$(shell pwd)
VENV_DIR?=$(PROJECT_DIR)/venv/
PIP?=$(VENV_DIR)/bin/pip
PYTHON?=$(VENV_DIR)/bin/python

all: virtualenv pip migrate test

virtualenv:
	virtualenv $(VENV_DIR)

pip: requirements

requirements:
	$(PIP) install -r $(PROJECT_DIR)/requirments.txt

migrate:
	$(PYTHON) $(PROJECT_DIR)/manage.py migrate

clean: clean_venv

clean_venv:
	rm -rf $(VENV_DIR)

test:
	$(PYTHON) $(PROJECT_DIR)/manage.py test --traceback

get_code:
	git pull origin master
	pip install -r requirments.txt
	python manage.py migrate

deploy:
	git pull origin master
	pip install -r requirments.txt
	python manage.py migrate
	python manage.py compilemessages
	python manage.py collectstatic --no-post-process --noinput
	sudo service nginx reload
	sudo supervisorctl restart sportomatics
	celery multi restart sportomatics_worker -B -A sportomatics --pidfile="/home/deploy/celery/%n.pid" --logfile="/home/deploy/celery/%n.log"

deploy_with_test: get_code test deploy