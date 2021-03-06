# Matlab Usage Statistics
[![Build Status](https://travis-ci.org/akshaykhadse/matlab-usage-stats.svg?branch=master)](https://travis-ci.org/akshaykhadse/matlab-usage-stats)
[![Coverage Status](https://coveralls.io/repos/github/akshaykhadse/matlab-usage-stats/badge.svg?branch=master)](https://coveralls.io/github/akshaykhadse/matlab-usage-stats?branch=master)

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
- Setup the project using **`$ python3 setup.py install`**
- Copy the data files to **`data/`** folder. Data files should be as follows:

  - **`LM_TMW`** - MATLAB Debug Log file
  - **`src_ip_log`** - Port activity log file with timestamp and IP coloumns
  - **`matlab_DB_active.csv`** - CSV file genrated from database `active` table
  - **`matlab_DB_archive.csv`** - CSV file generated from database `archive` table

- Create database by **`$ make migrate`**
- To update entries use **`$ make update`**

  (This command needs to be run whenever log files are changed)

- To start web interface **`$ make run`**

Generating simulated data
=========================
- Clear any contentes of **`simulator/output`** directory
- Ensure that there is log file generated by **`lmstat`** command in **`simulator/input`** directory with name **`lmstat.txt`** *(To ensure that simultor scripts has all package names available)*
- Run **`python3 simulator/simulator.py`** from the project root directory
- Let it run for required amount of time and press **`Ctrl+C`** to stop
- Copy the files from **`simulator/output`** directory to **`data/`** directory

Documentation
=============
- Docs for this project can be found **`docs`** directory

Requirements
============

- flake8>=3.2.0
- ldap3>=1.4.0
- django>=1.10
- coverage>=4.2
- coveralls>=1.1
- plotly>=1.12.9
- sphinx>=1.4.8
