import requests
import json
import time

startDate=1558341210
stopDate=1595234010



peer_id=139143886

count=requests.get("https://api.vk.com/method/messages.getHistory?access_token=2b69aa5aeca20b579071ee6308d5635b215f6a615e5d1a562d68e1c7ad241a55b4c867c5e88b4155e1aaf&v=5.124&user_id="+str(peer_id)+"&count=200&offset=0").text
count=json.loads(count)['response']['count']
print("COUNT: ",count)
for i in range(0,(count//200)+200):

    result = requests.get(
        "https://api.vk.com/method/messages.getHistory?access_token=2b69aa5aeca20b579071ee6308d5635b215f6a615e5d1a562d68e1c7ad241a55b4c867c5e88b4155e1aaf&v=5.124&user_id=" + str(
            peer_id) + "&count=200&offset="+str(i*200)).text

    result=json.loads(result)
    print(str(i*200))
    delIds=[]
    for j in range(0,len(result['response']['items'])):
        if(stopDate>=result['response']['items'][j]['date']>=startDate):
            delIds.append(str(result['response']['items'][j]['id']))
    if(len(delIds)>1):

        resulte = requests.get(
            "https://api.vk.com/method/messages.delete?access_token=5f9fe98ab0b73cd331ca4cb3b99cea85645680dff5e6c4b13d334ca9bc3e21dc34e2fb15b0f40a52db5d9&v=5.124&message_ids=" + str(
                ",".join(delIds))).text
        print("DELETE")
        time.sleep(0.5)
    else:
        time.sleep(0.5)

