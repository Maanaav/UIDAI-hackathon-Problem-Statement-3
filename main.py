from fastapi import FastAPI
from collections import Counter
import re
from googletrans import Translator

app = FastAPI()
translator = Translator()

@app.get("/address/{input}")
async  def address(input):
    org_lang = translator.detect(input).lang
    out = translator.translate(input, dest="en")
    input = out.text

    input = input.lower()
    # words = my_address.split()
    # new_address = " ".join(sorted(set(words), key=words.index))

    input = input.split(" ")
    print(input)

    for i in range(0, len(input)):
        if input[i] == "new" or input[i] == "old" or input[i] == "lower" or input[i] == "upper" or input[i] == "east" or input[i] == "west" or input[i] == "north" or input[i] == "south":
            input[i] = input[i] + " " + input[i + 1]
            input[i + 1] = " "

    print(input)

    UniqW = Counter(input)
    print(UniqW)

    s = " ".join(UniqW.keys())
    s = re.sub("\s\s+", " ", s)

    if isinstance(org_lang, list):
        s = translator.translate(s, dest=org_lang[0]).text
    else:
        s = translator.translate(s, dest=org_lang).text
    print(s)

    return f"{s}"
