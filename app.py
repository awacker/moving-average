import os
import json
from src.maengine import MAEngine, DocumentObtainError, DocumentProcessingError, DocumentSaveError


credential_path = os.path.join(os.path.sep, os.path.dirname(__file__), 'config', 'credentials.json')
document = json.load(open(os.path.join(os.path.sep, os.path.dirname(__file__), 'config', 'document.json')))

ma_engine = MAEngine(credential_path)

try:
    if ma_engine.build(document):
        print("MA build was successfully completed!")

except ConnectionError as e:
    print("{}: {}\nPlease check access and credentials to the Google Drive".format(e.__class__.__name__, e))

except DocumentObtainError as e:
    print("{}: {}\nPlease check ability to open the document '{}'".format(
        e.__class__.__name__, e, document['spreadsheet_id']))

except DocumentProcessingError as e:
    print("{}: {}\nPlease check input data".format(e.__class__.__name__, e))

except DocumentSaveError as e:
    print("{}: {}\nPlease check access and edit permission for the document '{}'".format(
        e.__class__.__name__, e, document['spreadsheet_id']))

except Exception as e:
    print("{}: {}\nUnexpected Error!".format(e.__class__.__name__, e))
