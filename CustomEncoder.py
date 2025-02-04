from Playlist import Playlist

import json

"""
This file is a custom encoder to allow classes to be presented in a json
"""
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Playlist):
            return obj.__dict__()
        return super().default(obj)