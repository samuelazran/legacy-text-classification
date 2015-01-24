from sklearn.pipeline import Pipeline

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectPercentile, chi2

from normalizer import Normalizer


normalizer = Normalizer()



def create(classifier, parameters=None, classifier_grid_parameters=None):
    """Create pipeline with specific parameters
    
    if parameters not specified than grid search parameters will be used
    
    Parameters
    ----------
        classifier: classifier algorithm (* required)
        parameters: (* required for specific module creation)
        classifier_grid_parameters: (* required for grid search for the best parameters)
        
            example:
                classifier=SVC, 
                grid_parameters={'kernel':('linear', 'rbf'), 'C':[1, 10]},
                parameters={'kernel':'linear', 'C':1}
        
    Returns
    -------
    pipeline: sklearn.pipeline.Pipeline object
    parameters: grid or specific parameters dict
    """
    grid_mode = False
    if classifier_grid_parameters is not None:
        grid_mode=True
        if parameters is None:
            #parameters = best_grid_parameters.copy()
            #parameters = full_grid_parameters.copy()
			parameters = featureset_grid_parameters.copy()
        else:
            parameters=parameters_to_grid(parameters)
        for key, value in classifier_grid_parameters.iteritems():
            parameters['clf__' + key]=value
    
    classification_pipeline = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('select', SelectPercentile()),
        ('clf', classifier()),
    ])
    
    if not grid_mode:
        classification_pipeline.set_params(**parameters)
    return classification_pipeline,parameters

#globals
featureset_grid_parameters = {
    'vect__lowercase': [False],
    'vect__preprocessor': [None],
    #'vect__strip_accents' : [u'ascii', u'unicode', None],
    'vect__token_pattern' : [u'(?u)\\b\\w\\w+\\b'],
    'vect__encoding' : [u'utf-8'],
    'vect__min_df': [1],
    'vect__max_df': [0.25,0.5,0.75,1.0],
    #'vect__analyzer' : ['char'],
    'vect__ngram_range': [(1, 1)],
    'vect__stop_words': [None],
    'tfidf__norm': [u'l2'],
    'tfidf__use_idf': [True,False],
    'tfidf__smooth_idf': [True,False],
    'tfidf__sublinear_tf': [True,False],
    'select__score_func': [chi2],
    'select__percentile': [10,16,20,100]
}
full_grid_parameters = {
    'vect__lowercase': [False],
    'vect__preprocessor': [normalizer.normalize],
    #'vect__strip_accents' : [u'ascii', u'unicode', None],
    'vect__token_pattern' : [u'(?u)\\b\\w\\w+\\b', u'\\b\\w+\\b'],
    'vect__encoding' : [u'utf-8'],
    'vect__min_df': [1,2],
    'vect__max_df': [0.25,0.5,0.75,1.0],
    #'vect__analyzer' : ['char'],
    'vect__ngram_range': [(1, 2),(1, 3),(1, 4),(1, 5)],
    'vect__stop_words': [u'english',None],
    'tfidf__norm': [u'l2'],
    'tfidf__use_idf': [True],
    'tfidf__smooth_idf': [True,False],
    'tfidf__sublinear_tf': [True,False],
    'select__score_func': [chi2],
    'select__percentile': [10,16,20,100]
}
best_grid_parameters = {
    'vect__lowercase': [False],
    'vect__preprocessor': [normalizer.normalize],
    #'vect__strip_accents' : [u'ascii', u'unicode', None],
    'vect__token_pattern' : [u'(?u)\\b\\w\\w+\\b'],
    'vect__encoding' : [u'utf-8'],
    'vect__min_df': [1],
    'vect__max_df': [0.25,0.5,0.75,1.0],
    'vect__ngram_range': [(1,1),(1, 2),(1, 3),(1, 4)],
    'vect__stop_words': [u'english',None],
    'tfidf__norm': [u'l2'],
    'tfidf__use_idf': [True],
    'tfidf__smooth_idf': [True],
    'tfidf__sublinear_tf': [True],
    'select__score_func': [chi2],
    'select__percentile': [16,50,100]
}
def parameters_to_grid(params):
    for param, val in params.iteritems():
        params[param]=[val]
    print("grid")
    print(params)
    return params