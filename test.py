import re
import json

def correct(text):
    text=re.sub("\s","",text)
    return text

def result(text):
    # скобки (\(([\d\.]*[\+\-\*\/][\d\.]*)*\))
    # умножение/деление ([\d\.]*[\*\/][\d\.]*)
    # сложение/умножение ([\d\.]*[\+\-][\d\.]*)

    # сначала считаем то, что в скобках
    skob = json.loads(
        json.dumps(re.findall("(\(([\-\d\.]*[\+\-\*\/][\-\d\.]*)*\))", text, re.MULTILINE | re.VERBOSE)))
    while (len(skob) > 0):
        nach = skob[0][0]
        op = re.findall("([\-\d\.]*[\*\/\^][\-\d\.]*)", skob[0][0])
        while (len(op) > 0):
            opp = re.findall("([\-\d\.]*)([\+\-\*\/\^])(\-\d*)", op[0])[0]
            if (opp[1] == '*'):
                res = str(float(opp[0]) * float(opp[2]))
            elif (opp[1] == "/"):
                res = str(float(opp[0]) / float(opp[2]))
            elif (opp[1] == "^"):
                res = str(float(opp[0]) ** float(opp[2]))
            skob[0][0] = skob[0][0].replace(op[0], res)
            op = re.findall("([\-\d\.]*[\*\/\^][\-\d\.]*)", skob[0][0])

        op = re.findall("([\-\d\.]*[\+\-][\-\d\.]*)", skob[0][0])
        while (len(op) > 0):
            opp = re.findall("([\-\d\.]*)([\+\-\*\/])(\-\d*)", op[0])[0]
            if (opp[1] == '+'):
                res = str(float(opp[0]) + float(opp[2]))
            elif (opp[1] == "-"):
                res = str(float(opp[0]) - float(opp[2]))
            skob[0][0] = skob[0][0].replace(op[0], res)

            op = re.findall("([\-\d\.]*[\*\/][\-\d\.]*)", skob[0][0])

        text = text.replace(nach, re.sub("[\)\(]", "", skob[0][0]))

        skob = json.loads(
            json.dumps(re.findall("(\(([\-\d\.]*[\+\-\*\/][\-\d\.]*)*\))", text, re.MULTILINE | re.VERBOSE)))

    # а теперь, что без скобок
    op = re.findall("([\-\d\.]*[\*\/\^][\-\d\.]*)", text)
    while (len(op) > 0):
        opp = re.findall("([\-\d\.]*)([\+\-\*\/\^])(\-\d*)", op[0])[0]
        print(opp)
        print(text)
        if (opp[1] == '*'):
            res = str(float(opp[0]) * float(opp[2]))
        elif (opp[1] == "/"):
            res = str(float(opp[0]) / float(opp[2]))
        elif (opp[1] == "^"):
            res = str(float(opp[0]) ** float(opp[2]))

        text = text.replace(op[0], res)
        op = re.findall("([\-\d\.]*[\*\/\^][\-\d\.]*)", text)
    op = re.findall("([\-\d\.]*[\+\-][\-\d\.]*)", text)
    while (len(op) > 0):
        opp = re.findall("([\-\d\.]*)([\+\-\*\/])(\-\d*)", op[0])[0]
        if (opp[1] == '+'):
            res = str(float(opp[0]) + float(opp[2]))
        elif (opp[1] == "-"):
            res = str(float(opp[0]) - float(opp[2]))

        text = text.replace(op[0], res)
        op = re.findall("([\-\d\.]*[\+\-][\-\d\.]*)", text)

    return str(text)


print(result(correct("748 * (15 + 3 * (15 / 15 * 1 + 2 * (79 + 5))) / (7 + 8) + 13")))
