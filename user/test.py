import requests
url = "http://127.0.0.1:8000/api/user/avatar/upload"
data = None
files = {  "field1" : ("filename1", open("25.jpg", "rb"))}
r = requests.post(url, data, files=files)