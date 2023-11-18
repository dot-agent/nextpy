import json
import numpy as np

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int64):
            return int(obj)
        elif isinstance(obj, tuple):
            return list(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(CustomJSONEncoder, self).default(obj)