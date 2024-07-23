import os

def createFolderForPlots(name):
    path = os.path.join('plots', name)
    os.mkdir(path)
    print("Folder created successfully")

def checkForFolder(name):
    path = os.path.join('plots', name)
    if os.path.isdir(path):
        print("Folder already exists")
        print(os.path.join('plots', name))
    else:
        createFolderForPlots(name)