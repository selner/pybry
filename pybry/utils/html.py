import codecs, os
from bs4 import BeautifulSoup

class Soupier(BeautifulSoup):

    def __init__(self, *args, **kwargs):
        if 'features' not in kwargs:
            kwargs['features'] = "html.parser"

        BeautifulSoup.__init__(self, *args, **kwargs)

    def dump_to_file(self, bsitem):
        filepath = os.path.abspath("./soupier_dump.html")
        f = codecs.open(filepath, encoding='utf-8', mode='w+')
        f.write(str(bsitem))
        f.close()

        return filepath
