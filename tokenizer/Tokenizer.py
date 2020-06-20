import re
import SingkatanAkronim as sa
import KataUlang as ku


def tokenisasi_kata_spasi(doc):
    kata = [unit for unit in doc.split()]
    return kata

def tokenisasi_kata_pungtuasi(doc):
    kata_kata = tokenisasi_kata_spasi(doc)
    tokens = []
    for kata in kata_kata:
        terms = __split_kata_pungtuasi(kata)
        tokens += terms

    return tokens

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
