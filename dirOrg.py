import os

def createFolderForPlots(name):
    #path = os.path.join('plots', name)
    path = os.path.join('plots', name)
    os.makedirs(path, exist_ok=True)  # Creează toate directoarele din cale dacă nu există deja
    print(f"Folder '{path}' created successfully")

def checkForFolder(name):
    #path = os.path.join('plots', name)
    path = "plots/" + name
    if os.path.isdir(path):
        print("Folder already exists")
        print(os.path.join('plots', name))
    else:
        createFolderForPlots(name)