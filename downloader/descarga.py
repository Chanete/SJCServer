import requests
import csv
cookie1="SIDCC=AJi4QfGiCL8y7ejQuczzq8UXMtJWTBroPZv-VrcguBAZPuzfuJksPh4vcBclhbHcp-ZscaP9kQ; expires=Sat, 21-May-2022 12:20:17 GMT; path=/; domain=.youtube.com; priority=high"
cookie2="__Secure-3PSIDCC=AJi4QfGErgXGEi3dLfRpi8wUzMCfY5zIkFYL0lonk9ZP-G5FVxojcRB1DgMMx7Le_0Q1mxXgW38; expires=Sat, 21-May-2022 12:20:17 GMT; path=/; domain=.youtube.com; Secure; HttpOnly; priority=high; SameSite=none"


headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cookie": cookie2 }
    


key = "QUFFLUhqbDZCR1JKbi1kV2dyZks1SWpHSW5qSVVqU0FlZ3xBQ3Jtc0tsSTlhN0J2ZnNEa0RLUFl6a19mZ0lWeU5sWHRrb0xBdjhXcUNtV2o4eFFzSnUxMnBGYjAtWnAwcG1ZS1RUQ0pIcVhvUEZpbTVna1JIYTh1Wnc3SkR6aHdZanhkcEl3SGJndjREblZKVkNoM0JoeVc1cw=="

video_id = "5f-FFlExzPA"
url = "https://www.youtube.com/download_my_video?v=%s&t=%s" % (video_id, key)
with requests.get(url, headers=headers, stream=True) as r:          
    r.raise_for_status()
    with open(video_id+".mp4", "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                print(chunk)