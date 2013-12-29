import urllib2
import urllib

def connect_minecraft(username, password):
    url = "http://login.minecraft.net/"
    data = {
        "user": username,
        "password": password,
        "version": 25
    }
    params = urllib.urlencode(data)
    req = urllib.urlopen(url, params)
    x = (req.read()).split(":")
    if x[0] == 'Bad login':
        return False
    else:
        return x[2]