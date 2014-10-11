__author__ = 'Samuel'
#special module to handle dumping pickle files to prevent module names conflicts
import pickle, dill
import sys
import models,normalizer


def dump(path, obj):
    f = open(path,'wb')
    pickle.dump(obj, f)
    f.close()
    return True

def load(path):
    f = open(path)

    #dirty workaround to make the necessary modules for the Model instance available

    original_models_ref = None
    try:
        original_models_ref = sys.modules["models"]
    except KeyError:
        pass

    original_normalizer_ref = None
    try:
        original_normalizer_ref = sys.modules["normalizer"]
    except KeyError:
        pass

    sys.modules["models"]=models
    sys.modules["normalizer"]=normalizer
    obj = pickle.load(f)
    sys.modules["models"]=original_models_ref
    sys.modules["normalizer"]=original_normalizer_ref
    #sys.modules.pop("models", None)
    #sys.modules.pop("normalizer", None)

    f.close()
    return obj