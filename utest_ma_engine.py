import unittest
from src.maengine import MAEngine
import os
import json


class MAEngineTest(unittest.TestCase):
    def test_build_ma(self):

        def test():
            ma_engine.build(document)
            return True

        credential_path = os.path.join(os.path.sep, os.path.dirname(__file__), 'config', 'credentials.json')
        document = json.load(open(os.path.join(os.path.sep, os.path.dirname(__file__), 'config', 'document.json')))
        ma_engine = MAEngine(credential_path)

        self.assertEqual(test(), True)


if __name__ == '__main__':
    unittest.main()