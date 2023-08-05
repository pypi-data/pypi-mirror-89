from pathlib import Path

from django.utils.text import slugify


def filename2human_name(filename):
    """
    Convert filename to a capitalized name, e.g.:

    >>> filename2human_name('bar.py')
    'Bar'
    >>> filename2human_name('No file-Extension!')
    'No File Extension'
    >>> filename2human_name('Hör_gut-zu!.aac')
    'Hör Gut Zu'
    """
    txt = filename.partition('.')[0]
    txt = slugify(txt, allow_unicode=True)
    txt = txt.replace('_', ' ').replace('-', ' ')
    txt = ' '.join(word.capitalize() for word in txt.split())
    return txt


def clean_filename(filename):
    """
    Convert filename to ASCII only via slugify, e.g.:

    >>> clean_filename('bar.py')
    'bar.py'
    >>> clean_filename('No-Extension!')
    'no_extension'
    >>> clean_filename('testäöüß!.exe')
    'testaou.exe'
    >>> clean_filename('nameäöü.extäöü')
    'nameaou.extaou'
    """
    def convert(txt):
        txt = slugify(txt, allow_unicode=False)
        return txt.replace('-', '_')

    suffix = Path(filename).suffix
    if suffix:
        filename = filename[:-len(suffix)]
        suffix = f'.{convert(suffix)}'
    filename = convert(filename)
    return f'{filename}{suffix}'
