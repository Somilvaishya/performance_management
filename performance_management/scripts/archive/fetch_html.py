import urllib.request
user_url = "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sX2E5ZGIzYjE0NTdlMzRiODU4ZGM1MDYyMzViZGY1NDJmEgsSBxDTnO2hxBUYAZIBIwoKcHJvamVjdF9pZBIVQhMxODEwNDUzODA0OTgzNTczOTUw&filename=&opi=96797242"
req = urllib.request.Request(user_url, headers={'User-Agent': 'Mozilla/5.0'})
content = urllib.request.urlopen(req).read().decode('utf-8')
print(content)
