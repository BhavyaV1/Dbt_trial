import requests

url = 'https://api.stitchdata.com/v4/sources/426879/sync'

payload = {}
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer at_960a3408b2aa996343baadc98e9bf401'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
