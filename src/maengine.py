from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import apiclient
import numpy as np
import math


class DocumentObtainError(Exception):
    pass


class DocumentProcessingError(Exception):
    pass


class DocumentSaveError(Exception):
    pass


class MAEngine:
    def __init__(self, credentials):
        self.credentials = credentials
        self.scope = ['https://www.googleapis.com/auth/spreadsheets']
        self.service = None

    def _connect(self):
        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials, self.scope)
            http_auth = credentials.authorize(httplib2.Http())
            self.service = apiclient.discovery.build('sheets', 'v4', http=http_auth)
        except Exception as e:
            raise ConnectionError(e)

    def _get_data(self, document):
        try:
            return self.service.spreadsheets().values().get(
                spreadsheetId=document['spreadsheet_id'],
                range=document['sheet']).execute()['values']
        except Exception as e:
            raise DocumentObtainError(e)

    @staticmethod
    def _document_processing(document, input_data):
        if document['source_field'] in input_data[0]:
            s_index = input_data[0].index(document['source_field'])
        else:
            raise DocumentProcessingError('Source field does not found!')

        try:
            input_data = [int(row[s_index]) for row in input_data[s_index:]]
            return np.convolve(input_data, np.repeat(1.0, 3) / 3, 'same').tolist()
        except Exception as e:
            raise DocumentProcessingError("Convolve process error: {}".format(e))

    def _save_result(self, document, input_data, output_data):

        def get_position(x, h):
            ord_a = ord('A')
            ord_z = ord('Z')
            length = ord_z - ord_a + 1
            s = ""
            while x >= 0:
                s = chr(x % length + ord_a) + s
                x = math.floor(x / length) - 1
            return "{}1:{}{}".format(s, s, h)

        t_index = 0
        if document['target_field'] in input_data[0]:
            t_index = input_data[0].index(document['target_field'])
        else:
            for i in input_data:
                if len(i) > t_index:
                    t_index = len(i)
        body = {'values': [[document['target_field']]] + [[row] for row in output_data]}

        try:
            self.service.spreadsheets().values().update(
                spreadsheetId=document['spreadsheet_id'],
                range=document['sheet'] + '!' + get_position(t_index, len(output_data) + 1),
                valueInputOption='RAW',
                body=body).execute()
        except Exception as e:
            raise DocumentSaveError(e)

    def build_ma(self, document):
        result = False
        try:
            if not self.service:
                self._connect()

            input_data = self._get_data(document)

            output_data = self._document_processing(document, input_data)

            self._save_result(document, input_data, output_data)

            result = True

        finally:
            return result
