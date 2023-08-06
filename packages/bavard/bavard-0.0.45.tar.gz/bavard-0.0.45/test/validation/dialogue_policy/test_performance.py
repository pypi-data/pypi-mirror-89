import json
from unittest import TestCase

from bavard.dialogue_policy.models import Classifier


class TestPerformance(TestCase):
    def setUp(self):
        super().setUp()
        with open("test/data/agents/bavard.json") as f:
            self.agent = json.load(f)

    def test_model_performance(self):
        # The DP model should be able to at *least* memorize and recreate a small
        # set of training conversations when in predict/inference mode.
        model = Classifier()
        model.fit(self.agent)
        train_performance = model.score(self.agent)
        print("train_performance:", train_performance)
        self.assertGreaterEqual(train_performance["f1_macro"], .95)
