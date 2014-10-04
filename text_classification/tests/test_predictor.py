from unittest import TestCase

from text_classification import predictor

class TestPredict(TestCase):
    def test_is_array(self):
        language='en'
        domain='bitcoin'
        source='twitter'
        predictor.use_model(language,domain,source)
        predictions = predictor.predict(language,domain,source,"the price of bitcoin is up!")
        self.assertTrue(predictions is list)