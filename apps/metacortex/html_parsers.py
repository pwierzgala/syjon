# -*- coding: utf-8 -*-

from html.parser import HTMLParser


class HTMLParserBase(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
        
    def get_data(self):
        """
        Zwraca przetworzony tekst.
        """
        return ''.join(self.fed)
    
    def parse(self, text):
        if not text:  # Jeżeli text ma wartość None wtedy w momencie wywołania na nim jakiejś funkcji pojawia się błąd
            text = ''
        
        self.feed(text)   
        return self.get_data() 


# -----------------------------------------------------------------
# --- WYSIWYG -> HTML
# -----------------------------------------------------------------

class HTMLParserWYSIWYG(HTMLParserBase):
    """
    Usuwa z kodu HTML wszystkie tagi poza <p>, <ul>, <ol>, <li>, <b>, <u>, <i>, <strike>, <sub>, <sup>, <br> oraz pozbawia je wszystkich atrybutów.
    """
    def __init__(self):
        self.reset()
        self.fed = []
        self.is_in_li = False
            
    def handle_starttag(self, tag, attrs):
        """
        Przetwarza tagi otwierające.
        """
        
        if tag == 'li':
            self.is_in_li = True 
            
        if tag == "p" or tag == 'ul' or tag == 'ol' or tag == 'li' or tag == 'b' or tag == 'strong' or tag == 'u' or tag == 'i' or tag == 'em' or tag == 'strike' or tag == 'sub' or tag == 'sup' or tag == 'br':
            if tag == 'p' and self.is_in_li:
                pass
            else:
                self.fed.append("<%s>" % tag)
                    
    def handle_endtag(self, tag):
        """
        Przetwarza tagi zamykajce.
        """
                
        if tag == 'li':
            self.is_in_li = False
        
        if tag == "p" or tag == 'ul' or tag == 'ol' or tag=='li' or tag == 'b' or tag == 'strong' or tag == 'u' or tag == 'i' or tag == 'em' or tag == 'strike' or tag == 'sub' or tag == 'sup':
            if tag == 'p' and self.is_in_li:
                pass
            else:
                self.fed.append("</%s>" % tag)
            
    def handle_data(self, data):
        """
        Przetwarza tekst. Tekst jest przekazywany w niezmienionej formie.
        """
        self.fed.append(data)
        
    def handle_comment(self, data):
        """
        Prztwarza komentarze. Nie chcemy żadnych komentarzy dlatego ta funkcja nic nie robi.
        """
        pass
