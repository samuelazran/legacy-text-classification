# predictor module
# uses saved models to predict the class of a given input

from utils import Bunch
import language_detector
import models

models_supported_languages = {}

# specify models to use for predictions (classifications) tasks
def use_model(language, domain, source):
    models_supported_languages[language] = True
    model = models.get_model(models.BaseModel(language=language,domain=domain, source=source))
    if not model.pipeline: model.load()

# detect individual text language
# returns object with two lists: supported and unsupported languages detected in the input
def detect_language(text):
    lines_languages = language_detector.detect(text)
    supported_languages, unsupported_languages = [], []
    for line_language in lines_languages:
        if line_language[0] in models_supported_languages:
            supported_languages.append(line_language)
        else:
            unsupported_languages.append(line_language)
    return Bunch(supported=supported_languages, unsupported=unsupported_languages)

# detect language for list of texts
def detect_languages(texts):
    languages = []
    for text in texts:
        languages.append(detect_language(text))
    return languages

# simple class that holds particular prediction data
class Prediction(object):
    def __init__(self, class_index, classes_names, probabilities=None):
        self._original_class_string = classes_names[class_index] # original class string as defined in the model
        self._class_name = None # string represent the name of the predicted class, e.g: "positive"
        self._class_value = None # numeric value represent the predicted class, e.g: 1
        self._class_index = class_index # index of the predicted class in the classes_names list
        self._probabilities = None # list with predicted probabilities per class in case the data available, if not holds None
        self._classes_names = classes_names # reference to list of classes names
        self.set_class_name_and_value()
    def set_class_name_and_value(self):
        original_class_parts = self._original_class_string.split("_")
        if len(original_class_parts) == 1:
            pass
        elif len(original_class_parts) == 2:
            try:
                self._class_value = int(original_class_parts[0])
            except ValueError:
                try:
                    self._class_value = float(original_class_parts[0])
                except ValueError:
                    self._class_value = str(original_class_parts[0])
            self._class_name = original_class_parts[1]
    @property
    def name(self):
        return self._class_name or self._original_class_string
    @property
    def value(self):
        return self._class_value
    @property
    def index(self):
        return self._class_index
    @property
    def names(self):
        return self._classes_names
    @property
    def probabilities(self):
        return  self._probabilities



#predict classes of input with model for this languages, domain and source
def predict_for_specific_language(language, domain, source, input):
    model = models.saved_models[language][domain][source]
    predictions_objects = []
    predictions_probabilities = None
    predictions_indexes=model.pipeline.predict(input)
    if hasattr(model.pipeline,'predict_proba'):
        try:
            predictions_probabilities = model.pipeline.predict_proba(input)
        except NotImplementedError as err:
            print (err.args)
    for i, prediction_index in enumerate(predictions_indexes):
        prediction_probabilities = None
        if predictions_probabilities: prediction_probabilities = predictions_probabilities[i]
        prediction_object = Prediction(prediction_index,model.classes_names,prediction_probabilities)
        predictions_objects.append(prediction_object)
    return predictions_objects

# detect languages if language is not specified
# predict the class of this input with model for the languages, domain and source
# params example: language='en', domain='bitcoin', source='twitter', input = ['tweet A', 'tweet B'...]
def predict(language=None, domain=None, source=None, input=None):
    if language:
        return predict_for_specific_language(language, domain, source, input)
    predictions=list(range(0,len(input)))
    languages=detect_languages(input)
    print(languages)
    input_by_lang = {}
    for i,text in enumerate(input):
        best_lang=languages[i].supported[0][0]
        if not best_lang in input_by_lang: input_by_lang[best_lang]=[[],[]]
        input_by_lang[best_lang][0].append(i)#original place in list
        input_by_lang[best_lang][1].append(text)
    for languages in input_by_lang:
        input_by_lang_predictions=predict_for_specific_language(languages, domain, source, input_by_lang[languages][1])
        for i,prediction in enumerate(input_by_lang_predictions):
            predictions[input_by_lang[languages][0][i]]=prediction
    return languages, predictions

if __name__ == "__main__":
    from optparse import OptionParser
    # parse commandline arguments
    op = OptionParser()
    op.add_option("--language", action="store", type=str, dest="language",
        help="language of the input")
    op.add_option("--domain", action="store", type=str, dest="domain",
        help="domain of the input")
    op.add_option("--source", action="store", type=str, dest="source",
        help="source of the input")
    op.add_option("--input", action="store", type=str, dest="input",
        help="predict the class of this input")
    (opts, args) = op.parse_args()

    if not opts.domain or not opts.source or not opts.input:
        raise Exception("must specify --domain, --source and --input")
    print("loading model...")
    use_model(opts.language,opts.domain,opts.source)
    print("predict for language:  {0:s}, domain: {1:s}, source: {2:s}".format(opts.language,opts.domain,opts.source))
    print ("input: {0:s}".format(opts.input))
    print ("class:")
    prediction = predict(opts.language, opts.domain, opts.source, [opts.input])[0]
    print("class name: {0:s}, class value: {1:s}, class index: {2:s}, classes names: {3:s}, probabilities: {4:s}".format(prediction.name, str(prediction.value), str(prediction.index), str(prediction.names), str(prediction.probabilities)))