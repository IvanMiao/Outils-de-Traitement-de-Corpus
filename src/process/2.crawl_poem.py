from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import os
import random


def crawl_poem(url: str) -> list:
    """
    Craels all poems from a given URL.

    Args:
        url: The URL to scrape.
    Returns:
        A list of dictionaries, where each of them representes a poem
        and contains the 'Title' and 'Content'.
        Returns an empty list if an error occurs.
    """
    poem_list = []

    headers = {
        'User-Agent': (
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/91.0.4472.124 Safari/537.36')
    }
    while True:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(3)

    soup = BeautifulSoup(response.text, 'html.parser')
    poem_divs = soup.find_all('div', class_='_poem')

    for poem_div in poem_divs:
        title_div = poem_div.find('div', class_='poemTitle showDetail')
        if title_div and title_div.a:
            title = title_div.a.text.strip()
            content_div = poem_div.find('div', class_='poemContent')
            if content_div:
                for comment in content_div.find_all(class_='inlineComment2'):
                    comment.decompose()
                content = content_div.text.strip()
                poem_list.append({'Title': title, 'Content': content})

    return poem_list


def process_author_csv(input_csv, output_csv):
    """
    Processes a CSV file containing dynasty/author URLs, crawls poems for each
    and save the poems to an output CSV file. It resumes crawling from the
    last processed author if the output file exists.

    Args:
        input_csv: path(str) to the input file containing url, author, dynasty.
        output_csv: path(str) to the output file where poems will be saved.
    """

    df = pd.read_csv(input_csv)
    df_output = pd.read_csv(output_csv)
    start = 0

    if len(df_output) >= 1 and 'Author' in df_output.columns:
        last_processed_author = df_output['Author'].iloc[-1]
        author_indices = df[df['author'] == last_processed_author].index
        start = author_indices[-1] + 1

    if start > 1000:
        return
    end = 1000
    for index, row in df.iloc[start:end].iterrows():
        url = row.get('url')
        author = row.get('author')
        dynasty = row.get('dynasty')
        poems = crawl_poem(url)
        for poem in poems:
            new_row = {
                'Dynasty': dynasty,
                'Author': author,
                'Title': poem['Title'],
                'Content': poem['Content']
            }
            new_df = pd.DataFrame([new_row])
            new_df.to_csv(
                output_csv,
                mode='a',
                header=False,
                index=False,
                encoding='utf-8'
                )

        print(f"{author} Crawled ! Total: {len(poems)} poems")
        time.sleep(random.uniform(0.5, 1.5))


def main():
    """
    Main function to orchestrate the craeling process for multiple dynasties.
    It iterates through a list of dynasties, defines input and output file
    paths, and calls the process_author_csv function for each dynasty.
    """
    dynasties = ["WeiJin", "NanBei", "Tang", "Song", "Yuan", "Ming", "Qing"]

    for dynasty in dynasties:
        input_file = f'./data/raw/{dynasty}_authors.csv'
        output_file = f'./data/raw/{dynasty}_poems.csv'
        if os.path.isfile(output_file):
            output_df = pd.read_csv(output_file)
        else:
            output_df = pd.DataFrame(
                columns=['Dynasty', 'Author', 'Title', 'Content']
                )
            output_df.to_csv(output_file, index=False, encoding='utf-8')
        process_author_csv(input_file, output_file)


if __name__ == '__main__':
    main()
