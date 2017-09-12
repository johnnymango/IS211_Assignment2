#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imported Modules
import argparse
import urllib2
import csv
import datetime
import logging


# Sets up the argparse to accept the url argument when the py file is executed.
parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str, required=True)
args = parser.parse_args()
url = args.url


# Sets up the Logger to catch errors and create error.log file
LOG_FILENAME  = 'error.log'
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.ERROR,)
logger = logging.getLogger('assignment2')


# Function downloads the data from the argparse URL argument.
def downloadData(urlname):
   response = urllib2.urlopen(urlname)
   mydata = csv.reader(response)
#Skip the header row
   next(mydata)
   return mydata


# Function processes data by checking the datetime format of the bday,
# logging errors against this error and creating up the dict.
def processData(mydata):
    mydict = {}
    line_number = 1
    for row in mydata:
        try:
            row[2] = datetime.datetime.strptime(row[2], '%d/%m/%Y')
            row[2] = row[2].date()
            mydict[(int(row[0]))] = (row[1], row[2])
        except ValueError:
            logger.error('Error processing line # {} for ID #{}'.format(line_number, row[0]))
        finally:
            line_number += 1
    return mydict


# Function displays the Person ID, Name and BDay to the screen.
def displayPerson(personID, personData):
    try:
        print 'Person # {} is {} with a birthday of {}'.format(
        personID, personData[personID][0], personData[personID][1])
    except:
        print 'No user found with that ID.'


# Function initiates the program when the file executes and takes
# the raw input for the ID lookup in the dict (in processData)
def main():
    csvData = downloadData(url)
    personData = processData(csvData)
    personID = 1
    while personID >= 1:
        personID = int(raw_input('Please enter an ID: '))
        if personID >= 1:
            displayPerson(personID, personData)
    else:
        print 'Invalid ID. Exiting...'
        exit


# Calls the main() function.
if __name__ == "__main__":
    main()