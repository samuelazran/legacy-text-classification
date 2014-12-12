text-classification
-------------------

text-classification is a python package that uses popular ML libraries such as scikit-learn to simplify text classification tasks

the tasks are divided into 3 main modules:
---------------------------------------------
	1. tester - perform grid search for the best classifier and parameters set for the data, or run test on saved classifier and parameters
	2. learner - train model on the data given classifier and set of parameters
	3. predictor - use the saved model to predict the class of input text


STEP BY STEP HOW TO:
-------------------

    1. Install

        First of all - as this package uses scikit-learn you should install it before, and read the docs: http://scikit-learn.org/stable/

		After you understand how this package tools works for classification problems you can go ahead and use "text-classification".
        
		Download the zip or "git clone https://github.com/samuelazran/text-classification.git" to an empty folder.
        
		In the root folder ("text-classification-master") open command line window and type: "python setup.py install"
        
		The package will be installed into your python package folder (e.g c:\python27-32b\lib\site-packages\text_classification-0.1-py2.7.egg\)
        
		Navigate to the package library to use its command line interface:		"cd C:\Python27-32b\Lib\site-packages\text_classification-0.1-py2.7.egg\text_classification"

    2. Data
        Put the data you want to classify into the data folder (e.g C:\Python27-32b\Lib\site-packages\text_classification-0.1-py2.7.egg\text_classification\data\)
        
		Inside the "data" folder you should create hierarchical structure of folders that represents your dataset. for example for data set of tweets about bitcoin in english create:
            .../data/corpora/raw/en/bitcoin/twitter/
            
			The pattern is: .../<data folder>/corpora/raw/<language>/<domain>/<source>/
            Inside the source folder you should create the classes folders. for example, for sentiment classification create folders by the names:
            0_informative
            -1_negative
            1_positive
            
			The class folder name pattern is: <id number>_<class name> (the id number could be any positive or negative number, in this case -1 represent the id of the class negative, this number could be used later instead of the class name)
            In each folder put text files with text relating to the domain, each file includs the text content in raw plain text UTF-8 files.
            To get good results put at least 100 text files in each folder.

    3. Tester - examine classification algorithms on the data set with range of parameters to see who can guess the correct class most of the time.

        Navigate to the package library root folder to use its command line interface:
            
			cd C:\Python27-32b\Lib\site-packages\text_classification-0.1-py2.7.egg\text_classification
            
			Create the folders (if not exist yet): "stdout" and "models" in the root directory to store the stdout logs and the saved models.
        
		Run the tester module from the command line:
            
			python tester.py --model_id en_bitcoin_twitter --stdout test1 --fullgrid --start 1 --end 10
            
			This command will execute full grid search (try any possible parameter for the classifiers) and will test in turn each classifier on the data.
            
			The --model_id parameters is an id that represent the folder where the data is stored.
            
			The pattern here is: <language code name>_<domain>_<source> (e.g: en_bitcoin_twitter).
            
			The --stdout parameter is a name for the file where the tester output will go to.
        
		After some time you'll start seeing log similar to this:

            classifier BernoulliNB:

            ('classifier_grid_parameters', {'binarize': [0, 0.01, 0.001], 'alpha': [0.01]})
            parameters:
            {'vect__ngram_range': [(1, 2), (1, 3), (1, 4), (1, 5)], 'tfidf__smooth_idf': [True, False], 'vect__stop_words': [u'english', None], 'tfidf__sublinear_tf': [True, False], 'vect__max_df': [0.25, 0.5, 0.75, 1.0], 'select__percentile': [10, 16, 20, 100], 'vect__lowercase': [False], 'clf__binarize': [0, 0.01, 0.001], 'select__score_func': [<function chi2 at 0x089EE8F0>], 'tfidf__use_idf': [True], 'vect__min_df': [1, 2], 'tfidf__norm': [u'l2'], 'vect__encoding': [u'utf-8'], 'vect__token_pattern': [u'(?u)\\b\\w\\w+\\b', u'\\b\\w+\\b'], 'clf__alpha': [0.01], 'vect__preprocessor': [<bound method Normalizer.normalize of <normalizer.Normalizer instance at 0x08A86C10>>]}

            Fitting 3 folds for each of 6144 candidates, totalling 18432 fits
            C:\Python27-32b\lib\site-packages\sklearn\feature_selection\univariate_selection.py:319: UserWarning: Duplicate scores. Result may depend on feature ordering.There are probably duplicate features, or you used a classification score for a regression task.
              warn("Duplicate scores. Result may depend on feature ordering."
            [Parallel(n_jobs=1)]: Done   1 jobs       | elapsed:    0.0s
            [Parallel(n_jobs=1)]: Done  50 jobs       | elapsed:    1.1s
            [Parallel(n_jobs=1)]: Done 200 jobs       | elapsed:    4.7s
            [Parallel(n_jobs=1)]: Done 450 jobs       | elapsed:   10.8s
            [Parallel(n_jobs=1)]: Done 800 jobs       | elapsed:   19.6s
            [Parallel(n_jobs=1)]: Done 1250 jobs       | elapsed:   30.2s
            [Parallel(n_jobs=1)]: Done 1800 jobs       | elapsed:   43.1s
            [Parallel(n_jobs=1)]: Done 2450 jobs       | elapsed:   59.6s
            [Parallel(n_jobs=1)]: Done 3200 jobs       | elapsed:  1.3min
            [Parallel(n_jobs=1)]: Done 4050 jobs       | elapsed:  1.6min
            [Parallel(n_jobs=1)]: Done 5000 jobs       | elapsed:  2.0min
            [Parallel(n_jobs=1)]: Done 6050 jobs       | elapsed:  2.4min
            [Parallel(n_jobs=1)]: Done 7200 jobs       | elapsed:  2.9min
            [Parallel(n_jobs=1)]: Done 8450 jobs       | elapsed:  3.3min
            [Parallel(n_jobs=1)]: Done 9800 jobs       | elapsed:  3.9min
            [Parallel(n_jobs=1)]: Done 11250 jobs       | elapsed:  4.4min
            [Parallel(n_jobs=1)]: Done 12800 jobs       | elapsed:  5.1min
            [Parallel(n_jobs=1)]: Done 14450 jobs       | elapsed:  5.7min
            [Parallel(n_jobs=1)]: Done 16200 jobs       | elapsed:  6.4min
            [Parallel(n_jobs=1)]: Done 18050 jobs       | elapsed:  7.2min
            [Parallel(n_jobs=1)]: Done 18432 out of 18432 | elapsed:  7.4min finished
            ()
            Best score: 0.625000000
            Best parameters set:
                clf__alpha: 0.01
                clf__binarize: 0
                select__percentile: 100
                select__score_func: <function chi2 at 0x089EE8F0>
                tfidf__norm: u'l2'
                tfidf__smooth_idf: True
                tfidf__sublinear_tf: True
                tfidf__use_idf: True
                vect__encoding: u'utf-8'
                vect__lowercase: False
                vect__max_df: 0.25
                vect__min_df: 1
                vect__ngram_range: (1, 2)
                vect__preprocessor: <bound method Normalizer.normalize of <normalizer.Normalizer instance at 0x08A86C10>>
                vect__stop_words: u'english'
                vect__token_pattern: u'(?u)\\b\\w\\w+\\b'

        The first part, is the classifier algorithm name.
        
		The second part, is the range of parameters the system will try the classifier with.
        
		The third part, is the log of the testing jobs (this part might take some time depending on the computing resources, the classifier is being tested with any combination of parameters on the dataset).
        
		The forth part, is the best parameters for the classifier, along with the score of the tests the computer did with this parameters.
        
		You should look over the results of the all classifiers and pick the the one with the best score.

The package is being developed in my spare time. And I'll try maintain it and update the docs as much as I can.
If you'd like to use or improve it, you are more than welcome to contact me at: samuel azran (in one word) at gmail.