from sklearn.grid_search import GridSearchCV

def start(classification_pipeline, parameters, rawdata, classes):
    grid_search = GridSearchCV(classification_pipeline, parameters, n_jobs=1, verbose=1)
    grid_search.fit(rawdata, classes)

    print()
    print("Best score: %0.9f" % grid_search.best_score_)
    print("Best parameters set:")
    best_parameters = grid_search.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))