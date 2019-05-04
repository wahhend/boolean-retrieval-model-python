import re

class Document:
    def __init__(self, title, text):
        self.title = title.lower()
        self.text = text.lower()
        self.words = self.get_words()

    def get_words(self):
        regex = r"[a-zA-Z]{2,}"
        return re.findall(regex, self.title+" "+self.text)
