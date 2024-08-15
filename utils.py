import os

from kivy.lang import Builder
import constants


def load_kv_path(path):
    """
    Loads a kv file from a path
    """
    kv_path = os.path.join(constants.PROJECT_DIR, path)
    if kv_path in Builder.files:
        Builder.unload_file(kv_path)

    if kv_path not in Builder.files:
        Builder.load_file(kv_path)