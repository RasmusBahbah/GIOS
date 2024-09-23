import os
from pyDataverse.api import NativeApi, DataAccessApi
import glob
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download files from GEUS Dataverse')
    parser.add_argument('--folder', type=str, help='Folder to download to', default=os.getcwd())
    parser.add_argument('--api_key', type=str, help='Your GEUS Dataverse API KEY', required=True)
    parser.add_argument('--dataverse_server', type=str, help='Dataverse server URL', default='https://dataverse.geus.dk')
    parser.add_argument('--persistentId', type=str, help='Persistent ID of the dataset', required=True)
    args = parser.parse_args()

    folder_store = args.folder
    api_key = args.api_key
    dataverse_server = args.dataverse_server
    persistentId = args.persistentId

    if not os.path.exists(folder_store):
        os.makedirs(folder_store)

    api = NativeApi(dataverse_server, api_key)
    data_api = DataAccessApi(dataverse_server, api_key)
    dataset = api.get_dataset(persistentId)

    files_local = glob.glob(folder_store + os.sep + '*.nc')
    files_local = [f.split(os.sep)[-1] for f in files_local]

    files_dataverse = dataset.json()['data']['latestVersion']['files']

    files_down = [f['label'] for f in files_dataverse if f['label'] not in files_local]
    files_down_id = [f["dataFile"]["id"] for f in files_dataverse if f['label'] not in files_local]

    for f_name, f_id in zip(files_down, files_down_id):
        print(f'downloading {f_name}')
        response = data_api.get_datafile(f_id)

        f_name_local = folder_store + os.sep + f_name
        with open(f_name_local, "wb") as f:
            f.write(response.content)