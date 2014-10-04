from optparse import OptionParser
import sys, os
import logging
import data
from classifiers import classifiers
import pipeline
import gridsearch
import logger
import models, settings

if __name__ == "__main__":
    # parse commandline arguments
    op = OptionParser()
    op.add_option("--fullgrid",
                      action="store_true", dest="fullgrid",
                      help="use the full grid parameters")
    op.add_option("--stdout",
                      action="store", type=str, dest="stdout",
                      help="stdout id for log file")
    op.add_option("--start",
                      action="store", type=int, dest="start",
                      help="Select the start range of the index of the classifiers list")
    op.add_option("--end",
                      action="store", type=int, dest="end",
                      help="Select the end range of the index of the classifiers list")
    op.add_option("--model_id", action="store", type=str, dest="model_id",
        help="model_id in the models config, also used for the name of the model file")
    (opts, args) = op.parse_args()
    start, end = -1,-1
    if opts.start is not None and opts.end is not None:
        start, end = opts.start,opts.end
        print("start: %d, end: %d" % (start, end))
    if opts.stdout:
        stdout = opts.stdout
        stdout_filename = stdout + '__stdout.log'
        sys.stdout = logger.Logger(settings.stdout_path + stdout_filename)
    #Display progress logs on stdout
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    
    fullgrid=opts.fullgrid
    
    model_id = opts.model_id
    assert isinstance(model_id, str), "must specify model_id"
    model = models.Model({'model_id': model_id})

    classifier_name = None
    if not fullgrid: classifier_name=model.classifier_name

    rawdata, classes, classes_names = data.load(model.path)

    classifier_grid_parameters={}
    if fullgrid:
        print("fullgrid")
        pipeline_parameters=None
    else:
        pipeline_parameters=model.pipeline_parameters
    
    index = -1
    for name, obj in classifiers.iteritems():
        index +=1
        if (not fullgrid and classifier_name==name) or (fullgrid and index >= start and index <= end):
            print("")
            print("classifier %s:" % name)
            print("")
            classifier_grid_parameters={}
            if fullgrid: 
                classifier_grid_parameters=obj['grid_parameters'].copy()
                print("classifier_grid_parameters",classifier_grid_parameters)
            pipeline, parameters = pipeline.create(classifier=obj["classifier"],parameters=pipeline_parameters,classifier_grid_parameters=classifier_grid_parameters)
            print("parameters:")
            print(parameters)
            print("")
            gridsearch.start(pipeline, parameters, rawdata[:550], classes[:550])