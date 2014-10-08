from sklearn.linear_model import RidgeClassifier
from sklearn.svm import SVC,LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid

classifiers = {
	"MultinomialNB": {
		"classifier": MultinomialNB, 
		"grid_parameters":{"alpha":[.01]}
	},
	"BernoulliNB": {
		"classifier": BernoulliNB, 
		"grid_parameters":{"alpha":[.01],"binarize":[0,0.01,0.001]}
	},
	"NearestCentroid": {
		"classifier": NearestCentroid, 
		"grid_parameters":{}
	},
	"RidgeClassifier": {
		"classifier": RidgeClassifier, 
		"grid_parameters":{"tol": [1e-2], "solver": ["lsqr"]}
	},
	"Perceptron": {
		"classifier": Perceptron, 
		"grid_parameters":{"n_iter": [25,50,100]}
	},
	"PassiveAggressiveClassifier": {
		"classifier": PassiveAggressiveClassifier, 
		"grid_parameters":{"n_iter": [25,50,100]}
	},
	"KNeighborsClassifier": {
		"classifier": KNeighborsClassifier, 
		"grid_parameters":{"n_neighbors": [5,10,20,100]}
	},
	"SVC": {
		"classifier": SVC, 
		"grid_parameters":{'kernel':('linear', 'rbf'), 'C':[1, 10]}
	},
	"LinearSVC": {
		"classifier": LinearSVC, 
		"grid_parameters":{"loss":['l2'], "penalty": ["l2", "l1"], "dual":[False], "tol": [1e-3]}
	},
	"SGDClassifier": {
		"classifier": SGDClassifier, 
		"grid_parameters":{"alpha":[.0001], "loss": ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron','squared_loss', 'huber', 'epsilon_insensitive', 'squared_epsilon_insensitive'], "n_iter": [25,50,100], "penalty": ["l2", "l1","elasticnet"]}
	}
}