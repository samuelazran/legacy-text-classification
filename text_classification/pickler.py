__author__ = 'Samuel'
#special module to handle dumping pickle files to prevent module names conflicts
import pickle, dill
import sys,text_classification

def dump(path, obj):
    f = open(path,'wb')
    pickle.dump(obj, f)
    f.close()
    return True

def load(path):
    print(sys.modules)
    f = open(path)
    #dirty workaround to make the necessary modules for the Model instance available
    sys.modules["models"]=text_classification.models
    sys.modules["normalizer"]=text_classification.normalizer
    obj = pickle.load(f)
    sys.modules.pop("models", None)
    sys.modules.pop("normalizer", None)
    f.close()
    return obj