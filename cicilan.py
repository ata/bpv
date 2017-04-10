import locale
import numpy as np
import math
import csv
locale.setlocale(locale.LC_ALL, '')

pinjaman = np.float128(540000000.0)
i = np.float128(9.25 / 100)
i_f = np.float128(9.25 / 100)
m = 180
m_f = 0
_1 = np.float128(1.0)
_12 = np.float128(12.0)

anuitas = lambda i: pinjaman * (i/_12) * _1 / (_1 - _1/ (_1 + (i/_12))**m )
angsuran = anuitas(i)

bulan_dipercepat = 0
percepatan = 3

_ = lambda x: locale.currency(x, grouping=True)

sisa_pokok = pinjaman
total_pembayaran = 0
total_bunga = 0
total_pokok = 0

tabungan = 0.0

with open('cicilan.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Jumlah Pinjaman', pinjaman])
    writer.writerow(['Lama pinjaman', m])
    writer.writerow(['Bunga Anuitas', i * 100])
    writer.writerow([])
    writer.writerow(['bulan ke','cicilan', 'pokok', 'bunga', 'sisa_pokok', '', 'total_pembayaran', 'total_pokok', 'total_bunga'])
    for a in range(1, m + 1):
        if a > m_f:
            i = i_f
        angsuran = anuitas(i)
        bunga = sisa_pokok * i / _12
        pokok = angsuran - bunga
        cicilan = angsuran

        pelunasan = angsuran * percepatan
        pengali = percepatan

        while pelunasan > 0.25 * sisa_pokok and pengali >= 3:
            pengali = pengali - 1
            pelunasan = angsuran * pengali

        if a % 6 == 0 and pelunasan < 0.25 * sisa_pokok and a > m_f and a >= bulan_dipercepat:
            cicilan = cicilan + pelunasan
            pokok = pokok + pelunasan
        elif (angsuran + pelunasan) >= sisa_pokok and a >= bulan_dipercepat:
            cicilan = pokok = sisa_pokok

        sisa_pokok = sisa_pokok - pokok

        total_pembayaran = total_pembayaran + cicilan
        total_bunga = total_bunga + bunga
        total_pokok = total_pokok + pokok

        print('Angsuran ke-%03d : %s ,Pokok: %s, Bunga: %s, sisa_pokok: %s, total_pembayaran: %s, total_bunga: %s, total_pokok: %s' % (
            a, _(cicilan), _(pokok), _(bunga), _(sisa_pokok), _(total_pembayaran), _(total_bunga), _(total_pokok)
        ))

        writer.writerow([a, cicilan, pokok, bunga, sisa_pokok, '', total_pembayaran, total_bunga, total_pokok])

        if sisa_pokok <= 0:
            break

    print('Total Pembayaran:', _(total_pembayaran))
    print('Total Pokok:', _(total_pokok))
    print('Total Bunga:', _(total_bunga))
    writer.writerow(['Total', total_pembayaran, total_pokok, total_bunga, ''])
