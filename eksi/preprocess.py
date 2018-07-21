import re

def remove_bkzs(string: str) -> str:
    """
    Verilen stringdeki `bakiniz` bloklarini siler.
    Return:
        string: `bakiniz`lari silinmis string
    Example:
        >>> remove_bkzs('yok artik (bkz: oha)')
        'yok artik'
    """
    ## bkz'ler silindikten sonra fazladan boşluklar oluşabiliyor.                                                                                                 
    bkzs = re.findall("\(bkz:[^\)]+\)", string)
    for i in bkzs:
        string = string.replace(i, '')
    return string

def get_bkzs(string: str) -> list:
    """
    Verilen stringin icindeki `bakiniz` bloklarinda yazanlari bulur ve liste
    halinde dondurur.
    Return:
        list: `bakiniz`larin icindeki stringler
    Example:
        >>> get_bkzs('(bkz: veni) (bkz: vidi) (bkz: vici)')
        ['veni', 'vidi', 'vici']
    """
    return [i[1:] for i in re.findall("\(bkz:([^/)]+)\)", string)]


def remove_numeric(string: str) -> str:
    """
    Verilen stringin icinden sayilari siler.
    Return:
        str: sayi icerigi silinmis olan `string`
    Example:
        >>> remove_numeric("2018de cikan iphone 10 cok guzel.")
        "de cikan iphone cok guzel."
    """
    numeric = re.findall("[0-9]", string)
    for i in numeric:
        string = string.replace(i, '')
    return string


def remove_links(string: str) -> str:
    """
    Verilen stringden URLleri ve URIlari siler.
    Return:
        str: linkleri silinmis `string`
    Example:
        >>> remove_links("google diye bir sey cikmis: http://google.com/")
        "google diye bir sey cikmis:"
    """
    # silindikten sonra aralarda fazla boşluk olabiliyor
    links = re.findall("(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?", string)
    for i in links:
        string = string.replace(f"{i[0]}://{i[1]}{i[2]}", '')
    return string


def stem(string: str) -> str:
    """
    Verilen stringde cekim eki almis kelimelerden cekim eklerini kaldirir.
    Return:
        str: cekim ekleri silinmis `string`
    Example:
        >>> stem("inceliyoruz")
        "incele"
        >>> stem("telefonunu")
        "telefon"
        >>> stem("kibarlıktan")
        "kibarlık"
    """
    return


def remove_stop_words(string: str) -> str:
    """
    Verilen stringde dilde sentiment uzerine degisim yaratmayan kelimeleri 
    siler.
    Return:
        string: stop word'ler silinmis `string`
    Example:
        >>> remove_stop_word("bu pasta bir harika")
        "pasta harika"
    """
    return
