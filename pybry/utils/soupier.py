import codecs, os
from bs4 import BeautifulSoup


class Soupier(BeautifulSoup):

    @staticmethod
    def from_node(bsnode, *args, **kwargs):
        if 'features' not in kwargs:
            kwargs['features'] = "html.parser"

        return Soupier(bsnode, *args, **kwargs)

    @staticmethod
    def from_content(content, *args, **kwargs):
        if 'features' not in kwargs:
            kwargs['features'] = "html.parser"
        kwargs['markup'] = str(content)
        
        return Soupier(*args, **kwargs)


    def __init__(self, filepath=None, *args, **kwargs):
        if 'features' not in kwargs:
            kwargs['features'] = "html.parser"
        
        if filepath:
            with open(filepath, "r") as fp:
                kwargs['markup'] = fp.read()

        BeautifulSoup.__init__(self, *args, **kwargs)

    def dump_to_file(self, bsitem=None, filepath=None):
        if not filepath:
            filepath = os.path.abspath("./soupier_dump.html")
        f = codecs.open(filepath, encoding='utf-8', mode='w+')
        if not bsitem:
            bsitem = self.decode(pretty_print=True)
        f.write(str(bsitem))
        f.close()

        return filepath
