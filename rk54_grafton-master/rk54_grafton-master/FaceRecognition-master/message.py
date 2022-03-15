import requests
url = "https://www.fast2sms.com/dev/bulk"
test="hello"
payload = "sender_id=FSTSMS&message={}&language=english&route=p&numbers=8160756915".format(test)

headers = {
'authorization': "Gkpe7Y3UWOISLxMdVXHDmjJb6zNuf5aTwrt4ivcRo8B29sAPlnQowaeR0DHdvNWk45xpqOShyGlLcVIj",
'Content-Type': "application/x-www-form-urlencoded",
'Cache-Control': "no-cache",
}
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)