"""Download entry data en masse and save the data to disk for later usage."""

from datetime import datetime

import requests
from lxml import html


EKSI_BASE_URL = "https://eksisozluk.com/"
EKSI_ENTRY_URL = EKSI_BASE_URL + "entry/"

ENTRY_BODY_XPATH = r'//*[@id="entry-item-list"]/li/div[1]'
ENTRY_FAV_XPATH = r'//*[@id="entry-item-list"]/li/footer/div[1]/span[3]/a[2]'
ENTRY_AUTHOR_XPATH = r'//*[@id="entry-item-list"]/li/footer/div[2]/a[2]'
ENTRY_DATE_XPATH = r'//*[@id="entry-item-list"]/li/footer/div[2]/a[1]'


def _normalize_date(self, date: str) -> str:
    """
    Remove the modification date and split the datetime format into 
    seperate date and time format.
    Args:
        date: Raw date time string
    Returns:
        tuple: Original date and time.
    Example:
        '18.05.2018 17:50 ~ 18:30' -> datetime(2018, 5, 18, 17, 50)
    """
    original_date = date.split(' ~ ')[0]
    return datetime.strptime(original_date, '%d.%m.%Y %H:%M')


def _is_entry_available(self, page_content: str) -> bool:
    """Return false if the entry has been deleted."""
    if 'data-not-found="true"' in page_content:
        return False
    return True


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
    if _is_entry_available(content):
        return None
    
    tree = html.fromstring(content)
    owner = tree.xpath(ENTRY_AUTHOR_XPATH + '/text()')[0]
    body_elems = []
    for elem in tree.xpath(ENTRY_BODY_XPATH + '//text()'):
        body_elems.append(elem.strip())
    body = " ".join(body_elems)
    date = _normalize_date(
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