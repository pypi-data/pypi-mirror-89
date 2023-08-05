# simager
Tools for cleaning or preprocessing text data

## Features
```
- Remove Hastag, mention, nonascii, emoticons, html tag, punctuation,
  character, repeated character, repeated word, number, whitespace
- Stopword Operation
- Text normalizer Operation
```

## Instalation
```
pip install simager
```
## Getting Started
```
from simager import text_cleaner, stop_word, normalizer


text_cleaner.rm_url("your text data")

text_cleaner.rm_all("your text data")

text_cleaner.rm_set([
    "rm_hastag",
    "rm_mention",
    "rm_url",
    "rm_punct",
    "rm_whitespace"
])
text_cleaner.rm("your text data")

stop_word.remove("your text data")

normalizer.text("your text data")
```
Full Example Usage [Here](https://github.com/ulwan/simager/tree/master/simager/example)

