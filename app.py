import tkinter as tk
from tkinter import simpledialog, ttk, messagebox
import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

class Barang:
    def __init__(self, nama, harga_beli, harga_jual, stok, vendor):
        self.nama = nama
        self.harga_beli = harga_beli
        self.harga_jual = harga_jual
        self.stok = stok
        self.vendor = vendor

    def tambah_stok(self, jumlah):
        self.stok += jumlah

    def kurangi_stok(self, jumlah):
        if self.stok >= jumlah:
            self.stok -= jumlah
            return True
        else:
            print("Stok tidak mencukupi.")
            return False

    def update_info(self, nama, harga_beli, harga_jual, stok, vendor):
        self.nama = nama
        self.harga_beli = harga_beli
        self.harga_jual = harga_jual
        self.stok = stok
        self.vendor = vendor

    def to_list(self):
        return [self.nama, str(self.harga_beli), str(self.harga_jual), str(self.stok), self.vendor]

class AplikasiInventaris(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Inventaris Barang")
        self.barang = []
        self.load_data()

        self.label_info = tk.Label(self, text="Informasi Barang", font=("Helvetica", 16, "bold"))
        self.label_info.grid(row=0, column=0, columnspan=2, pady=10)

        self.treeview_barang = ttk.Treeview(self, columns=("Nama", "Harga Beli", "Harga Jual", "Stok", "Vendor", "Total Harga"), show="headings")
        self.treeview_barang.heading("Nama", text="Nama Barang")
        self.treeview_barang.heading("Harga Beli", text="Harga Beli")
        self.treeview_barang.heading("Harga Jual", text="Harga Jual")
        self.treeview_barang.heading("Stok", text="Stok")
        self.treeview_barang.heading("Vendor", text="Vendor")
        self.treeview_barang.heading("Total Harga", text="Total Harga")
        self.treeview_barang.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.update_treeview()

        button_frame = tk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)

        self.btn_tambah = tk.Button(button_frame, text="Tambah Barang", command=self.tambah_barang)
        self.btn_tambah.pack(side=tk.LEFT, padx=5)

        self.btn_edit = tk.Button(button_frame, text="Edit Barang", command=self.edit_barang)
        self.btn_edit.pack(side=tk.LEFT, padx=5)

        self.btn_hapus = tk.Button(button_frame, text="Hapus Barang", command=self.hapus_barang)
        self.btn_hapus.pack(side=tk.LEFT, padx=5)

        self.btn_beli = tk.Button(self, text="Beli Barang", command=self.beli_barang)
        self.btn_beli.grid(row=3, column=0, pady=5, padx=5, sticky="ew")

        self.btn_jual = tk.Button(self, text="Jual Barang", command=self.jual_barang)
        self.btn_jual.grid(row=3, column=1, pady=5, padx=5, sticky="ew")

        self.btn_trans = tk.Button(self, text="Tampilkan Transaksi", command=self.tampilkan_transaksi)
        self.btn_trans.grid(row=4, column=0, columnspan=2, pady=5, padx=5, sticky="ew")

        self.label_cari = tk.Label(self, text="Cari Nama Barang:")
        self.label_cari.grid(row=5, column=0, pady=5, padx=5, sticky="e")
        self.entry_cari = tk.Entry(self)
        self.entry_cari.grid(row=5, column=1, pady=5, padx=5, sticky="ew")
        self.btn_cari = tk.Button(self, text="Cari", command=self.cari_barang)
        self.btn_cari.grid(row=5, column=2, pady=5, padx=5, sticky="w")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def load_data(self):
        try:
            with open("data_barang.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    self.barang.append(Barang(data[0], float(data[1]), float(data[2]), int(data[3]), data[4]))
        except FileNotFoundError:
            pass

    def save_data(self):
        with open("data_barang.txt", "w") as file:
            for barang in self.barang:
                file.write(",".join(barang.to_list()) + "\n")

    def update_treeview(self, results=None):
        self.treeview_barang.delete(*self.treeview_barang.get_children())
        if results is None:
            results = self.barang
        for barang in results:
            total_harga = barang.harga_beli * barang.stok
            self.treeview_barang.insert("", tk.END, values=[barang.nama, barang.harga_beli, barang.harga_jual, barang.stok, barang.vendor, total_harga])

    def tambah_barang(self):
        nama = simpledialog.askstring("Tambah Barang", "Masukkan nama barang:")
        harga_beli = float(simpledialog.askstring("Tambah Barang", "Masukkan harga beli barang:"))
        harga_jual = float(simpledialog.askstring("Tambah Barang", "Masukkan harga jual barang:"))
        stok = int(simpledialog.askstring("Tambah Barang", "Masukkan stok barang:"))
        vendor = simpledialog.askstring("Tambah Barang", "Masukkan vendor barang:")
        self.barang.append(Barang(nama, harga_beli, harga_jual, stok, vendor))
        self.save_data()
        self.update_treeview()

    def edit_barang(self):
        selected_item = self.treeview_barang.selection()
        if selected_item:
            item = self.treeview_barang.item(selected_item)
            index = self.treeview_barang.index(selected_item)
            barang = self.barang[index]
            nama = simpledialog.askstring("Edit Barang", "Masukkan nama barang:", initialvalue=barang.nama)
            harga_beli = float(simpledialog.askstring("Edit Barang", "Masukkan harga beli barang:", initialvalue=barang.harga_beli))
            harga_jual = float(simpledialog.askstring("Edit Barang", "Masukkan harga jual barang:", initialvalue=barang.harga_jual))
            stok = int(simpledialog.askstring("Edit Barang", "Masukkan stok barang:", initialvalue=barang.stok))
            vendor = simpledialog.askstring("Edit Barang", "Masukkan vendor barang:", initialvalue=barang.vendor)
            barang.update_info(nama, harga_beli, harga_jual, stok, vendor)
            self.save_data()
            self.update_treeview()

    def hapus_barang(self):
        selected_item = self.treeview_barang.selection()
        if selected_item:
            index = self.treeview_barang.index(selected_item)
            self.barang.pop(index)
            self.save_data()
            self.update_treeview()

    def beli_barang(self):
        selected_item = self.treeview_barang.selection()
        if selected_item:
            index = self.treeview_barang.index(selected_item)
            barang = self.barang[index]
            jumlah = int(simpledialog.askstring("Beli Barang", f"Masukkan jumlah pembelian {barang.nama}:"))
            barang.tambah_stok(jumlah)
            self.barang[index] = barang
            self.save_transaction(barang.nama, "Beli", jumlah, barang.harga_beli)
            self.save_data()
            self.update_treeview()

    def jual_barang(self):
        selected_item = self.treeview_barang.selection()
        if selected_item:
            index = self.treeview_barang.index(selected_item)
            barang = self.barang[index]
            jumlah = int(simpledialog.askstring("Jual Barang", f"Masukkan jumlah penjualan {barang.nama}:"))
            if barang.kurangi_stok(jumlah):
                self.barang[index] = barang
                self.save_transaction(barang.nama, "Jual", jumlah, barang.harga_jual)
                self.save_data()
                self.update_treeview()

    def save_transaction(self, nama_barang, jenis_transaksi, jumlah, harga):
        with open("transaksi.txt", "a") as file:
            waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{waktu},{nama_barang},{jenis_transaksi},{jumlah},{harga}\n")

    def tampilkan_transaksi(self):
        transaksi_window = tk.Toplevel(self)
        transaksi_window.title("Daftar Transaksi")

        treeview_trans = ttk.Treeview(transaksi_window, columns=("Waktu", "Nama Barang", "Jenis Transaksi", "Jumlah", "Harga"), show="headings")
        treeview_trans.heading("Waktu", text="Waktu")
        treeview_trans.heading("Nama Barang", text="Nama Barang")
        treeview_trans.heading("Jenis Transaksi", text="Jenis Transaksi")
        treeview_trans.heading("Jumlah", text="Jumlah")
        treeview_trans.heading("Harga", text="Harga")
        treeview_trans.pack(padx=10, pady=10, fill="both", expand=True)

        try:
            with open("transaksi.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if data[2] == "Beli":
                        harga = float(data[4]) * int(data[3])
                    else:
                        harga = float(data[4]) * int(data[3])
                    treeview_trans.insert("", tk.END, values=[data[0], data[1], data[2], data[3], harga])
        except FileNotFoundError:
            pass

    def cari_barang(self):
        query = self.entry_cari.get().lower()
        results = []
        for barang in self.barang:
            if query in barang.nama.lower():
                results.append(barang)
        if results:
            self.update_treeview(results)
        else:
            messagebox.showinfo("Info", "Barang tidak ditemukan.")

if __name__ == "__main__":
    app = AplikasiInventaris()
    app.mainloop()
