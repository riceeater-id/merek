import requests
import urllib
import html
import shutil
import argparse
from bs4 import BeautifulSoup
from content import parse_content
from merek import Merek
from content_writer import write_content_to_file

BASE_URL = "https://pdki-indonesia.dgip.go.id/index.php/merek?"


parser = argparse.ArgumentParser()
parser.add_argument("merek", help="""Merek yang akan dicari, gunakan tanda petik jika ada spasi pada merek contoh: "rice eater" """, type=str)
parser.add_argument("halaman", help="pencarian dimulai dari halaman ke berapa default = 0", type=int)
args = parser.parse_args()

keyword = args.merek
search_type = 1
sort_by = ""
sort_type = "asc"   # asc / desc
start_page = args.halaman
record_per_page = 10

urlparams = {'q': keyword, 'type': search_type, 'skip': start_page * record_per_page, 'sort_by': sort_by, 'sort_type': sort_type}

req = requests.get(BASE_URL + urllib.parse.urlencode(urlparams))
soup = BeautifulSoup(req.content, "html.parser")
total_records = int(soup.find(class_="jml").text)


print("Total Result: " + str(total_records))

list_result = soup.find(class_="list-result")
list_merek = []
header = Merek()

header.nama = "nama"
header.deskripsi = "deskripsi"
header.status = "status"
header.nomor_pengumman = "nomor_pengumman"
header.nomor_permohonan = "nomor_permohonan"
header.tgl_penerimaan = "tgl_penerimaan"
header.tgl_pengumuman = "tgl_pengumuman"
header.tgl_mulai_perlindungan = "tgl_mulai_perlindungan"
header.tgl_berakhir_perlindungan = "tgl_berakhir_perlindungan"
header.translasi = "translasi"
header.kode_kelas_jenis_barang = "kelas/jenis_barang"
header.pemilik_nama = "pemilik_nama"
header.pemilik_alamat = "pemilik_alamat"
header.nationality = "nationality"
header.gambar = "gambar"
header.url_logo = "url_logo"
header.detail_link = ""

total_record_written = 0

list_merek.append(header)

write_content_to_file(keyword, list_merek)

print("Proces Halaman ke: " + str(start_page))
parse_content(keyword, list_result, list_merek)

total_record_written += len(list_merek)
write_content_to_file(keyword, list_merek)

if (total_records > record_per_page):
    page = 1
    total_page = int(total_records / record_per_page)

    for page in range(start_page + 1, total_page + 1):
        print("Proses Halaman ke:" + str(page))
        urlparams = {'q': keyword, 'type': search_type, 'skip': page * record_per_page, 'sort_by': sort_by, 'sort_type': sort_type}
        req = requests.get(BASE_URL + urllib.parse.urlencode(urlparams))
        soup = BeautifulSoup(req.content, "html.parser")
        list_result = soup.find(class_="list-result")
        parse_content(keyword, list_result, list_merek)
        total_record_written += len(list_merek)
        write_content_to_file(keyword, list_merek)

print("Total Merek Yang Diproses: " + str(total_record_written))
print("Selesai")

