import re


__singkatan = [
    'Prof.',
    'Dr.',
    'dr.',
    'KH.',
    'H.',
    'Hj.',
    'Tn.',
    'Ny.',
    'Bpk.',
    'Sdr.',
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
    'Ttd.',
    'ttd.',
    'dkk.',
    'd.a.',
    'c.q.',
    'u.b.',
    'u.p.',
    's.d.',
    'a.n.'
]

__akronim = [
    'Bappenas',
    'Pemilu'
]


def is_singkatan_akronim(term):
    return term in __singkatan \
           or term in __akronim \
           or __is_pola_singkatan_nama(term)


def __is_pola_singkatan_nama(term):
    if re.match(r"^[A-Z][a-z]*\.([A-Z][a-z]*\.)+$", term):
        # print term + " adalah pola singkatan"
        return True
    else:
        return False
