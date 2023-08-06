import requests
import sys

def dudbCheck(userid):
    resCheck = requests.get('https://discord.riverside.rocks/check.json.php?id=' + userid)
    return resCheck.json()

def dudbReport(userid, token, reason):
    resCheck = requests.get('https://discord.riverside.rocks/report.json.php?key=' + token + '&id=' + userid + '&details=' + reason)
    return resCheck.json()
