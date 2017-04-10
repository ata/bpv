import locale
import math
from terminaltables import AsciiTable

class Cicilan:
    def __init__(self, bulan, jumlah_pembayaran, jumlah_pokok, jumlah_bunga,
                 sisa_pokok, total_pembayaran, total_pokok, total_bunga,
                 pembayaran_extra=0, target_pembayaran=0, tabungan=0):
        self.bulan = bulan
        self.jumlah_pembayaran = jumlah_pembayaran
        self.jumlah_pokok = jumlah_pokok
        self.jumlah_bunga = jumlah_bunga
        self.sisa_pokok = sisa_pokok
        self.total_pembayaran = total_pembayaran
        self.total_pokok = total_pokok
        self.total_bunga = total_bunga
        self.pembayaran_extra = pembayaran_extra
        self.target_pembayaran = target_pembayaran
        self.tabungan = tabungan


class Loan:
    def __init__(self, pinjaman, bunga, tenor, target_bulanan, accel=0):
        self.pinjaman = pinjaman
        self.bunga = bunga / 100
        self.tenor = tenor
        self.target_bulanan = target_bulanan
        self.accel = accel
        self.sisa_pokok = self.pinjaman
        self.total_pembayaran = 0
        self.total_pokok = 0
        self.total_bunga = 0
        self.cicilans = []
        self.cicilan_anuitas = self.get_cicilan_anuitas()
        self.tabungan = 0

    def get_cicilan_anuitas(self):
        return self.pinjaman * (self.bunga/12) * 1 / (1 - 1/ (1 + (self.bunga/12))**self.tenor )

    def populate_cicilan(self):
        for bulan in range(1, self.tenor + 1):
            jumlah_bunga = self.sisa_pokok * self.bunga / 12
            jumlah_pembayaran = self.get_pembayaran(bulan)
            jumlah_pokok = jumlah_pembayaran - jumlah_bunga

            if (jumlah_pembayaran + self.tabungan) >= self.sisa_pokok:
                jumlah_pembayaran = jumlah_pokok = self.sisa_pokok
                jumlah_bunga = 0

            self.sisa_pokok = self.sisa_pokok - jumlah_pokok

            self.total_pembayaran += jumlah_pembayaran
            self.total_pokok += jumlah_pokok
            self.total_bunga += jumlah_bunga

            cicilan = Cicilan(bulan=bulan,
                              jumlah_pembayaran=jumlah_pembayaran,
                              jumlah_pokok=jumlah_pokok,
                              jumlah_bunga=jumlah_bunga,
                              sisa_pokok =self.sisa_pokok,
                              total_pembayaran=self.total_pembayaran,
                              total_pokok=self.total_pokok,
                              total_bunga=self.total_bunga,
                              pembayaran_extra=self.get_cicilan_extra(bulan),
                              target_pembayaran=self.get_target_bulanan(bulan),
                              tabungan=self.tabungan)
            self.cicilans.append(cicilan)

            if self.sisa_pokok <= 0:
                break


    def get_pembayaran(self, bulan):
        pembayaran = self.cicilan_anuitas
        self.tabungan += self.get_cicilan_extra(bulan)

        if bulan % 6 == 0 and self.tabungan < 0.25 * self.sisa_pokok and self.tabungan > 3 * self.cicilan_anuitas:
            pembayaran = pembayaran + self.tabungan
            self.tabungan = 0

        return pembayaran

    def get_cicilan_extra(self, bulan):
        return self.get_target_bulanan(bulan) - self.cicilan_anuitas

    def get_target_bulanan(self, bulan):
        current_salary = self.target_bulanan * 2.5
        next_salary = current_salary * (1 + self.accel) ** math.floor(bulan/12)

        return next_salary * 0.4


class Renderer:
    def __init__(self, loan):
        self.loan = loan
        locale.setlocale(locale.LC_ALL, '')
        loan.populate_cicilan()

    def render(self):
        _ = self.currency
        table_data = [
            ['Bulan', 'Angsuran', 'Pokok', 'Bunga', 'Sisa Pokok','Target', 'Extra', 'Tabungan'],
        ]
        for c in self.loan.cicilans:
            table_data.append([c.bulan, _(c.jumlah_pembayaran), _(c.jumlah_pokok), _(c.jumlah_bunga), _(c.sisa_pokok), _(c.target_pembayaran), _(c.pembayaran_extra), _(c.tabungan)])

        table = AsciiTable(table_data)
        for j in range(0, 9):
            table.justify_columns[j] = 'right'
        print(table.table)

        table_data = [
            ['Pinjaman', _(loan.pinjaman)],
            ['Tenor', '%s bulan' % loan.tenor],
            ['Bunga', '%s percent' % (loan.bunga * 100)],
            ['Total Pembayaran', _(loan.total_pembayaran)],
            ['Total Pokok', _(loan.total_pokok)],
            ['Total Bunga', _(loan.total_bunga)],
            ['Accerasi', '%s percent' % (loan.accel * 100)],
        ]
        table = AsciiTable(table_data)
        table.justify_columns[1] = 'right'
        print(table.table)

    def currency(self, number):
        return locale.currency(number, grouping=True)


loan = Loan(540000000.0, 9.25, 180, 8000000.0, 0.15)
renderer = Renderer(loan)
print(renderer.render())

