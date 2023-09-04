#!/usr/bin/env python3

import os
import sys
import argparse
from datetime import datetime


#***************************************
#** Utils
#***************************************
  
def searchAccessLog(filePath, query):
  results = []
  with open(filePath, 'r') as currentFile:
      for line in currentFile:
        if query in line:
            results.append(line)
            
  return results

def getServerIp(fileName):
  fileParts = fileName.split('/')
  for part in fileParts:
    if 'ip-' in part:
      return part

def writeToFile(filePath, query, searchType, searchResults):
  currentPath = filePath + '/' + searchType + '-' + datetime.now().strftime('%d-%m-%y--%H-%M-%S') + '.txt'
  with open(currentPath, 'w', encoding='utf-8') as currentFile:
    currentFile.write('Search query: ' + query + '\n-------------------------------\n\n\n')
    currentFile.writelines(searchResults)

def searchSingleLineLog(filePaths, typeOfLog, query):
  results = []
  for file in filePaths:
      if typeOfLog in file:
        fName = '\n\n------------------------------------------\nFrom server ' + getServerIp(file) + ':\n------------------------------------------\n'
        results.append(fName)
        with open(file, 'r') as currentFile:
          fileData = []
          
          for lineNumber, line in enumerate(currentFile):
            if query.lower() in line.lower():
                fileData.append(str(lineNumber + 1) + ': ' + line)
          if len(fileData) > 0:
            for line in fileData:
              results.append(line)
          else:
            results.append('No Results were found on this server')
  
  
  printResults(results)
    
def searchMultipleLineLog(filePaths, typeOfLog, query, hasHeaders = False):
  results = []
  for file in filePaths:
      if typeOfLog in file:
        fName = '\n\n------------------------------------------\nFrom server ' + getServerIp(file) + ':\n------------------------------------------'
        results.append(fName)
        with open(file, 'r') as currentFile:
          capturingStack = False
          fileData = []
          for lineNumber, line in enumerate(currentFile):
            if query.lower() in line.lower():
                capturingStack = True
                fileData.append(str(lineNumber + 1) + ': ' + line)
            else:
              if capturingStack:
                if(hasHeaders):
                  if line.split(' | ')[3].startswith('\t') or line.split(' | ')[3].startswith('Caused by'):
                    fileData.append(line)
                  else:
                    capturingStack = False
                else:
                  if line.startswith('\t') or line.startswith('Caused by'):
                    fileData.append(line)
                  else:
                    capturingStack = False
          if len(fileData) > 0:
            for line in fileData:
              results.append(line)
          else:
            results.append('No Results were found on this server')
            
  printResults(results)



def printResults(results):
  if not args.output is None:
    writeToFile(args.output, args.search, args.type, results)
  else:
    for item in results:
      print(item)


#***************************************
#** Script variables
#***************************************

validTypes = ['access', 'services', 'email', 'sql', 'standard']

#***************************************
#** Argument validation
#***************************************

inboundArgs = argparse.ArgumentParser()

inboundArgs.add_argument('-i', '--input', help="Path of the folder where the logs are stored")
inboundArgs.add_argument('-o', '--output', help="Path of the folder where the results will be stored")
inboundArgs.add_argument('-t', '--type', help="Type of search. accepted values are: access, services, email, standard")
inboundArgs.add_argument('-s', '--search', help="String that will be searched throughout the logs")

args = inboundArgs.parse_args()

if args.input is None:
  print('The input argument is missing')
  sys.exit(10)
  
if not os.path.exists(args.input):
  print('The input path doesn\'t exist, please validate the inputs')
  sys.exit(15)

if not args.output is None:
  if not os.path.exists(args.output):
    print('The output path doesn\'t exist, please validate the inputs')
    sys.exit(15)

if args.type is None:
  print('The type argument is missing')
  sys.exit(10)
  
if not args.type in validTypes:
  print('The type of log is not valid, valid values are: access, services, email, standard')
  sys.exit(15)

if args.search is None:
  print('The search argument is missing')
  sys.exit(10)

#***************************************
#** Folder tree creation
#***************************************

fileNames = []

for root, dirs, files in os.walk(args.input):
  for name in files:
    fileNames.append(os.path.join(root, name))

#***************************************
#** Access logs search logic
#***************************************

if(args.type == 'access'):
  searchSingleLineLog(fileNames, 'bb-access', args.search)


#***************************************
#** Email logs search logic
#***************************************

if(args.type == 'email'):
  searchSingleLineLog(fileNames, 'bb-email', args.search)

#***************************************
#** Services logs search logic
#***************************************

if(args.type == 'services'):
  searchMultipleLineLog(fileNames, 'bb-services', args.search)

#***************************************
#** SQL logs search logic
#***************************************

if(args.type == 'sql'):
  searchMultipleLineLog(fileNames, 'bb-sqlerror', args.search)

#***************************************
#** Stdout-stderr logs search logic
#***************************************

if(args.type == 'standard'):
  searchMultipleLineLog(fileNames, 'stdout-stderr', args.search, True)