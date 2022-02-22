import requests
from requests.structures import CaseInsensitiveDict
import os
from os import listdir
from fpdf import FPDF
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--link', help='Give JSON File Link')
args = parser.parse_args()
link = args.link

import urllib.request, json
with urllib.request.urlopen(link) as url:
  data = json.loads(url.read().decode())

ck = data['ck']
fileName = data['file']
ds = data['ds']
pg = data['page']

headers = CaseInsensitiveDict()
headers = {
  'Host': 'drive.google.com',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'x-requested-with': 'idm.internet.download.manager',
  'sec-fetch-site': 'none',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-user': '?1',
  'sec-fetch-dest': 'document',
  'accept-encoding': 'gzip, deflate',
  'accept-language': 'en,en-US;q=0.9',
  'cookie': ck
}

for x in range(int(pg)):
  response = requests.get("https://drive.google.com/viewer2/prod-01/img?ck=drive&ds="+str(ds)+"&authuser=1&page="+str(x)+"&skiphighlight=true&w=1600&webp=true", headers = headers)
  file = open('d/'+str(x)+".png", "wb")
  file.write(response.content)
  file.close()

###Starts Pdf Making Code####

path = "d/"
"""
imagelist = listdir(path)
#imagelist = [int(x) for x in imagelist]
imagelist=sorted(imagelist, key=lambda fname: int(fname.split('.')[0]))
"""
def sortKeyFunc(s):
  return int(os.path.basename(s)[:-4])

pdf = FPDF("P", "mm", "A4")
imageList = listdir(path)
imageList.sort(key = sortKeyFunc)
x = 0
y = 0
w = 210
h = 297

for image in imageList:
  pdf.add_page()
  pdf.image(path+image, x, y, w, h)

pdf.output(fileName, "F")