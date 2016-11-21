.PHONY: test install run migrate update
test:
	coverage run --rcfile=.coveragerc manage.py test parser reports
	coverage report --rcfile=.coveragerc
	flake8 .

install:
	python3 setup.py install

migrate:
	python3 manage.py migrate

update:
	python3 manage.py updateentries

run:
	python3 manage.py runserver
