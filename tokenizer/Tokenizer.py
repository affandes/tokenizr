import re

import KataUlang as ku
import SingkatanAkronim as sa


# Todo: tandai dulu untuk dihapus
def tokenisasi_kata_spasi(doc):
    kata = [unit for unit in doc.split()]
    return kata


# Todo: tandai dulu untuk dihapus
def tokenisasi_kata_pungtuasi(doc):
    kata_kata = tokenisasi_kata_spasi(doc)
    tokens = []
    for kata in kata_kata:
        terms = __split_kata_pungtuasi(kata)
        tokens += terms

    return tokens


# Todo: tandai dulu untuk dihapus
def __split_kata_pungtuasi(kata):
        terms = []

        print kata + " : "

        # Apakah hanya 1 karakter?
        if len(kata) == 1:
            terms.append(kata)
            print " 1 char "
            return terms

        # Apakah teks biasa
        if re.match(r"^[a-zA-Z]+$",kata):
            terms.append(kata)
            print " Pass "
            return terms

        # Apakah elipsis?
        if kata == "...":
            terms.append(kata)
            print " Pass "
            return terms

        # Pisahkan tanda titik, tanda koma, tanda tanya, tanda seru, tanda titik koma,
        # tanda titik dua pada setiap akhir kalimat.
        if re.match(r"^.+[.,?!;:]$",kata):

            if sa.is_singkatan_akronim(kata):
                terms.append(kata)
            else:
                terms += __split_kata_pungtuasi(kata[:-1])
                terms.append(kata[-1])

            #print terms
        elif re.match(r"^[\"\'(\[].+[\"\')\]]$",kata):
            terms.append(kata[0])
            terms += __split_kata_pungtuasi(kata[1:-1])
            terms.append(kata[-1])

            #print terms
        elif re.match(r"^[\"\'(\[/].+$",kata):
            terms.append(kata[0])
            terms += __split_kata_pungtuasi(kata[1:])

            #print terms
        elif re.match(r"^.+[\"\')\]/]$",kata):
            terms += __split_kata_pungtuasi(kata[:-1])
            terms.append(kata[-1])

            #print terms

        elif re.match(r"^[\w][\w.,-/]*/[\w.,-/]*[\w]$",kata):
            ts = kata.split("/")
            if len(ts) > 2:
                cek = False
                for t in ts:
                    print "Coba cek kata berikut: " + t
                    if re.match(r"[0-9-]+", t):
                        print "ok"
                        cek = True

                if cek:
                    terms.append(kata)
                else:
                    for i,t in enumerate(ts):
                        terms += __split_kata_pungtuasi(t)
                        if i < len(ts)-1:
                            terms.append("/")
            else:
                terms += __split_kata_pungtuasi(ts[0])
                terms.append("/")
                terms += __split_kata_pungtuasi(ts[1])
        elif re.match(r"^\w+-\w+$",kata):
            ts = kata.split("-")
            if len(ts) == 2 and ts[0] == ts[1]:
                # cek apakah pengulangan tsb memang ada di kamus atau tidak
                if kata in ku.__kamus_kata_ulang:
                    terms.append(kata)
                else:
                    terms.append(ts[0])
                    terms.append("-")
                    terms.append(ts[1])
            else:
                terms.append(kata)
        else:
            terms.append(kata)

            #print " Pass Other "

        return terms


# Tokenize per 1 line
def tokenize_line(line):
    tokens_in_line = []
    for term in line.split():
        tokens = tokenize_term(term)
        tokens_in_line += tokens

    return tokens_in_line


# Tokenize per 1 term
def tokenize_term(term):
    # Prepare
    tokens = []

    # Simple token
    if re.match(__simple_token, term):
        tokens.append(term)
        return tokens

    # Ellipsis
    if re.match(__complex_elipsis, term):
        if term == "...":
            tokens.append(term)
            return tokens
        else:
            tokens.append(term[:-1])
            tokens.append(term[-1:])
            return tokens

    # Prefixed
    if re.match(__prefixed_token, term):
        # todo: pikirkan ttg apostrof
        tokens.append(term[:1])
        tokens += tokenize_term(term[1:])
        return tokens

    # Suffixed
    if re.match(__suffixed_token, term):
        if term[-1:] == "-":
            tokens.append(term)
        elif sa.is_singkatan_akronim(term):
            tokens.append(term)
        else:
            tokens += tokenize_term(term[:-1])
            tokens.append(term[-1:])

        return tokens

    # Infixed
    if re.match(__infixed_token, term):

        # Tanda pisah, unicode \xe2 diubah menjadi -
        if re.match(__tanda_pisah, term, re.UNICODE):
            #print term
            terms = re.split(r"\xe2", term, 2)
            if len(terms) == 2:
                tokens += tokenize_term(terms[0])
                tokens.append("-")
                tokens += tokenize_term(terms[1][2:])
                return tokens
            else:
                tokens.append(term)
                return tokens

        # Tanda garis miring
        if re.match(__tanda_garis_miring, term):
            if __is_nomor_surat(term):
                tokens.append(term)
                return tokens
            else:
                terms = term.split("/")
                for i, t in enumerate(terms):
                    tokens.append(t)
                    if i < len(terms)-1:
                        tokens.append("/")
                return tokens

        # Tanda hubung
        if re.match(__tanda_hubung, term):
            if __is_pisah_by_tanda_hubung(term):
                terms = term.split("-")
                for i, t in enumerate(terms):
                    tokens.append(t)
                    if i < len(terms) - 1:
                        tokens.append("-")

                return tokens
            else:
                tokens.append(term)
                return tokens

    #    Else infix
    #    print "Else infix: " + term

    if term == "":
        return []

    # Else
    print term
    tokens.append(term)
    return tokens


def __is_pisah_by_tanda_hubung(text):
    terms = text.split("-")
    # Cek jika hanya 1 tanda hubung
    if len(terms) == 2:
        # Kata ulang semu harus digabung
        if text.lower() in ku.__kamus_kata_ulang_semu:
            return False

        # Se-Kapital
        if re.match(__rangkaian_se, text):
            return False

        # Kata-Kapital
        if re.match(__rangkaian_kata_kap, text):
            return False

        # Ke-12
        if re.match(__rangkaian_ke, text):
            return False

        # Akhiran 1950-an
        if re.match(__rangkaian_an, text):
            return False

        # Kata ganti -mu -ku -nya
        if re.match(__rangkaian_kap_mu, text):
            return False

        # Kata ganti Tuhan -Nya -Mu
        if re.match(__rangkaian_kata_ganti_tuhan, text):
            return False

        # Rangkaian xxx-KAP-yyy
        if re.match(__rangkaian_kap, text):
            return False

        # Rangkaian KAP-12
        if re.match(__rangkaian_kap_angka, text):
            return False

    else: # Cek jika tanda hubung lebih dari 2
        # Tanggal
        if re.match(__penanggalan_angka, text):
            return False

        # Ejaan
        if re.match(__ejaan_satu_satu, text):
            return False

        # Angka serial
        if re.match(__angka_serial, text):
            return False

    return True


def __is_nomor_surat(text):
    terms = text.split("/")
    if len(terms) > 2:
        for term in terms:
            if re.match(__bagian_nomor_surat, term):
                return True
        return False
    else:
        return False


# Cek yang hanya mengandung huruf saja
__simple_token = r"^[A-Za-z]+$"

# Cek bentuk2 ellipsis, misalnya ... .... ..., ...? ...!
__complex_elipsis = r"^[.]{3}[.,?!:;]?"

# Cek bentuk2 tanda baca di awal term
__prefixed_token = r"^[.:\-\xe2\"\'\(\[\/]+"

# Cek bentuk2 tanda baca di akhir term
__suffixed_token = r".+[.,;:\-\xe2\?\!\"\'\)\]\/]+$"

# Cek bentuk2 tanda baca di tengah term
__infixed_token = r"^.+[.,;:\-\xe2\?\!\"\'\(\[\)\]\/]+.+$"

# Cek tanda pisah saja
__tanda_pisah = r"^.+\xe2.+$"

# Cek hubung
__tanda_hubung = r"^[\w\d.,]+(\-[\w\d.,]+)+$"

# Cek nomor surat
__tanda_garis_miring = r"^[\w\d.,-]+(\/[\w\d.,-]+)+$"

# Cek bagian nomor surat
__bagian_nomor_surat = r"[0-9]+[A-Za-z0-9.-]*[A-Za-z0-9]*"

# Cek tanggal dd-mm-yy dd-mm-yyyy atau kombinasinya
__penanggalan_angka = r"^(\d{1,2}\-\d{1,2}\-\d{2,4}|\d{2,4}\-\d{1,2}\-\d{1,2})$"

# Cek e-j-a-a-n
__ejaan_satu_satu = r"^[A-Za-z](\-[A-Za-z])+$"

# Cek se-Kapital
__rangkaian_se = r"^(Se|SE|se)-[A-Z]{1}[a-z]+$"

# Cek kata-Kapital
__rangkaian_kata_kap = r"^\w+-[A-Z]{1}[a-z]+$"

# Cek ke-12
__rangkaian_ke = r"^(KE|Ke|ke)-\d+$"

# Cek akhiran 1950-an
__rangkaian_an = r"^\d+\-an$"

# Cek KAP-mu
__rangkaian_kap_mu = r"^[A-Z]+\-(ku|mu|nya){1}$"

# Cek kata ganti Tuhan -Nya, -Mu
__rangkaian_kata_ganti_tuhan = r"^\w+\-(Nya|Mu){1}$"

# Cek rangkaian xx-KAP-xx
__rangkaian_kap = r"^(\w{2,}\-)?[A-Z]+(\-\w{1,3})?$"

# Cek KAP-2
__rangkaian_kap_angka = r"^[A-Z]+\-\d+$"

# Cek angka serial
__angka_serial = r"^\d+(\-\d+)*$"
