import requests
import shutil
import os
from merek import Merek
from bs4 import BeautifulSoup

def parse_content(keyword, raw_result, list_merek):
    parse_results = []

    keyword = keyword.replace(" ", "")

    #create directory based on keyword
    if (keyword != "" and os.path.exists(keyword) == False):    
        os.mkdir(keyword)
        os.mkdir(keyword + "/images")

    html_records = raw_result.find_all(class_="item-list-result")
    
    for html_record in html_records:
        record = Merek()
        record.nomor_permohonan = html_record.find(class_="number").text
        record.nama = html_record.find("a", class_="title").text
        record.detail_link = html_record.find("a", class_="title", href=True)['href']
        record.status = html_record.find(class_="status").text
        record.url_logo = html_record.find("img", class_="lazy")['data-src']
        print("Processing " + record.nomor_permohonan + " - " + record.nama)
        download_image(keyword, record.nomor_permohonan, record.url_logo)
        get_detail(record)
        list_merek.append(record)

    return

def download_image(keyword, nomor_permohonan, url_logo):
    if (url_logo == ""):
        return
    else:
        filename = keyword + "/images/" + nomor_permohonan + ".jpg"
        if (os.path.exists(filename) == False):
            req = requests.get(url_logo, stream=True)
            if (req.status_code == 200):
                req.raw.decode_content = True
                with open(filename, "wb") as f:
                    shutil.copyfileobj(req.raw, f)
                
                print(nomor_permohonan + " - Image downloaded")

def get_detail(record):
    req = requests.get(record.detail_link)
    soup = BeautifulSoup(req.content, "html.parser")
    container_top = soup.find("div", class_="top")
    container_detail = soup.find_all("div", class_="container-detail")[1]
    container_top_span1s = container_top.find(class_="row").find_all(class_="span-1")
    i = 0
    for container_top_span1 in container_top_span1s:
        if (i == 0):
            record.nomor_pengumman = container_top_span1.find("p").contents[0]
        if (i == 1):
            record.tgl_pengumuman = container_top_span1.find("p").contents[0]
        if (i == 3):
            record.tgl_penerimaan = container_top_span1.find("p").contents[0]
        if (i == 4):
            record.tgl_mulai_perlindungan = container_top_span1.find("p").contents[0]
        if (i == 5):
            record.tgl_berakhir_perlindungan = container_top_span1.find("p").contents[0]
        i = i + 1

    container_detail_span3s = container_detail.find_all(class_="span-3")
    i = 0
    for container_detail_span3 in container_detail_span3s:
        if (i == 0):
            record.translasi = container_detail_span3.find("p").contents[0]
        if (i == 1):
            two_columns = container_detail_span3.find_all("p", class_="value-u")
            for two_column in two_columns:
                record.kode_kelas_jenis_barang += two_column.contents[0] + "/ "
        if (i == 3):
            record.pemilik_nama = container_detail_span3.find_all(class_="table-row")[1].find_all("li")[0].find("p").contents[0]
            record.pemilik_alamat = container_detail_span3.find_all(class_="table-row")[1].find_all("li")[1].find("p").contents[0]
        i = i + 1



    