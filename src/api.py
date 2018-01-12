import json
import requests
import logging
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from http import HTTPStatus

VALID_TASK_STATUS = ['running', 'complete', 'failed']


class APIClient(object):
    def __new__(cls, baseUrl, token):
        if baseUrl is None or token is None:
            raise ValueError
        else:
            return super(APIClient, cls).__new__(cls)

    def __init__(self, baseUrl, token):
        self.baseUrl = baseUrl
        self.headers = {
            'Authorization': 'Bearer %s' % token,
        }
        transport = RequestsHTTPTransport(baseUrl, headers=self.headers,
                                          use_json=True)
        self.client = Client(transport=transport, fetch_schema_from_transport=True)
        logging.debug("Api Client initialized with baseUrl: {} and token: {}".format(baseUrl, token))

    def get_assets_for_recording(self, recording_id, asset_type):
        """Query to retrieve filtered assets for a recording by a specific asset type."""
        logging.debug("Getting {} assets for a recording {} ".format(asset_type, recording_id))
        query = gql('''
                    query{
                      temporalDataObject(id:"%s"){
                        assets(type:"%s") {
                          records  {
                            id
                            contentType
                            createdDateTime
                            signedUri
                          }
                        }
                      }
                    }
                    ''' % (recording_id, asset_type))
        try:
            response = self.client.execute(query)
            return response['temporalDataObject']['assets']['records']

        except Exception as e:
            logging.error('Failed to find {} for recording_id {} due to: {}'.format(asset_type, recording_id, e))
        return None

    def publish_results(self, recording_id, results):
        """Performs a Multipart/form-data request with the graphql query and the output file"""
        logging.debug("Publishing results for recording: {} . Results: {}".format(recording_id, results))
        filename = 'tmpfile'

        query = '''
            mutation {
              createAsset(
                input: {
                    containerId: "%s",
                    contentType: "application/json",
                    assetType: "object"
                }) {
                id
                uri
              }
            }
            ''' % recording_id

        data = {
            'query': query,
            'filename': filename
        }

        files = {
            'file': (filename, json.dumps(results))
        }

        try:
            response = requests.post(self.baseUrl, data=data, files=files, headers=self.headers)
            return response.status_code == HTTPStatus.OK
        except Exception as e:
            logging.error('Failed to create asset for recording: {} due to: {}'.format(recording_id, e))
            return False

    def update_task(self, job_id, task_id, status, output=None):
        logging.debug("Updating task status to {} for task_id: {}".format(status, task_id))
        if status not in VALID_TASK_STATUS:
            return False

        if output is None:
            output = {}

        query = gql('''
            mutation {
              updateTask(input: {id: "%s", jobId: "%s", status: %s, outputString: "%s"}) {
                id
                status
              }
            }
        ''' % (task_id, job_id, status, json.dumps(output).replace('"','\\"')))
        try:
            self.client.execute(query)
        except Exception as e:
            logging.error('Failed to update task {} status to {} due to: {}'.format(task_id, status, e))
            return False
