import http.cookiejar ,urllib.request
filename="cookie.txt"
cookie=http.cookiejar.MozillaCookieJar(filename)
handler=urllib.request.HTTPCookieProcessor(cookie)
opener=urllib.request.build_opener(handler)
response=opener.open("http://www.baidu.com")
for item in cookie:
    print(item.name+"m"+item.value)

cookie.save(ignore_discard=True,ignore_expires=True)