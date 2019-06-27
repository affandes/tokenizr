import os
import csv
import time
import tokenizer.Tokenizer as tzr

# Set file name
file_name = "text/identic.raw.npp.txt"

# Check file exist
if not os.path.isfile(file_name):
    print "File '" + file_name + "' tidak ditemukan."
    exit()

# Read file and convert to list of docs
with open(file_name) as file_csv:
    docs = [ row[1] for row in csv.reader(file_csv, delimiter="\t") ]

# Tokenize each doc
start_time = time.time()
words = [ tzr.tokenize(doc) for doc in docs ]
end_time = time.time()

# Result
print words
print end_time-start_time