

from typing import Dict, List
import requests
import os
import fire


class DataSource:
    def __init__(self, url, credentials, friendly_name) -> None:
        self.url = url
        self.credentials = credentials
        self.friendly_name = friendly_name


destination_folder = None
sources: List[DataSource] = []

default_sources = [DataSource(url='https://dd.weather.gc.ca/vertical_profile/observation/csv/ObsTephi_00_CAWE.csv', friendly_name='EC Vertical Profile', credentials=None)]
sources += default_sources

def fetch_data():
    for source in sources:
        print('Fetching data from {}'.format(source.url))
        response = requests.get(source.url)
        success = None
        if response.status_code != 200:
            print('Encountered error fetching {} - error code {}'.format(source.url, response.status_code))
            success = False
        data = response.text
        if len(data) == 0:
            print('Could not retrieve any data from {}'.format(source.url))
            success = False
        else:
            print('Pulled data from {}. Status code {}'.format(source.url, response.status_code))
            success = True

        if success is True:
            with open(os.path.join(destination_folder, source.friendly_name+'.csv'), 'w+') as dest_file:
                print('Writing data to destination file {}'.format(dest_file))
                dest_file.write(data)

    print('Finished retrieving all datasets')

if __name__ == '__main__':
    fire.Fire()
