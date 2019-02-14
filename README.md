# simple-python-rover

Simple Python application that will parse dates from input text file and download Mars Rover images based on the specified date/s

# Pre-requisites
The following need to be installed:
- [Python 3.6+](https://www.python.org/downloads/)
- [Requests](http://docs.python-requests.org/en/master/user/install/#install)

# How To Use
1. Open terminal / cmd, and type ```py rover.py -i <INPUT_FILE>``` to execute

# Notes
- Only the following date formats are supported:
  - MM/DD/YY (e.g. 02/25/17)
  - Month DD, YYYY (e.g. June 2, 2018)
  - Mon-DD-YYYY (e.g. Jul-13-2016)
- The application will create a new directory (```output```) every execution
