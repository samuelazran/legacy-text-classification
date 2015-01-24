import logger, logging
import sys
import settings, data
from classifiers import classifiers
import models
import pipeline
import numpy as np

def print_vect(vect, feature_names):
    #print(type(vect))
    #print(dir(vect))
    #print(vect._get_dtype())
    #print(vect)
    for i in vect:
        print("array")
        ar=i.toarray()
        print(ar)
        for x,a in enumerate(ar):
            print(x)
            print('a')
            print(a)
            for y,b in enumerate(a):
                if b>0:
                    print(y)
                    print(feature_names[y])
                    print('b')
                    print(b)
        break

def train(model):
    pipeline_parameters=model.pipeline_parameters
    classifier_name=model.classifier_name
    model_id=model.id
    data_path="/".join(model_id.split("_"))
    print("data path: %s" % data_path)
    print ("training %s model with classifier %s and parameters:" % (model_id, classifier_name))
    print(pipeline_parameters)
    print("pipeline:")
    print(classifiers[classifier_name]["classifier"])
    
    classification_pipeline, params = pipeline.create(classifier=classifiers[classifier_name]["classifier"],parameters=pipeline_parameters)
    print(classification_pipeline)
    rawdata, classes, classes_names = data.load(data_path)
    
    
    feats = classification_pipeline.fit(rawdata, classes)
    feature_names = np.asarray(classification_pipeline.steps[0][1].get_feature_names())
    
    if False:
        print("count")
        count = classification_pipeline.steps[0][1].transform(rawdata)
        print_vect(count, feature_names)
        print("tfidf")
        tfidf = classification_pipeline.steps[1][1].transform(count)
        print_vect(tfidf, feature_names)
        selection = classification_pipeline.steps[2][1].transform(tfidf)
        print_vect(selection, feature_names)
    
    print("step 0")
    print(type(classification_pipeline.steps[0][1]))

    print("step 1")
    print(type(classification_pipeline.steps[1][1]))
    
    print("step 2")
    print(type(classification_pipeline.steps[2][1]))
    #print(dir(pipeline.steps[2][1]))
    
    #print("vocabulary_:")
    #print(pipeline.steps[0][1].vocabulary_)
	
    for i, class_name in enumerate(classes_names):
        print i, class_name
	
    if hasattr(classification_pipeline.steps[3][1], "coef_"):
		print("top 100 keywords per class:")
		for i, class_name in enumerate(classes_names):
			top = np.argsort(classification_pipeline.steps[3][1].coef_[i])[-100:]
			#print(top)
			print("%s:\n %s" % (class_name, ", ".join(feature_names[top])))
		print()

    model.train_details.items_amount = len(rawdata)
    model.pipeline = classification_pipeline
    model.classes_names = classes_names


if __name__ == "__main__":
    # parse commandline arguments
    from optparse import OptionParser
    op = OptionParser()
    op.add_option("--stdout", action="store", type=str, dest="stdout",
        help="stdout id for log file")
    op.add_option("--model_id", action="store", type=str, dest="model_id",
        help="model_id in the models config, also used for the name of the model file")
    op.add_option("--action", action="store", type=str, dest="action",
        help="whitch action to do: save, train, test")
    op.add_option("--predict", action="store", type=str, dest="predict",
        help="predict the class of this input")
    (opts, args) = op.parse_args()

    if opts.stdout:
        stdout = opts.stdout
        sys.stdout = logger.Logger(settings.stdout_path + stdout + '__stdout.log')
        #Display progress logs on stdout
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    if not opts.model_id:
        raise Exception("must specify --model_id")

    model_id = opts.model_id
    model = models.get_model(models.BaseModel(model_id=model_id), True)

    action = opts.action
    predict = opts.predict
    if action == "train" or action == "save":
        train(model)
    if action == "save":
        model.save()
    if predict:
        print("predict: %s" % predict)
        prediction = model.pipeline.predict([predict])
        print(prediction)
        print(model.pipeline.score([predict],prediction))
        if False and hasattr(model.pipeline,'predict_proba'):
            print("proba:")
            try:
                prediction = model.pipeline.predict_proba([predict])[0]
                print(prediction)
            except NotImplementedError as err:
                print (err.args)
