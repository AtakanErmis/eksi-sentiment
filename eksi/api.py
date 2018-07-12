"""Download entry data en masse and save the data to disk for later usage."""

from datetime import datetime

import requests
from lxml import html

from . import utils


EKSI_BASE_URL = "https://eksisozluk.com/"
EKSI_ENTRY_URL = EKSI_BASE_URL + "entry/"

ENTRY_BODY_XPATH = r'//*[@id="entry-item-list"]/li/div[1]'
ENTRY_FAV_XPATH = r'//*[@id="entry-item-list"]/li/footer/div[1]/span[3]/a[2]'
ENTRY_AUTHOR_XPATH = r'//*[@id="entry-item-list"]/li/footer/div[2]/a[2]'
ENTRY_DATE_XPATH = r'//*[@id="entry-item-list"]/li/footer/div[2]/a[1]'


# def download_api(start=1, end=None, access_token=None):
#     """Download entry data between ids `start` amd `end`"""
#     if not access_token:
#         raise ConnectionError("Access Token must be given. "
#                               "See https://eksisozluk.herokuapp.com")
#  
#     it = start
#     while True:
#         ret = requests.get(
#             f"https://eksisozluk.herokuapp.com/api/entries/{it}", 
#             params={ "accessToken": access_token }
#         )
#         it += 1
#         return ret.text


def get_entry_by_id(entry_id):
    """
    Retrieve entry information from entry_id.
    Args:
        entry_id: Entry ID
    Returns:
        dict object with keys:
            - id: int, entry id
            - owner: str, author of the entry
            - body: str, entry text
            - date: date, entry date (does not include modification date)
            - fav: int, number of 'fav's
        None if the specified entry cannot be found
    """
    response = requests.get(EKSI_ENTRY_URL + str(entry_id))
    page_content = response.content.decode('utf-8')

    # pass if the entry has been 404'ed
    if utils.is_entry_available(content):
        return None
    
    tree = html.fromstring(content)
    owner = tree.xpath(ENTRY_AUTHOR_XPATH + '/text()')[0]
    body_elems = []
    for elem in tree.xpath(ENTRY_BODY_XPATH + '//text()'):
        body_elems.append(elem.strip())
    body = " ".join(body_elems)
    date = utils.normalize_date(
        tree.xpath(ENTRY_DATE_XPATH + '/text()')[0]
    )
    try:
        fav = int(tree.xpath(ENTRY_FAV_XPATH + '/text()')[0])
    except IndexError:
        # this element does not exist if the favcount of the entry is 0
        # and so it raises IndexError
        fav = 0
    
    entry = {
        'id': entry_id,
        'owner': owner,
        'body': body,
        'date': date,
        'fav': fav
    }

    return entry    

if __name__ == "__main__":
    x = get_entry_by_id(1)
    print(x['body'])