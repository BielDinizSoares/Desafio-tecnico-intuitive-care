import pandas as pd
import zipfile

files_to_unzip = ['data/1T2025.zip', 'data/2T2025.zip', 'data/3T2025.zip']

def descompactar_arquivos(): 
    for file in files_to_unzip:
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall('data')