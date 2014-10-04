import sys, os
from sklearn.datasets import load_files
from sklearn.datasets import fetch_20newsgroups
import settings

data_path = settings.data_path
def load(path):
	if path=="newsgroups":
		categories=['alt.atheism', 'soc.religion.christian']
		data=fetch_20newsgroups(subset='all',categories=categories)
	else:
		data_container_path = data_path + 'corpora/raw/' + path
		print("Loading files dataset")
		data = load_files(data_container_path, load_content=True, shuffle=True, encoding='utf8', charset='utf8', charset_error='', decode_error='strict', random_state=42)
	
	rawdata, classes = data.data, data.target
	print("classes: %s" % data.target_names)
	print('data loaded')
	return rawdata, classes, data.target_names
def load_dataset(dataset_name):
    """Load and return dataset (classification).

    The dataset is a classic and very easy multi-class classification
    dataset.
	
    Returns
    -------
    data : Bunch
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn, 'target', the classification labels,
        'target_names', the meaning of the labels, 'feature_names', the
        meaning of the features

    Examples
    --------
    Let's say you are interested in the samples 10, 25, and 50, and want to
    know their class name.
	
    >>> data = load_dataset("en_room_facebook")
    >>> data.target[[10, 25, 50]]
    array([0, 0, 1])
    >>> list(data.target_names)
    ['room', 'rent', 'amsterdam']
    """
    data_file = csv.reader(open(join(data_path, 'datasets', dataset_name + '.csv')))
    first_line = next(data_file)
    n_samples = int(first_line[0])
    n_features = int(first_line[1])
    target_names = np.array(first_line[2:])
    second_line = next(data_file)
    feature_names = second_line
    data = np.empty((n_samples, n_features))
    target = np.empty((n_samples,), dtype=np.int)

    for i, line in enumerate(data_file):
        data[i] = np.asarray(line[:-1], dtype=np.float)
        target[i] = np.asarray(line[-1], dtype=np.int)

    return Bunch(data=data, target=target, target_names=target_names, feature_names=feature_names)
def save_dataset():
	return None