import requests


def query(method, params, token="753593125:AAHvUANvzJwY6cwmXW6t9QigimAcuimijjs",headers=None,files=None):
    pr: str = ""
    for i in params.keys():
        pr = str(pr) + "&" + str(i) + "=" + str(params.get(i))

    return requests.post("https://api.telegram.org/bot" + token + "/" + method, data=params,headers=headers,files=files)


