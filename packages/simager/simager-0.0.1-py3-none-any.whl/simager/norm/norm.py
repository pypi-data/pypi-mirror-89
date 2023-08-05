import pickle
import pkg_resources


class Normalizer(object):
    def __init__(self, *args, **kwargs):
        self.norm_path = pkg_resources.resource_filename("simager", "data/normalizer.p")
        self.normalizer = pickle.load(open(self.norm_path, "rb"))
        super().__init__(*args, **kwargs)

    def get(self):
        return self.normalizer

    def add(self, dict_):
        if isinstance(dict_, dict):
            self.normalizer.update(dict_)
        else:
            raise TypeError("You must provide dictionary type of data")

    def remove(self, keys):
        if isinstance(keys, list):
            for i in keys:
                if i in self.normalizer:
                    self.normalizer.pop(i)
        else:
            raise TypeError("You must provide list type of data")

    def text(self, text):
        return " ".join([self.normalizer.get(str(i), str(i)) for i in text.lower().split()])


normalizer = Normalizer()
