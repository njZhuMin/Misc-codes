import os
def GetFileList(FindPath):
    FileList = []
    FileNames = os.listdir(FindPath)
    if (len(FileNames) > 0):
        for fn in FileNames:
            FileList.append(fn)
    if (len(FileList)>0):
        FileList.sort()
    return FileList

if __name__ == '__main__':
    filename = GetFileList("/home/silverlining/test")
    prename = []
    for name in filename:
        prename.append(name.split(".")[0])
    arr = [str(i) for i in range(1, 100)]
    for n in arr:
        if n not in prename:
            print(n)
