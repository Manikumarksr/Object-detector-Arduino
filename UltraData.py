
import urllib.request
import re
url = "http://192.168.4.22/"
while True:
    url_response = urllib.request.urlopen(url)
    url_contents = url_response.read().decode()
    data=re.findall(r'\d+',url_contents)
    print(data[0])
