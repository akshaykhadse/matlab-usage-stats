# Matlab Usage Statistics
[![Build Status](https://travis-ci.org/akshaykhadse/matlab-usage-stats.svg?branch=master)](https://travis-ci.org/akshaykhadse/matlab-usage-stats)
[![Coverage Status](https://coveralls.io/repos/github/akshaykhadse/matlab-usage-stats/badge.svg?branch=master)](https://coveralls.io/github/akshaykhadse/matlab-usage-stats?branch=master)
[![Documentation Status](https://readthedocs.org/projects/matlab-usage-stats/badge/?version=latest)](http://matlab-usage-stats.readthedocs.io/en/latest/?badge=latest)

Introduction
============

Matlab Usage Stats is a django based project to aggregate statistics FlexLM based MATLAB License Server logs.

MATLAB License Server does not provide and option to track users IP addresses. So, there is no way in which one can analyse usage in terms of users departments or category.

This project provides a way to analyse the originally produced MATLAB debug logs along with port activity log and login portal log.

This Django project has two apps, parser and reports.

The parser app takes care of processing the logs and creating database entries which will then be processed by the reports app to generate different graphs based on the toolboxes that matlab provides and the departments.

There are four types of reports:

- `<site_root>/reports/list/` - List view of all entries
- `<site_root>/reports/graphs/` - Stacked Bar view of all entries
- `<site_root>/reports/departments/` - Bar Graph view of all entries from selected departments
- `<site_root>/reports/time/` - Stacked Bar Graph view of all entries from selected time frame

How to Use
==========

- Download or Clone the source code from [here](https://github.com/akshaykhadse/matlab-usage-stats/)
- `$ python3 setup.py install`
- Copy the data files to `data/` folder. Data files should be as follows:

  - `LM_TMW.log` - MATLAB Debug Log file
  - `src_ip_log` - Port activity log file with timestamp and IP coloumns
  - `matlab_DB_active.csv` - CSV file genrated from database `active` table
  - `matlab_DB_archive.csv` - CSV file generated from database `archive` table

- Create database by `$ python3 manage.py migrate`
- To update entries use

  - `$ python3 manage.py shell`
  - `>>> run parser/main`

- To start web interface `$ python3 manage.py runserver`

Documentation
=============
Docs for this project can be found [here](https://matlab-usage-stats.readthedocs.io/)

Requirements
============

- flake8>=3.2.0
- ldap3>=1.4.0
- django>=1.10
- coverage>=4.2
- coveralls>=1.1
- plotly>=1.12.9
- sphinx>=1.4.8
