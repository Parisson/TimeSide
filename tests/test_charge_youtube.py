import youtube_dl

ydl_opts = {
    'quiet': True,
    'skip_download': True,
    'forcetitle': True,
}

# Extracts information using the "ytsearch:string" method
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    infoSearched = ydl.extract_info("ytsearch100:the Beatles")

for i in infoSearched['entries']:
    print(i['webpage_url'])