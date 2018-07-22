import re


# bkzlari match eder, ama sadece bkz icindeki text'i gruplara alir.
REGEX_BKZ = re.compile(r"(?:\(bkz: )([a-z0-9 ]+)(?:\))")

# noktalama işaretlerini match eder.
REGEX_PUNC = re.compile(r"[.,:;!-?]")

# string icinde yanyana gelmis ikiden fazla bosluk karakterini ve
# stringin bas ve sonundaki herhangi bosluk kararkterini match eder
REGEX_UNNEEDED_WHITESPACE = re.compile(r" {2,}")
REGEX_TRIMMABLE_WHITESPACE = re.compile(r"^ *| *$")


def _trim_spaces(string: str) -> str:
    """
    Verilen stringin icinden gereksiz bosluklari siler.
    Return:
        string: gereksiz bosluklari silinmis string
    Example:
        >>> _trim_spaces('abartili    deneme  yazisi')
        'abartili deneme yazisi'
    """
    return re.sub(
        REGEX_TRIMMABLE_WHITESPACE, 
        '',
        re.sub(REGEX_UNNEEDED_WHITESPACE, ' ', string)
    )


def remove_bkzs(string: str) -> str:
    """
    Verilen stringdeki `bakiniz` bloklarini siler.
    Return:
        string: `bakiniz`lari silinmis string
    Example:
        >>> remove_bkzs('yok artik (bkz: oha)')
        'yok artik'
    """
    return _trim_spaces(re.sub(REGEX_BKZ, '', string))


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
    return re.findall(REGEX_BKZ, string)


def remove_numeric(string: str) -> str:
    """
    Verilen stringin icinden sayilari siler.
    Return:
        str: sayi icerigi silinmis olan `string`
    Example:
        >>> remove_numeric("2018de cikan iphone 10 cok guzel.")
        "de cikan iphone cok guzel."
    """
    return _trim_spaces(re.sub("[0-9]", '', string))


def remove_links(string: str) -> str:
    """
    Verilen stringden URLleri ve URIlari siler.
    Return:
        str: linkleri silinmis `string`
    Example:
        >>> remove_links("google diye bir sey cikmis: http://google.com/")
        "google diye bir sey cikmis:"
    """
    return _trim_spaces(
        re.sub(r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))"
               r"([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?",
               '',
               string)
    )


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
