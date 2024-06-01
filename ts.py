import requests

response = requests.get("https://web.facebook.com/ads/archive/render_ad/?id=385550857686219&access_token=EAAUO7xsa6KsBOwJ4PFfmZAkF8KBtxzsL5MYKYr5Ejihw6LwPVvYT74gXEY8ZAAqlS64DlRRoLmOYTw88RxwJkPpSGZBlhNby5kWlsd80KpfUbbXEj3eMje1wiNqXA1I1j7CU2emxjNGZAnmh7rQoZBupT1v4MktMEnKPGHxtnFEWQSzXTZCCx4aRNWwMvSoqmP&_rdc=1&_rdr")
tokens = str(response.content).split('"')
index = tokens.index("video_sd_url")
overslashed = tokens[index+2]
slashedIterable = overslashed.split("\\")
slashed = "".join(slashedIterable)
print(slashed)