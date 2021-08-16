import requests
import lxml.html
from bs4 import BeautifulSoup
import os
import argparse

# gets the maximum page count


def get_Followed_Pages(username, savedir):
    url = "https://bsaber.com/songs/new/?bookmarked_by=" + str(username)
    request = requests.get(url).text
    tree = lxml.html.fromstring(request)
    page_number = tree.xpath(
        '//*[@id="content-container"]/div[2]/div/section/div[2]/a[3]')[-1]
    max_pages = int(page_number.text_content()) + 1
    print(savedir)
    for f in range(1, max_pages):
        links = []
        url = "https://bsaber.com/songs/new/page/" + \
            str(f) + "/?bookmarked_by=" + str(username)
        links.append(url)
        Get_Song_Links(links, savedir)

# gets the links for the songs


def get_Song_Links(links, savedir):
    for url in links:
        request = requests.get(
            url).text
        soup = BeautifulSoup(request, "lxml")
        for link in soup.find_all(
                "a", {"class": "action post-icon bsaber-tooltip -download-zip"}, href=True):
            link_for_download = link['href']
            Download_Songs(link_for_download, savedir)

# downloads the songs


def download_Songs(url, savedir, chunk_size = 128 ):
    filename = os.path.basename(url + str(".zip"))
    completeName = os.path.join(savedir, filename)
    r = requests.get(url, stream=True)
    with open(completeName, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

# parses the username and the path argument


def parse_arg():
    my_parser = argparse.ArgumentParser(
        description='Downloads your favourite songs from bsaber.com')
    my_parser.add_argument('--username',
                           metavar='Username',
                           type=str,
                           help='The username which favourites will be downloaded')
    my_parser.add_argument('--path',
                           metavar='Path',
                           type=str,
                           help='Path where the songs will be saved')

    args = my_parser.parse_args()
    username = args.username
    savedir = args.path
    Get_Followed_Pages(username, savedir)


if __name__ == "__main__":
    parse_arg()
