"""Sozlukten bilgiyi indirip uyumlu formata donusturur."""

from datetime import datetime

import requests
from lxml import html


EKSI_BASE_URL = "https://eksisozluk.com/"
EKSI_ENTRY_URL = EKSI_BASE_URL + "entry/"

ENTRY_BODY_XPATH = r'//*[@id="entry-item-list"]/li/div[1]'
ENTRY_FAV_XPATH = r'//*[@id="entry-item-list"]/li/footer/div[1]/span[3]/a[2]'
ENTRY_AUTHOR_XPATH = r'//a[@class="entry-author"]'
ENTRY_DATE_XPATH = r'//a[@class="entry-date permalink"]'


def _normalize_date(date: str) -> str:
    """
    Modifiye edilme tarihini sil ve string olan tarih-zaman verisini datetime 
    objesine cevir.

    Args:
        date: Ciplak tarih zaman stringi
    Return:
        tuple: Original date and time.
    Ornek:
        '18.05.2018 17:50 ~ 18:30' -> datetime(2018, 5, 18, 17, 50)
    """
    original_date = date.split(' ~ ')[0]

    # sozluk ilk kuruldugunda entry tarihlerindeki saat tutulmazmis.
    # eger saat yazarken string'in icinde bulunan : varsa saatle beraber 
    # yazdiriyoruz. Yoksa 00:00 olarak yazdiriyoruz.
    if ':' in original_date:
        # TODO: bunun daha iyi bir yolu vardir
        return datetime.strptime(original_date, '%d.%m.%Y %H:%M')
    else:
        return datetime.strptime(original_date + ' 00:00', '%d.%m.%Y %H:%M')


def _is_entry_available(page_content: str) -> bool:
    """Entry silinmisse false return eder."""
    if 'data-not-found="true"' in page_content:
        return False
    return True


def get_entry_by_id(entry_id):
    """
    Entry numarasindan bilgiyi ayirir.

    Args:
        entry_id: Entry numarasi
    Returns:
        dict objesi:
            - id: int, entry numarasi
            - owner: str, yazar ismi
            - body: str, entry icerigi
            - date: date, olusturulma tarihi
            - fav: int, fav sayisi
        Entry silinmisse None dondurur
    """
    response = requests.get(EKSI_ENTRY_URL + str(entry_id))
    page_content = response.content.decode('utf-8')

    with open('content.html', 'w') as file:
        print(page_content, file=file)

    if not _is_entry_available(page_content):
        return None
    
    tree = html.fromstring(page_content)
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
