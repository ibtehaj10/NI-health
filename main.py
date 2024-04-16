#importing required Dependencies
import requests
import base64
from io import BytesIO
import json
from PIL import Image
import requests
import json
import datetime
from concurrent.futures import ThreadPoolExecutor



######################## Image Generation Test
def imagine_image(message, username):


        url = "http://65.108.32.175:8002/imagegen"

        payload = json.dumps({
  "messages": message,
  "type": 'true',
})
        headers = {
  'Content-Type': 'application/json',
   "Authorization": f"Bearer LoTuFvRqEHhJuTdl6V7yh-adBsVSegPRNGD9WMOsplI1xpVTIg8ON1OydyCecs9v",
}

        response = requests.request("POST", url, headers=headers, data=payload)
        try:
            if str(response.status_code) == "200":
                    # print(response.status_code)
                    json_resp = json.loads(response.text)
                    image_b64 = json_resp['choices'][0]['location'].split(',')[1]
                    image_data = base64.b64decode(image_b64)
                    image_stream = BytesIO(image_data)
                    image = Image.open(image_stream)
                    filenames = 'images/'+username+'.jpg'
                    image.save(filenames, format="JPEG")
                    # print(filenames)
                    # print('PASS')
                    return {'status':'PASS','status_code':response.status_code}
            else:
                    print(response.status_code)
                    return {'status':'FAIL','status_code':response.status_code}
        except:
             return  {'status':'FAIL','status_code':response.status_code}
        

############################# Send message on Slack
def send_msg_slack(strr):
    

    url = ""

    payload = json.dumps({
    "text": strr
    })
    headers = {
    'Content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return 'ok'


# Define your sets of arguments for each function call
tasks = [
    ("Tom & Jerry", "1"),
    ("john wick", "2"),
    ("GOKU", "3"),
    ("Harry potter", "4"),
    ("The Batman", "5"),
        ("Vegita", "6"),
    ("JOHN CENA", "7"),
    ("J cole", "8"),
        ("Eminem", "9"),
    ("trasnformer optimus prime", "10")
]



count = []
# Function to wrap the execution of imagine_image, unpacking the arguments
def execute_task(args):
    return imagine_image(*args)


# Run the imagine_image function in parallel using ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(execute_task, task) for task in tasks]
    print(futures)
    # Wait for all futures to complete and print their results
    for i, j in enumerate(futures):
        # print(str(i)+" "+str(j.result()))
        print('Result : ',j.result())
        
        a = j.result()
        if a['status'] == 'FAIL':
            count.append(i)
            send_msg_slack(str("Test Failed at "+str(datetime.datetime.now())))


print(count)
print(len(count))
c = len(count)
if count != []:
    send_msg_slack(str(c)+" requests fails out of 10!")
count = []
