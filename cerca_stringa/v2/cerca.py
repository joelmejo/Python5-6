import os, mmap, base64
import PyPDF2
import textract
import requests
from PIL import Image as PImage

img_ext: list = [".png", ".jpeg", ".jpg"]

with open('pgkey.txt', 'r') as file:
    google_api_key = file.read()

base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-exp-0827:generateContent?key="
api_url = base_url + google_api_key

# IMISSIONE DEI PARAMETRI

sRoot = input("Inserisci la root directory: ")
sStringaDaCercare = input("Inserisci la stringa da cercare: ")
SOutDir = input("Inserici la directory di output: ")
iNumFileTrovati = 0

# METODI

def CercaStringaInFileName(sFile, sStringToSearch):
    sFilename1 = sFile.lower()
    sStringToSearch1 = sStringToSearch.lower()
    print("Cerco {0} in {1}".format(sStringToSearch1, sFilename1))
    iRet = sFilename1.find(sStringToSearch1)
    if(iRet>=0):
        print("Trovato!")
        return True
    return False

def CercaInTxt(sFile, sString):
    sString = sString.lower()
    try:
        with open(sFile) as f:
            s = mmap.mmap(f.fileno(), 0, access = mmap.ACCESS_READ)
            sAppo = s.readline()
            while len(sAppo) > 0:
                SAppo = SAppo.lower()
                if sAppo.find(sString.encode() != -1):
                    return True
                else:
                    sAppo = s.readline()
    except:
        return False

def CercaInFilePdf(sFile,sString):
    object = PyPDF2.PdfReader(sFile)
    numPages = len(object.pages)
    for i in range(0, numPages):
        pageObj = object.pages[i]
        text = pageObj.extract_text()
        text = text.lower()
        if(text.find(sString)!=-1):
           return True
    return False

def CercaInFileDocx(sFile,sString):
    text = textract.process(sFile)
    text = text.lower()
    if(text.find(sString.encode())!=-1):
        return True
    return False

def CercaInImg(sImage,sString):
    with open(sImage, 'rb') as f:
        img = f.read()
    jsonDataRequest = {
    "contents":[
        {
        "parts":[
            {"text": "Questa immagine è correlata alla parola" + sString + "? Rispondimi solamente con True o False."},
            {
            "inline_data": {
                "mime_type":"image/jpeg",
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
        risposta = jsonfile["candidates"][0]["content"]["parts"][0]["text"]
        print(risposta)
        if risposta == "True.":
            return True
        else:
            return False
    print(response.status_code)
    return "La richiesta a restituito un errore"


#NAVIGA NEL FILE SYSTEM

for root, dirs, files in os.walk(sRoot):
    sToPrint = "Dir corrente {0} contenent {1} subdir e {2} files".format(root,len(dirs),len(files))
    print(sToPrint)

    for filename in files:
        pathCompleto = os.path.join(root,filename)
        sOutFileName,sOutFileExt = os.path.splitext(filename)
        iRet = CercaStringaInFileName(filename, sStringaDaCercare)
        if iRet == True:
            print("Trovato file: ", filename)
            iNumFileTrovati += 1
        elif sOutFileExt.lower()==".pdf":
            if CercaInFilePdf(pathCompleto,sStringaDaCercare):
                iNumFileTrovati += 1
        elif sOutFileExt.lower()==".docx":
            if CercaInFileDocx(pathCompleto,sStringaDaCercare):
                iNumFileTrovati += 1
        elif any(sOutFileExt.lower() == ext for ext in img_ext):
            if CercaInImg(pathCompleto,sStringaDaCercare):
                iNumFileTrovati += 1
        elif sOutFileExt.lower()==".txt":
            if CercaInTxt(pathCompleto,sStringaDaCercare):
                iNumFileTrovati += 1
print(iNumFileTrovati)