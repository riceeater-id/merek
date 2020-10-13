import csv
from merek import Merek

#writing to csv file
def write_content_to_file(keyword, list_merek):
    if (len(list_merek) > 0):
        try:
            path =  keyword.replace(" ", "")
            filename = path + "/hasil.csv"

            print("Tulis ke File: " + filename)
            with open(filename, 'a') as f:
                writer = csv.writer(f, delimiter="|", lineterminator="\n")
                for merek in list_merek:
                    writer.writerow([
                        merek.nama,
                        merek.deskripsi,
                        merek.status,
                        merek.nomor_pengumman,
                        merek.nomor_permohonan,
                        merek.tgl_penerimaan,
                        merek.tgl_pengumuman,
                        merek.tgl_mulai_perlindungan,
                        merek.tgl_berakhir_perlindungan,
                        merek.translasi,
                        merek.kode_kelas_jenis_barang,
                        merek.pemilik_nama,
                        merek.pemilik_alamat,
                        merek.nationality,
                        merek.gambar,
                        merek.url_logo,
                        merek.detail_link,
                    ])
            list_merek.clear()
        except BaseException as e:
            print('BaseException:', filename)
        else:
            print('Data berhasil ditulis !')

    




