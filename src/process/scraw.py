import time
import csv
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


def get_authors(url: str, dynasty: str) -> list:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    target_elements = soup.find_all(class_='inline1')
    data_list = []

    for element in target_elements:
        a_tag = element.find('a')
        if a_tag and 'href' in a_tag.attrs:
            url = urljoin(url, a_tag['href'])
        else:
            url = None
        author = element.get_text()
        data_list.append({'url': url, 'author': author, 'dynasty': dynasty})
    return data_list


if __name__ == '__main__':
    dynasties = ["WeiJin", "NanBei", "Tang", "Song", "Yuan", "Ming", "Qing"]
    base_url = input("give me the base url of THE poem site:")

    all_data = {}

    for dynasty in dynasties:
        target_url = f"{base_url}/PoemIndex.aspx?dynasty={dynasty}"
        data = get_authors(target_url, dynasty)
        all_data[dynasty] = data
        time.sleep(1)

    for dynasty, data_list in all_data.items():
        filename = f"./data/raw/{dynasty}_authors.csv"
        with open(filename, 'w', encoding='utf-8') as f:
            fields = ['url', 'author', 'dynasty']
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for data in data_list:
                writer.writerow(data)
