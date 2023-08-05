import pickle
import pkg_resources


class StopWord(object):
    def __init__(self, *args, **kwargs):
        self.stop_w_path = pkg_resources.resource_filename("simager", "data/stop_w.p")
        self.stop_w = pickle.load(open(self.stop_w_path, "rb"))
        super().__init__(*args, **kwargs)

    def get(self):
        return self.stop_w

    def add(self, ls):
        if isinstance(ls, list):
            self.stop_w.update(set(ls))
        else:
            raise TypeError("You must provide list type of data")

    def remove(self, text):
        return " ".join([i for i in text.lower().split() if i not in self.stop_w])


stop_word = StopWord()
