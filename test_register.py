'''
script to upload test to https://tools.ostrails.eu/fdp-index

'''

import os
import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# github_api_url = "https://api.github.com/repos/oeg-upm/fair_ontologies/contents/doc/test"
github_api_url = config.get('Paths', 'path_github_api_url').strip('"')
urlRegister = config.get('Paths', 'path_url_register').strip('"')

print(f"URL: {urlRegister}")


def fetch_github_files(base_url):
    '''
        iterate repo github with test ttl
    '''
    response = requests.get(base_url, timeout=60)

    if response.status_code == 200:

        items = response.json()
        for item in items:

            if item["type"] == "dir":
                print(f"Folder: {item['name']}")
                fetch_github_files(item["url"])
            elif item["type"] == "file" and item["name"].endswith(".ttl"):
                clientUrl = {"clientUrl": item['download_url']}
                headers = {"Content-Type": "application/json"}

                try:
                    response = requests.post(
                        urlRegister, json=clientUrl, headers=headers, timeout=60)
                    # Imprimir detalles
                    print(f"File found: {clientUrl}")
                    print(f"Request URL: {response.url}")
                    print(f"Request Headers: {response.request.headers}")
                    print(f"Response Status Code: {response.status_code}")
                    # print(f"Response Body: {response.text}\n")

                except requests.exceptions.RequestException as e:
                    print(
                        f"Error processing the file {item['download_url']}: {e}")
    else:
        print(f"Error get content: {response.status_code}")


fetch_github_files(github_api_url)
print("----- END of process ------")
