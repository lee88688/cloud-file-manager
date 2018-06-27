import json
import os

file_types = ['directory', 'image', 'video', 'audio', 'document', 'zip', 'other']

# IMAGE_TYPE = {"jpg", "png", "gif", "webp", "tif", "bmp", "ico", "psd"}
# VIDEO_TYPE = {"mp4", "m4v", "mkv", "mov", "avi", "mpg", "mpg", "rmvb"}
# AUDIO_TYPE = {"mid", "mp3", "m4a", "ogg", "flac", "wav", "amr"}
# ZIP_TYPE = {"zip", "tar", "rar", "gz", "bz2", "7z", "xz"}
# DOCUMENT_TYPE = {"pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "epub"}

current_pwd = os.path.split(__file__)[0]
with open(current_pwd + os.sep + "filetype.json", 'r') as f:
    TYPE_LIST = json.loads(f.read())


def check_file_type(file_name):
    arr = file_name.split('.')
    if(len(arr) < 2):
        return "other"

    ext_name = arr[-1].lower()
    for typename in TYPE_LIST:
        if(ext_name in TYPE_LIST[typename]):
            return typename

    return "other"
