import re


__singkatan = [
    'Prof.',
    'dr.',
    'Almh.',
    'almh.',
    'alm.',
    'hlm.',
    'dsb.',
    'dst.',
    'dll.',
    'sda.',
    'Sda.',
    'ybs.',
    'Ybs.',
    'yth.',
    'Yth.',
    'ttd.',
    'dkk.',
    'd.a.',
    'c.q.',
    'u.b.',
    'a.n.'
]

__akronim = [
    'Bappenas'
]


def is_singkatan_akronim(term):
    return term in __singkatan \
           or term in __akronim \
           or __is_pola_singkatan_nama(term)

def __is_pola_singkatan_nama(term):
    if re.match(r"([A-Z]{1,2}[a-z]{0,2}[.])+",term):
        #print term + " adalah pola singkatan"
        return True
    else:
        return False
