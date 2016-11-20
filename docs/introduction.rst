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
