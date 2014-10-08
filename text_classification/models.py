#module for Model class, and saved models configurations

import settings, pickler

# base structure of model class
class BaseModel(object):
    def __init__(self, model_id=None, language = "general", domain = "general", source = "general"):
        """
        base structure of model class
        :rtype : BaseModel(object)
        """

        # model basic properties
        self.__language = language
        self.__domain = domain
        self.__source = source
        if model_id: self.set_id(model_id)

    @property
    def path(self):
        return self.__language + "/" + self.__domain + "/" + self.__source + ""

    def get_id(self):
        return self.__language + "_" + self.__domain + "_" + self.__source + ""

    def set_id(self, model_id):
        model_path = model_id.split('_')
        if len(model_path) != 3: raise Exception("model_id must be string of 3 items seperated by _")
        self.language = model_path[0]
        self.domain = model_path[1]
        self.source = model_path[2]

    def get_property(self, property_name):
        return getattr(self, "__" + property_name)

    @property
    def language(self):
        return self.__language
    @language.setter
    def language(self, value):
        self.__language = value

    @property
    def domain(self):
        return self.__domain
    @domain.setter
    def domain(self, value):
        self.__domain = value

    @property
    def source(self):
        return self.__source
    @source.setter
    def source(self, value):
        self.__source = value

    @property
    def id(self):
        return self.get_id()


# class for holding train details such as amount of items in the train set and accuracy score
class TrainDetails(object):
    def __init__(self, items_amount=None, score=None):
        self.items_amount = items_amount
        self.score = score

# inherit from BaseModel
# adds pipeline, pipeline parameters and classes
class Model(BaseModel):
    def __init__(self, model_properties = None, classes_names = None, classifier_name = None, pipeline = None, pipeline_parameters = None, train_details = None):
        BaseModel.__init__(self, **model_properties)
        self.classes_names=classes_names
        self.pipeline = pipeline
        self.pipeline_parameters = pipeline_parameters
        self.classifier_name = classifier_name
        self.train_details = train_details or TrainDetails()

    # load specific model pickle file into this Model instance and into the dictionary: saved_models
    def load(self):
        print u"loading model: {0:s}".format(self.id)
        loaded_model = unpickle_model(self)
        if not loaded_model:
            raise Exception("can't find saved model with the given model properties: {0:s}".format(str({'language':language, 'domain': domain, 'source': source})))
        #assert isinstance(loaded_model, Model)
        self.pipeline = loaded_model.pipeline
        self.pipeline_parameters = loaded_model.pipeline_parameters
        self.classes_names = loaded_model.classes_names
        self.classifier_name = loaded_model.classifier_name
        self.train_details = loaded_model.train_details
        print("finished loading model!")

    def save(self):
        return pickle_model(self)

from sklearn.feature_selection import SelectPercentile, chi2
from normalizer import Normalizer

normalizer = Normalizer()

#language/domain/source:model
saved_models = {
    'en': {
        'bitcoin': {
            'twitter': Model(
                model_properties = { 'language': 'en', 'domain': 'bitcoin', 'source': 'twitter' },
                classifier_name = 'SGDClassifier',
                pipeline_parameters = {
                    "clf__alpha": 0.0001,
                    "clf__n_iter": 50,
                    "clf__penalty": 'l2',
                    "clf__loss": 'hinge',
                    "select__percentile": 100,
                    "select__score_func": chi2,
                    "tfidf__norm": u'l2',
                    "tfidf__smooth_idf": True,
                    "tfidf__sublinear_tf": True,
                    "tfidf__use_idf": True,
                    "vect__encoding": u'utf-8',
                    "vect__lowercase": False,
                    "vect__max_df":0.5,
                    "vect__min_df": 1,
                    "vect__ngram_range": (1, 2),
                    "vect__preprocessor": normalizer.normalize,
                    "vect__stop_words": None,
                    'vect__token_pattern' : u'(?u)\\b\\w\\w+\\b'
                },
                train_details=TrainDetails(score=0.680000000, items_amount=1075)
            ),
            'reddit': Model(
                model_properties = { 'language': 'en', 'domain': 'bitcoin', 'source': 'reddit' },
                classifier_name = 'MultinomialNB',
                pipeline_parameters = {
                    "clf__alpha": 0.01,
                    "select__percentile": 100,
                    'vect__token_pattern' : u'(?u)\\b\\w\\w+\\b',
                    "select__score_func": chi2,
                    "tfidf__norm": u'l2',
                    "tfidf__smooth_idf": True,
                    "tfidf__sublinear_tf": True,
                    "tfidf__use_idf": True,
                    "vect__encoding": u'utf-8',
                    "vect__lowercase": False,
                    "vect__max_df": 0.25,
                    "vect__min_df": 1,
                    "vect__ngram_range": (1, 3),
                    "vect__preprocessor": normalizer.normalize,
                    "vect__stop_words": None
                },
                train_details=TrainDetails(items_amount=100)
            )
        },
        'room':{
            'facebook': Model(
                model_properties = { 'language': 'en', 'domain': 'room', 'source': 'facebook' },
                classifier_name = 'Perceptron',
                pipeline_parameters = {
                    "clf__n_iter": 10,
                    "select__percentile": 16,
                    'vect__token_pattern' : u'(?u)\\b\\w\\w+\\b',# u'\\b\\w+\\b',
                    "select__score_func": chi2,
                    "tfidf__norm": u'l2',
                    "tfidf__smooth_idf": True,
                    "tfidf__sublinear_tf": True,
                    "tfidf__use_idf": True,
                    "vect__encoding": u'utf-8',
                    "vect__lowercase": False,
                    "vect__max_df": 0.75,
                    "vect__min_df": 1,
                    "vect__ngram_range": (1, 4),
                    "vect__preprocessor": normalizer.normalize,
                    "vect__stop_words": None
                }
            )
        },
    },
    'nl': {
        'room': {
            'facebook':  Model(
                model_properties = { 'language': 'nl', 'domain': 'room', 'source': 'facebook' },
                classifier_name = 'Perceptron',
                pipeline_parameters = {
                    "clf__n_iter": 25,
                    "select__percentile": 16,
                    "select__score_func": chi2,
                    "tfidf__norm": u'l2',
                    "tfidf__smooth_idf": True,
                    "tfidf__sublinear_tf": True,
                    "tfidf__use_idf": True,
                    "vect__encoding": u'utf-8',
                    "vect__lowercase": False,
                    "vect__max_df": 0.75,
                    "vect__min_df": 1,
                    "vect__ngram_range": (1, 4),
                    "vect__preprocessor": normalizer.normalize,
                    "vect__stop_words": None
                }
            )
        }
    }
}



def get_model(base_model, create_if_not_saved=False):
    model = None
    try:
        model = saved_models[base_model.language][base_model.domain][base_model.source]
    except KeyError:
        if create_if_not_saved:
            model = Model(model_properties={'language':base_model.language, 'domain': base_model.domain, 'source': base_model.source})
    return model


def pickle_model(model):
    path = settings.models_path
    print("pickling model to: " + path + model.id + ".pickle")
    pickler.dump(path + model.id + ".pickle", model)
    print("done")
    return True

def unpickle_model(model):
    path = settings.models_path
    print("loading model from: " + path + model.id + ".pickle")
    loaded_model = pickler.load(path + model.id + ".pickle")
    return loaded_model