import re
import string
import unicodedata
import emoji
from bs4 import BeautifulSoup


class TextCleaner(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def rm_punct(self, text, ex=None):
        punct = string.punctuation
        if ex:
            punct = punct.translate(str.maketrans(dict.fromkeys(ex)))
        return text.translate(str.maketrans(dict.fromkeys(punct))).lower()

    def rm_whitespace(self, text):
        return " ".join(x.strip().lower() for x in text.split())

    def rm_char(self, text, rm_char):
        return text.translate(str.maketrans(dict.fromkeys(rm_char))).lower()

    def rm_nonascii(self, text):
        return unicodedata.normalize("NFKD", text.lower()).encode("ascii", "ignore").decode("utf-8", "ignore")

    def rm_emoticons(self, text):
        return re.sub(emoji.get_emoji_regexp(), r"", text.lower())

    def rm_html(self, text):
        return BeautifulSoup(text, "html.parser").get_text().lower()

    def rm_url(self, text):
        regex = r"""(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*|www\S+"""
        return re.sub(regex, "", text.lower())

    def rm_repeat_char(self, text):
        return re.sub(r'(.)\1+', r'\1\1', text.lower())

    def rm_repeat_word(self, text):
        return re.sub(r'(?<!\S)((\S+)(?:\s+\2))(?:\s+\2)+(?!\S)', r'\1', text.lower())

    def rm_numb(self, text):
        return re.sub(r"\d+", "", text.lower())

    def rm_all(self, text):
        all_ = ["rm_hastag",
                "rm_mention",
                "rm_nonascii",
                "rm_emoticons",
                "rm_html",
                "rm_url",
                "rm_punct",
                "rm_repeat_char",
                "rm_repeat_word",
                "rm_numb",
                "rm_whitespace"]
        clean_text = text.lower()
        for i in all_:
            clean_text = eval(f"self.{i}")(clean_text)
        return clean_text

    def rm_set(self, ls_rm):
        self.set_rm = ls_rm

    def rm(self, text):
        clean_text = text.lower()
        for i in self.set_rm:
            clean_text = eval(f"self.{i}")(clean_text)
        return clean_text

    def rm_hastag(self, text):
        return re.sub("#(\w+)", "", text.lower())

    def get_hastag(self, text):
        return re.findall("#(\w+)", text.lower())

    def rm_mention(self, text):
        return re.sub("@(\w+)", "", text.lower())

    def get_mention(self, text):
        return re.findall("@(\w+)", text.lower())


text_cleaner = TextCleaner()
