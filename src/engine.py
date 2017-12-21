import sys
import os
import json
import argparse
import logging
from api import APIClient
from workflow import process
from helper import format_output


PAYLOAD_ENV = 'PAYLOAD_FILE'
CONFIG_PATH = '../conf/config.json'

def load_json(file):
    logging.info('Loading {}'.format(file))
    with open(file, 'r') as json_file:
        return  json.loads(json_file.read())

def run(payload_arg):
    config = load_json(CONFIG_PATH)
    payload = load_json(payload_arg)

    client = APIClient(config['baseUri'], payload['token'])

    try:
        client.update_task(payload['jobId'], payload['taskId'], 'running')
        assets = client.get_assets_for_recording(payload['recordingId'], 'media')
        if not assets:
            raise ValueError('Cannot find assets for recording with id {}'.format(payload['recordingId']))

        predictions_per_frame = process(assets, config['detectionThreshold'], config['fps'])
        results = format_output(predictions_per_frame, config['fps'])

        results_published = client.publish_results(payload['recordingId'], results)

        if not results_published:
            client.update_task(payload['jobId'], payload['taskId'], 'failed')
            raise ValueError('Failed to publish results')
        else:
            client.update_task(payload['jobId'], payload['taskId'], 'complete', results)
    except Exception as ex:
        logging.error('Error during the execution {}'.format(ex))
        client.update_task(payload['jobId'], payload['taskId'], 'failed')
        raise ex


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

    PARSER = argparse.ArgumentParser(description='Veritone Developer - YOLO object detection engine')
    PARSER.add_argument('-payload', type=str)
    ARGS = PARSER.parse_args()
    PAYLOAD = vars(ARGS).get('payload', '')
    if os.getenv(PAYLOAD_ENV) is not None:
        PAYLOAD = os.getenv(PAYLOAD_ENV)

    if PAYLOAD is None:
        PARSER.print_help()
        sys.exit(1)

    run(PAYLOAD)