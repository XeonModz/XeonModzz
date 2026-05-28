# Version: 1.0 Beta
# ©️ 2025 XeonModz ALL RIGHTS RESERVED

import re, requests


# filename sanitize
def sanitize_filename(filename):

    return re.sub(
        r'[^a-zA-Z0-9_.-]',
        '_',
        filename
    )


# download file
def download_file(download_link, file_path):

    with requests.get(
        download_link,
        stream=True
    ) as file_response:

        if file_response.status_code == 200:

            with open(file_path, 'wb') as f:

                for chunk in file_response.iter_content(
                    chunk_size=8192
                ):

                    f.write(chunk)

            return True

    return False