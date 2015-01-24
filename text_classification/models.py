#module for Model class, and saved models configurations

import settings, pickler


# base structure of model class
class BaseModel(object):
    def __init__(self, model_id=None, language = "general", domain = "general", source = "general", type = "general"):
        """
        base structure of model class
        :rtype : BaseModel(object)
        """

        # model basic properties
        self.__language = language      # e.g en or nl...
        self.__domain = domain          # e.g bitcoin or residence or room...
        self.__source = source          # e.g facebook or twitter...
        self.__type = type              # e.g sentiment or pos or ner...
        if model_id: self.set_id(model_id)

    @property
    def path(self):
        return self.__language + "/" + self.__domain + "/" + self.__source + "/" + self.__type + ""

    def get_id(self):
        return self.__language + "_" + self.__domain + "_" + self.__source + "_" + self.__type + ""

    def set_id(self, model_id):
        model_path = model_id.split('_')
        if len(model_path) != 4: raise Exception("model_id must be string of 4 items separated by _")
        self.language = model_path[0]
        self.domain = model_path[1]
        self.source = model_path[2]
        self.type = model_path[3]

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
    def type(self):
        return self.__type
    @type.setter
    def type(self, value):
        self.__type = value

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


def get_model(base_model, create_if_not_saved=False):
    from saved_models import saved_models
    model = None
    try:
        model = saved_models[base_model.language][base_model.domain][base_model.source][base_model.type]
    except KeyError:
        if create_if_not_saved:
            model = Model(model_properties={'language':base_model.language, 'domain': base_model.domain, 'source': base_model.source, 'type': base_model.type})
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