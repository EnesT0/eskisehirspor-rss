import requests
from bs4 import BeautifulSoup

base="https://www.eskisehirspor.org.tr"
page=requests.get(base+"/haberler").text
soup=BeautifulSoup(page,"html.parser")

items=""

links=set()
for a in soup.select("a[href*='/haber/']"):
    links.add(a["href"])

for href in list(links)[:10]:
    link=base+href
    h=requests.get(link).text
    s=BeautifulSoup(h,"html.parser")

    title=s.find("h1").text.strip() if s.find("h1") else link

    img=s.find("img")
    img=img["src"] if img else ""

    article=s.find("div")
    content=article.get_text(" ",strip=True)[:500] if article else ""

    items+=f"""
<item>
<title>{title}</title>
<link>{link}</link>
<description><![CDATA[
<img src="{img}"><br>{content}
]]></description>
</item>
"""

rss=f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>Eskisehirspor Haberler</title>
<link>{base}</link>
<description>Otomatik RSS</description>
{items}
</channel>
</rss>'''

open("feed.xml","w",encoding="utf-8").write(rss)
