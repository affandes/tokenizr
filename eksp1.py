# coding=utf-8
import tokenizer.Tokenizer as tzr
import os
import csv

# Tentukan nama file input/output
corpus_file_name = "text/puebi.txt"
output_file_name = "out/eksp1.txt"

# Periksa ketersediaan file input
if not os.path.isfile(corpus_file_name):
    print "File '" + corpus_file_name + "' tidak ditemukan."
    exit()

# Baca file input dan konversi ke array [{'k':'Kategori','t':'Teks'}]
with open(corpus_file_name) as file_csv:
    docs = [{'k': row[0], 't': row[1]} for row in csv.reader(file_csv, delimiter="\t")]

# Tokenisasi menggunakan spasi saja
results = [tzr.tokenisasi_kata_spasi(doc['t']) for doc in docs]

# Simpan results ke file
with open(output_file_name, "wb") as out_csv:
    writer = csv.writer(out_csv, delimiter="\t")
    for result in results:
        writer.writerow(result)
