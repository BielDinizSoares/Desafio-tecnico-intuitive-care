import requests
import os
import zipfile

def baixar_e_descompactar(urls, chunk_size=100000):
    os.makedirs("./data/", exist_ok=True)

    for url in urls:
        file_name = url.split('/')[-1]
        file_path = os.path.join("./data/", file_name)

        print(f"Baixando {file_name}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                f.write(chunk)

        if file_name.endswith(".zip"):
            print(f"Descompactando {file_name}")
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall("./data/")
