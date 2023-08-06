
import os

def get_files_from_path(path):
    result=[]
    for root,dirs,files in os.walk(path):
        for file in files:
            result.append(os.path.join(root,file))
    return result

