import requests
import xml.etree.ElementTree as ET
import pandas as pd
import os
import json
import html
import re
from bs4 import BeautifulSoup


def download_data_file(dir_path : str):
    file_name = "player_stats.html"
    full_file_path = os.path.join(dir_path, file_name)

    url = 'https://www.pro-football-reference.com/years/2025/fantasy.htm#fantasy'
    response = requests.get(url)

    if response.status_code == 200:
        with open(full_file_path, "w") as file:
            file.write(response.text)
        print("XML file downloaded successfully!")
    else:
        print(f"Error downloading file: {response.status_code}")


def html_to_csv(path_to_html):
    path = path_to_html
    
    data = []

    list_header = []
    soup = BeautifulSoup(open(path),'html.parser')
    rows = soup.find_all("table")[0].find_all("tr")
    second_row = rows[1]
    for items in second_row:
        try:
            list_header.append(items.get('aria-label'))
        except:
            continue

    HTML_data = soup.find_all("tbody")[0].find_all("tr")[:]
    for element in HTML_data:
        sub_data = []
        for sub_element in element:
            try:
                sub_data.append(sub_element.get_text())
            except:
                continue
        if (len(sub_data) == len(list_header)):
            data.append(sub_data)



    dataFrame = pd.DataFrame(data = data, columns = list_header)
    dataFrame.to_csv('data/player_stats.csv')

download_data_file("data/")
html_to_csv("data/player_stats.html")