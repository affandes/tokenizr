# coding=utf-8
import os

import tokenizer.Tokenizer as tzr

# Tentukan nama file input/output
corpus_file_name = "text/puebi.txt"
output_file_name = "out/eksp2.txt"

# Periksa ketersediaan file input
if not os.path.isfile(corpus_file_name):
    print("File '" + corpus_file_name + "' tidak ditemukan.")
    exit()

# Baca file input dan konversi ke array [{'k':'Kategori','t':'Teks'}]
with open(corpus_file_name) as file_csv:
    docs = []
    for line in file_csv.readlines():
        row = line.split("\t")
        docs.append({'k': row[0], 't': row[1].strip()})

# Tokenisasi menggunakan spasi dan pungtuasi
results = [tzr.tokenize_line(doc['t']) for doc in docs]

# Simpan results ke file
with open(output_file_name, "wb") as out_csv:
    for result in results:
        for idx,kata in enumerate(result):
            out_csv.write(kata)
            if idx < len(result)-1:
                out_csv.write("\t")
        out_csv.write("\n")

