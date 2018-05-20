How to Use
==========

- Download or Clone the source code from `here <https://github.com/akshaykhadse/matlab-usage-stats/>`_
- Setup the project using ``$ python3 setup.py install``
- Copy the data files to ``data/`` folder. Data files should be as follows:

  - ``LM_TMW.log`` - MATLAB Debug Log file
  - ``src_ip_log`` - Port activity log file with timestamp and IP coloumns
  - ``matlab_DB_active.csv`` - CSV file genrated from database `active` table
  - ``matlab_DB_archive.csv`` - CSV file generated from database `archive` table

  Sample data files can be downloaded `here <https://drive.google.com/drive/folders/0B8bbv1FqBgBVZ1NBdWE4VGd2Zlk?usp=sharing>`_

- Create database by ``$ make migrate``
- To update entries use ``$ make update``

  (This command needs to be run whenever log files are changed)

- To start web interface ``$ make run``

Requirements
============

- flake8>=3.2.0
- ldap3>=1.4.0
- django>=1.10
- coverage>=4.2
- coveralls>=1.1
- plotly>=1.12.9
- sphinx>=1.4.8
