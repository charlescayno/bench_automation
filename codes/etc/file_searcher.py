import os
import shutil
from powi.equipment import path_maker
def file_searcher(phrase, search_path):

    filelist = os.listdir(search_path)

    match_ctr = 0
    for file in filelist:
        filename = os.path.splitext(file)

        if phrase in filename[0]:
            print(file)
            match_ctr += 1
            src_path = search_path + f"/{file}"
            dst_path = search_path + f"/trades/{file}"
            path_maker(dst_path)
            shutil.move(src_path, dst_path)


    print(match_ctr)

search_path = "C:/Users/ccayno/Downloads"
phrase = "USDT"


file_searcher(phrase, search_path)