import os
import requests

### SETTINGS ###

# pythonanywhere username
username = ''

# pythonanywhere token found in Account/API token
token = ''

# the path to the directory on pythonanywhere you want to upload to
path_to_upload_dir = '/home'

# list of paths to files to upload, subdirectories will be reflected in the pythonanywhere directory
files_to_upload = [
    'temp.txt',
    'temp2.txt'
    ]





### CODE ###

def updatePythonAnywhere():

    api_url = 'https://www.pythonanywhere.com/api/v0/user/{username}/files/path{path}'

    headers = {'Authorization': 'Token {token}'.format(token=token)}

    if not files_to_upload:
        print('No files to upload. Exiting.')
        return

    for file_path in files_to_upload:
        if not os.path.isfile(file_path):
            print(f'Skipping {file_path} (not a file)')
            continue
        
        relative_path = os.path.relpath(file_path, os.path.commonpath(files_to_upload))
        pythonanywhere_path = os.path.join(path_to_upload_dir, relative_path)

        print(f'Uploading {file_path} to {pythonanywhere_path}')

        try:
            with open(file_path, 'rb') as f:
                response = requests.post(
                    api_url.format(username=username, path=pythonanywhere_path),
                    headers=headers,
                    files={'content': f}
                )
                response.raise_for_status()
                print(f'Successfully uploaded {file_path} to {pythonanywhere_path}')
        except requests.exceptions.RequestException as e:
            print(f'Failed to upload {file_path} to {pythonanywhere_path}: {e}')
        except Exception as e:
            print(f'An unexpected error occurred while uploading {file_path}: {e}')



if __name__ == '__main__':
    try:
        updatePythonAnywhere()
    except Exception as e:
        print("updatePythonAnywhere.py failed")
        print(e)