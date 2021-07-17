from re import split
import sys
import os

from typing import List

import requests
from bs4 import BeautifulSoup
import urllib.request

argv = sys.argv[1:]
base_url = "https://nhentai.net/g/"

current_dir = os.path.abspath(os.path.dirname(__file__))


def validate_argv(argv: List[str]):
    if(len(argv) > 0):
        return True
    else:
        return False


def convert_to_num_arr(arr: List[str]):
    return list(map(
        lambda value: int(value),
        arr
    ))


def get_doujin_metadata(doujin_num: int):
    url = f"{base_url}{doujin_num}"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    title = soup.select("h1.title")[0].getText()

    tags = soup.select("div.tag-container span.tags")
    page_count = tags[-2].getText()

    image_elems = soup.select(
        "div.thumbs div.thumb-container a noscript img")

    image_srcs: List[str] = list(map(
        lambda value: value["src"],
        image_elems
    ))

    return [title, image_srcs]


def get_gallery_src_from_thumbnail_src(thumbnail_src: str):

    split_src = thumbnail_src.split("/")
    split_src[-1] = split_src[-1].replace("t", "")
    split_src[2] = split_src[2].replace("t", "i", 1)

    thumbnail_src = "/".join(split_src)

    return thumbnail_src


def ensure_image_folder_exists(doujin_title: str):
    folder = os.path.join(current_dir, doujin_title)
    if not os.path.isdir(folder):
        os.mkdir(folder)

    return folder


def download_image_from_src(src: str, folder: str):

    # Check if destination exists
    image_name = src.split("/")[-1]
    dest = os.path.join(folder, image_name)

    if not os.path.exists(dest):
        urllib.request.urlretrieve(src, dest)


def download_doujin(title: str, image_srcs: List[str]):
    dest_folder = ensure_image_folder_exists(title)

    for thumb_src in image_srcs:
        gallery_src = get_gallery_src_from_thumbnail_src(thumb_src)
        download_image_from_src(gallery_src, dest_folder)


def main():
    nums = convert_to_num_arr(argv)

    [title, image_srcs] = get_doujin_metadata(nums[0])
    download_doujin(title, image_srcs)


main()
