import urllib2
import urllib

def connect_minecraft(username, password):
    url = "https://www.minerap.com/user/login/"
    data = {
        "username": username,
        "password": password,
    }
    params = urllib.urlencode(data)
    req = urllib2.Request(url, params)
    try:
        response = urllib2.urlopen(req)
        code = response.code
    except Exception, e:
        code = e.code
    if code == 200:
        return False
    else:
        return username
