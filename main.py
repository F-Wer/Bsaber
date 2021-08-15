import requests
import lxml.html
from bs4 import BeautifulSoup
import re


def Get_Followed_Pages():
    url = "https://bsaber.com/songs/new/?bookmarked_by=llojassd"

    request = requests.get(url).text
    tree = lxml.html.fromstring(request)
    page_number = tree.xpath(
        '//*[@id="content-container"]/div[2]/div/section/div[2]/a[3]')[-1]
    max_pages = int(page_number.text_content()) + 1

    for f in range(1, max_pages):
        links = []
        url = "https://bsaber.com/songs/new/page/" + \
            str(f) + "/?bookmarked_by=llojassd"
        links.append(url)
        Get_Song_Links(links)


def Get_Song_Links(links):
    savedir = "F:\Test"
    for url in links:
        request = requests.get(
            url).text
        soup = BeautifulSoup(request, "lxml")
        for link in soup.find_all(
                "a", {"class": "action post-icon bsaber-tooltip -download-zip"}, href=True):
            link_for_download = link['href']
            Downlaod_Songs(link_for_download, savedir)


def Downlaod_Songs(url, save_path, chunk_size=128):
    print(url)
    r = requests.get(url, stream=True)
    with open("F:\Test", 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


if __name__ == "__main__":
    Get_Followed_Pages()
