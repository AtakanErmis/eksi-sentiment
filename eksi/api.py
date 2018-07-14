"""Sozlukten bilgiyi indirip uyumlu formata donusturur."""

from datetime import datetime

import requests
from lxml import html


EKSI_BASE_URL = "https://eksisozluk.com/"
EKSI_ENTRY_URL = EKSI_BASE_URL + "entry/"

ENTRY_ENTRY_XPATH = r'//li[@data-favorite-count]'
ENTRY_BODY_XPATH = r'//*[@id="entry-item-list"]/li/div[1]'
ENTRY_AUTHOR_XPATH = r'//a[@class="entry-author"]'
ENTRY_DATE_XPATH = r'//a[@class="entry-date permalink"]'
ENTRY_TOPIC_XPATH = r'//h1[@id="title"]'

TOPIC_ITEM_LIST_XPATH = r'//li[@data-author]'
TOPIC_NEXT_PAGE_XPATH = r'//a[@class="next"]'


def _normalize_date(date: str) -> datetime:
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


def get_entry_by_id(entry_id: int) -> dict:
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
    topic = tree.xpath(ENTRY_TOPIC_XPATH)[0].get('data-title')

    try:
        fav = int(tree.xpath(ENTRY_ENTRY_XPATH)[0].get('data-favorite-count'))
    except IndexError:
        # Bu eleman fav sayisi 0 ise olmuyor, index error veren durumlarda
        # fav sayisi 0 yani
        # TODO: buna daha guzel bir cozum bulunacak
        fav = 0

    entry = {
        'id': entry_id,
        'owner': owner,
        'topic': topic,
        'body': body,
        'date': date,
        'fav': fav
    }

    return entry


def get_entries_by_topic(topic: str) -> list:
    entries = []
    topic_url = requests.get(EKSI_BASE_URL + f"?q={topic}").url

    page = 1
    while True:
        url = topic_url + f"?p={page}"
        response = requests.get(url)
        page_content = response.content.decode('utf-8')

        if not _is_entry_available(page_content):
            break
        
        tree = html.fromstring(page_content)
        elements = tree.xpath(TOPIC_ITEM_LIST_XPATH)

        for elem in elements:
            date = elem.xpath(r'//a[@class="entry-date permalink"]//text()')[0]
            body = ' '.join(elem.xpath(r'//div[@class="content"]//text()'))
            entry = {
                'id': int(elem.get("data-id")),
                'owner': elem.get("data-author"),
                'topic': topic,
                'body': body,
                'date': _normalize_date(date),
                'fav': int(elem.get("data-favorite-count"))
            }
            entries.append(entry)
        
        page += 1

    return entries

# TODO: Profil adindan entry alma yapilacak

# TODO: Link verilip ona gore baslik alma da yapilacak.