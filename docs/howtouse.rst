How to Use
==========

- Download or Clone the source code from `here<https://github.com/akshaykhadse/matlab-usage-stats/>`_
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
