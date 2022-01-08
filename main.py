

from typing import Dict, List
import requests
import html5lib
from bs4 import BeautifulSoup
import os
import sys
from pathlib import Path
import fire

class DataSource:
    def __init__(self, url, credentials, friendly_name) -> None:
        self.url = url
        self.credentials = credentials
        self.friendly_name = friendly_name


sources: List[DataSource] = []

default_sources = [DataSource(url='https://dd.weather.gc.ca/vertical_profile/observation/csv/', friendly_name='EC Vertical Profile', credentials=None)]
sources += default_sources

def fetch_data(folder):
    for source in sources:
        print('Fetching data from {}'.format(source.url))
        response = requests.get(source.url)
        soup = BeautifulSoup(response.content, 'html5lib')
        html_list = soup.find_all('a')
        source_files = []
        for row in html_list:
            file_url = str(row['href'])
            if file_url.endswith('.csv'):
                source_files.append(file_url)
        for filename in source_files:
            url = os.path.join(source.url, filename)
            success = None
            download_response = requests.get(url)
            if download_response.status_code != 200:
                print('Encountered error fetching {} - error code {}'.format(url, download_response.status_code))
                success = False
            data = download_response.text
            if len(data) == 0:
                print('Could not retrieve any data from {}'.format(url))
                success = False
            else:
                print('Pulled data from {}. Status code {}'.format(url, download_response.status_code))
                success = True

            if success is True:
                Path(os.path.join(folder, source.friendly_name)).mkdir(parents=True, exist_ok=True)
                dest_filepath = os.path.join(folder, source.friendly_name, filename)
                print('Saving to {}'.format(dest_filepath))
                with open(dest_filepath, 'w+') as dest_file:
                    print('Writing data to destination file {}'.format(dest_file))
                    dest_file.write(data)

    print('Finished retrieving all datasets')

if __name__ == '__main__':
    fire.Fire()
