

from slugify import slugify as pkgslugify

'''  
Make a slug from the given text.  

Potential kwargs are:
:param entities (bool): converts html entities to unicode (foo &amp; bar -> foo-bar)
:param decimal (bool): converts html decimal to unicode (&#381; -> Ž -> z)
:param hexadecimal (bool): converts html hexadecimal to unicode (&#x17D; -> Ž -> z)
:param max_length (int): output string length
:param word_boundary (bool): truncates to end of full words (length may be shorter than max_length)
:param save_order (bool): if parameter is True and max_length > 0 return whole words in the initial order
:param separator (str): separator between words
:param stopwords (iterable): words to discount
:param regex_pattern (str): regex pattern for allowed characters
:param lowercase (bool): activate case sensitivity by setting it to False
:param replacements (iterable): list of replacement rules e.g. [['|', 'or'], ['%', 'percent']]
:return (str): slugify text
'''
def slugify(val, **kwargs):
    callargs = {
        'text': val,
        'entities': True,
        'separator': "_",
        'stopwords': ["the", "an", "a"],
        'lowercase': True
    }

    callargs = callargs | kwargs
    return pkgslugify(**callargs)



def split_string_list(val, delim=","):
    l = str(val).split(delim)
    return [v.strip() for v in l]
