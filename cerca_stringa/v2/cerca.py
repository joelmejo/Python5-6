import base64
import os
from docx import Document
import PyPDF2
import requests
import shutil
import re

img_ext: list = [".png", ".jpeg", ".jpg"]

with open('pgkey.txt', 'r') as file:
    google_api_key = file.read()

base_url: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-exp-0827:generateContent?key="
api_url: str = base_url + google_api_key

# IMISSIONE DEI PARAMETRI

sRoot: str = input("Inserisci la root directory: ")
sStringaDaCercare: str = input("Inserisci la stringa da cercare: ")
SOutDir: str = input("Inserisci la directory di output: ")
root_choice: str = input("Inserire nel nome del file il path assoluto(a) o relativo(r): ")
iNumFileTrovati: int = 0


# METODI

def CercaStringaInFileName(sFile: str, sStringToSearch: str) -> bool:
    sFilename1: str = sFile.lower()
    sStringToSearch1: str = sStringToSearch.lower()
    print(f"Cerco {sStringToSearch1} in {sFilename1}")
    if sStringToSearch1 in sFilename1:
        return True
    return False


def CercaInTxt(sFile: str, sString: str) -> bool:
    """
        Ritorna un valore binario indicando se la stringa è presente all'interno di un file txt.

            Parameters:
                sFile (str): File dove cercare la stringa
                sString (str): Stringa da cercare

            Returns:
                bool: True se la stringa è trovata nel file, False altrimenti.

    """
    sString: str = sString.lower()
    try:
        with open(sFile, encoding="utf-8") as f:
            lines: list[str] = f.readlines()
        for line in lines:
            if sString in line:
                return True
        return False
    except Exception as e:
        print(e)

def CercaInFilePdf(sFile: str, sString: str) -> bool:
    object = PyPDF2.PdfReader(sFile)
    numPages = len(object.pages)
    for i in range(0, numPages):
        pageObj = object.pages[i]
        text = pageObj.extract_text()
        text = text.lower()
        if (text.find(sString) != -1):
            return True
    return False

def CercaInFileDocx(sFile: str, sString: str) -> bool:
    doc = Document(sFile)
    search_string = sString.lower()
    for para in doc.paragraphs:
        para_text = para.text.lower()
        if search_string in para_text:
            return True
    return False

def CercaInImg(sImage, sString) -> bool | None:
    _, ext = os.path.splitext(sImage)
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg', 
        '.png': 'image/png'
    }
    mime_type = mime_types[ext.lower()]
    with open(sImage, 'rb') as f:
        img = f.read()
        
    jsonDataRequest: dict = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Questa immagine è correlata alla parola " + sString + "? Rispondimi solamente con True o False"},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": base64.b64encode(img).decode('utf-8')
                        }
                    }
                ]
            }
        ]
    }
    response = requests.post(api_url, json=jsonDataRequest)
    if response.status_code == 200:
        jsonfile = response.json()
        risposta: str = jsonfile["candidates"][0]["content"]["parts"][0]["text"]
        risposta = risposta.strip('.')
        if risposta == "True":
            return True
        else:
            return False
    print(response.status_code)
    print("La richiesta ha restituito un errore")


# NAVIGA NEL FILE SYSTEM

for root, dirs, files in os.walk(sRoot):
    if root == SOutDir:
        continue
    sToPrint = f"Dir corrente {root} contenente {len(dirs)} subdir e {len(files)} files"
    print(sToPrint)

    for filename in files:
        stringfound: bool = False
        pathCompleto = os.path.join(root, filename)
        sOutFileName, sOutFileExt = os.path.splitext(filename)
        if CercaStringaInFileName(filename, sStringaDaCercare):
            stringfound = True
        else:
            file_check_functions = {".docx": CercaInFileDocx,".pdf": CercaInFilePdf, ".png": CercaInImg, ".jpg": CercaInImg, ".jpeg": CercaInImg}
            if sOutFileExt in file_check_functions:
                if file_check_functions[sOutFileExt](pathCompleto, sStringaDaCercare):
                    stringfound = True
        if stringfound:
            print("Trovato file: ", filename)
            os.makedirs(SOutDir, exist_ok=True)
            if root_choice.lower() == 'a':
                absolute_root = os.path.abspath(root)
                sanitized_root = re.sub(r'[\\/]', '_', absolute_root)
            else:
                relative_root = os.path.relpath(root, sRoot)
                sanitized_root = re.sub(r'[\\/]', '_', relative_root)
            new_file_name: str = f"{sanitized_root}_{filename}"
            current_dir = os.getcwd()
            dest_path = os.path.join(current_dir, SOutDir, new_file_name)
            shutil.copy(pathCompleto, dest_path)
