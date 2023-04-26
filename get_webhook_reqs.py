import requests

# example url: https://webhook.site/#!/196c8880-7a6b-4909-a05f-b44617d86bba/cd958aa2-2483-45a5-8c3c-8050a7ab814c/1

token_id = "196c8880-7a6b-4909-a05f-b44617d86bba"       # the first string
headers = {"api-key": "91ffd168-ccf8-4bf9-9958-18515c4844dc"}   #the second string


r = requests.get('https://webhook.site/token/'+ token_id +'/requests?sorting=newest', headers=headers)

for request in r.json()['data']:
    print(request)