from sklearn.feature_selection import SelectPercentile, chi2
from normalizer import Normalizer

normalizer = Normalizer()

from models import *

#dict path pattern: language/domain/source/type  =  model
#e.g en/residence/agent/map
saved_models = {
    'en': {
        'residence': {
            'agent': {
                'map': Model(
                    model_properties = { 'language': 'en', 'domain': 'residence', 'source': 'agent', 'type': 'map' },
                    classifier_name = 'NearestCentroid',
                    pipeline_parameters = {
                        'select__percentile': 100,
                        'select__score_func': chi2,
                        'tfidf__norm': u'l2',
                        'tfidf__smooth_idf': True,
                        'tfidf__sublinear_tf': True,
                        'tfidf__use_idf': True,
                        'vect__encoding': u'utf-8',
                        'vect__lowercase': False,
                        'vect__max_df': 0.25,
                        'vect__min_df': 1,
                        'vect__ngram_range': (1, 1),
                        'vect__preprocessor': None,
                        'vect__stop_words': None,
                        'vect__token_pattern': u'(?u)\\b\\w\\w+\\b'
                    },
                    train_details=TrainDetails(score=0.83333333, items_amount=48)
                )
            }
        },
        'bitcoin': {
            'twitter': {
                'sentiment': Model(
                    model_properties = { 'language': 'en', 'domain': 'bitcoin', 'source': 'twitter', 'type': 'sentiment' },
                    classifier_name = 'SGDClassifier',
                    pipeline_parameters = {
                        'clf__alpha': 0.0001,
                        'clf__loss': 'epsilon_insensitive',
                        'clf__n_iter': 25,
                        'clf__penalty': 'l2',
                        'select__percentile': 100,
                        'select__score_func': chi2,
                        'tfidf__norm': u'l2',
                        'tfidf__smooth_idf': True,
                        'tfidf__sublinear_tf': True,
                        'tfidf__use_idf': True,
                        'vect__encoding': u'utf-8',
                        'vect__lowercase': False,
                        'vect__max_df': 0.25,
                        'vect__min_df': 1,
                        'vect__ngram_range': (1, 2),
                        'vect__preprocessor': normalizer.normalize,
                        'vect__stop_words': None,
                        'vect__token_pattern': u'(?u)\\b\\w\\w+\\b'
                    },
                    train_details=TrainDetails(score=0.722693831, items_amount=1767)
                )
            },
            'reddit': {
                'sentiment': Model(
                    model_properties = { 'language': 'en', 'domain': 'bitcoin', 'source': 'reddit', 'type': 'sentiment' },
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
            }
        },
        'room':{
            'facebook': {
                'type': Model(
                    model_properties = { 'language': 'en', 'domain': 'room', 'source': 'facebook', 'type': 'act' },
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
            }
        },
    },
    'nl': {
        'room': {
            'facebook': {
                'act': Model(
                    model_properties = { 'language': 'nl', 'domain': 'room', 'source': 'facebook', 'type':'act' },
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
}
