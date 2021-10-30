from fastapi import FastAPI
from collections import Counter
import re
from googletrans import Translator
import pandas as pd
# c0wijwa4_92UTS4NCavdhLYsSrHr5Qpz7pYNpc4Lw
# c0wijwa4

app = FastAPI()
translator = Translator()

@app.get("/address/{input}")
async  def address(input):
    org_lang = translator.detect(input).lang
    out = translator.translate(input, dest="en")
    input = out.text


    def contains(TestVar, elements):
        #print(TestVar, elements)
        for element in elements:
            if element == TestVar:
                #print('True')
                return True
        return False


    def OcrAddressCheck(OcrAddress):
        tempList = {'district': '', 'sub_district': ''}
        districtNames = pd.read_csv('Districts.csv')
        subDistrictNames = pd.read_csv('Sub_districts.csv')
        districtNamesList = list(districtNames['Districts'])
        subDistrictNamesList = list(subDistrictNames['Sub_districts'])
        ocrAddressList = list(((OcrAddress.lower()).replace(',', '')).split(' '))

        i = 0
        # print('Districts')
        for elements in districtNamesList:
            if contains(elements.lower(), ocrAddressList):
                # print('districtNamesList')
                i += 1
                tempList['district'] = elements
                #print(i)
                break

        #print('Sub Districts')
        for elements in subDistrictNamesList:
            if contains(elements.lower(), ocrAddressList):
                #print('subDistrictNamesList')
                # print(elements)
                #print(i)
                tempList['sub_district'] = elements
                i += 1
                break
        #print('end',i)
        if i == 2:
            return tempList
        return False


    input = 'oh god what is this behaviour pooja Handwara Anantnag'
    input = input.lower()
    # words = my_address.split()
    # new_address = " ".join(sorted(set(words), key=words.index))

    input = input.split(" ")

    for i in range(0, len(input)):
        if input[i] == "new" or input[i] == "old" or input[i] == "lower" or input[i] == "upper" or input[i] == "east" or input[i] == "west" or input[i] == "north" or input[i] == "south":
            input[i] = input[i] + " " + input[i + 1]
            input[i + 1] = " "


    UniqW = Counter(input)
    print(UniqW)

    s = " ".join(UniqW.keys())
    s = re.sub("\s\s+", " ", s)

    if isinstance(org_lang, list):
        s = translator.translate(s, dest=org_lang[0]).text
    else:
        s = translator.translate(s, dest=org_lang).text
    print(s)
    Dictionary1 = OcrAddressCheck(s)
    if Dictionary1:
        answer = s + '\n'+'District: ' + \
            Dictionary1['district'] + '\n' + \
            'Sub District: '+Dictionary1['sub_district']
        return answer
    else:
        return s

