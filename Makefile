.PHONY: test install run docs
test:
	coverage run --rcfile=.coveragerc manage.py test parser reports
	coverage report --rcfile=.coveragerc
	flake8 .

install:
	python3 setup.py install

run:
	python3 manage.py runserver
