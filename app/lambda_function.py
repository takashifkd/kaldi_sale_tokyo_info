"""
lambda_function.py
"""

import requests
from bs4 import BeautifulSoup
import datetime
from linebot import LineBotApi
from linebot.models import TextSendMessage
import json
import os


LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")

URL = os.getenv("URL")

TEN_CLOCK = os.getenv("TEN_CLOCK")

def lambda_handler(event, context):
  today = datetime.date.today()
  str_today = today.strftime('%Y-%m-%d')
  url = URL + str_today + TEN_CLOCK
  response = requests.get(url)
  response.encoding = response.apparent_encoding

  bs = BeautifulSoup(response.text, "html.parser")
  table = bs.find("table", {"class":"cz_sp_table cz_clear"}).tbody
  rows = table.find_all("tr")
  # print(rows[0])
  data = []
  for row in rows:
    data.append([v.text.replace("\n", " ").replace("\u3000", " ") for v in row.find_all("td")])
  # print(data)
  send_data = []
  for d in data:
    if "東京都" in d[1]:
      send_data.append(d)
  # print(send_data)
  # print(len(send_data))

  if len(send_data) > 0:
    sale_list = []
    for i in range(len(send_data)):
      content = []
      content.append(str(i+1) + ":" + send_data[i][0])
      content.append(send_data[i][1])
      content.append(send_data[i][3])
      sale_list.append(content)

    # str_today2 = today.strftime('%Y/%m/%d')
    title = "カルディセール情報(" + str_today + ")"
    content_text = []
    for i in range(len(sale_list)):
      content_text.append("\n".join(sale_list[i]))


    line_message = title + "\n" + "\n\n".join(content_text) + "\n\n" + url
    # print(line_message)
    line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
    line_bot_api.broadcast(TextSendMessage(text=line_message))

if __name__ == "__main__":
  print(lambda_handler(event=None, context=None))
