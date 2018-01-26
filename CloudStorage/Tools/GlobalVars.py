import os

G_SESSION_DIR = ''

G_UPLOAD_PHOTO_FOLDER = ''
G_UPLOAD_PHOTO_FOLDER_REL = ''

G_UPLOAD_FILE_FLODER = ''
G_UPLOAD_FILE_FLODER_REL = ''

from Config import *

def _init_upload_dir(dir):
    rel_root_path = os.path.dirname(__file__) + '/../'
    if not os.path.isabs(dir):
        dir = rel_root_path + dir
        dir = os.path.normpath(dir)
    if not os.path.exists(dir):
        os.mkdir(dir)
        os.chmod(dir, 770)
    return os.path.abspath(dir), os.path.normpath(os.path.relpath(dir, rel_root_path))

G_SESSION_DIR, __G_SESSION_DIR_REL = _init_upload_dir(SESSION_DIR)
G_UPLOAD_FILE_FLODER, G_UPLOAD_FILE_FLODER_REL = _init_upload_dir(UPLOAD_FILE_FOLDER)
G_STATIC_FOLDER, G_STATIC_FOLDER_REL = _init_upload_dir('static')

G_USER_PORTRAIT = 'userPortrait'
G_ZONE_PIC = 'zonePic'
G_OBJECT_VIDEO = 'objectVideo'