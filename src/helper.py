import logging


def format_output(predictions_per_frame, fps):
    """
    Transforms detection results to Veritone Object format of:
    {
      "series": [
        {
          "found": "outdoor",
          "start": 0,
          "end": 109050,
          "confidence": 825
        },
        ...
      ]
    }
    :param predictions_per_frame: yolo Output per frame
    :param fps: frames per second extracted from video
    :return: Veritone Object Series data
    """
    results = []
    for index, predictions in enumerate(predictions_per_frame):
        for prediction in predictions:
            result = create_result(prediction, index, fps)
            results.append(result)

    clump_threshold_ms = 1000 / fps
    return {'series': group_recognition_results(results, clump_threshold_ms)}


def group_recognition_results(data, clump_threshold_ms=1000):
    """Groups together objects that have been detected in previous frames."""
    sorted_data = sorted(data, key=lambda k: (str(k['found']), int(k['start'])))
    results = []
    prev_result = None
    for result in sorted_data:
        if not prev_result:
            prev_result = result
        else:
            clumped_together = (result['start'] - prev_result['end'] < clump_threshold_ms) or (
                    prev_result['start'] == result['start'])
            same_object = prev_result['found'] == result['found']

            if clumped_together and same_object:
                prev_result['end'] = result['end']
            else:
                results.append(prev_result)
                prev_result = result

    if prev_result:
        results.append(prev_result)

    return results


def create_result(json_data, start, fps):
    """Transforms yolo prediction data to Veritone Object."""
    left = json_data['topleft']['x']
    top = json_data['topleft']['y']
    width = json_data['bottomright']['x'] - left
    height = json_data['bottomright']['y'] - top

    result = {
        'boundingPoly': {
            'left': left,
            'top': top,
            'width': width,
            'height': height
        },
        'confidence': json_data['confidence'].astype(float),
        'found': json_data['label'],
        'start': start * 1000,  # in ms
        'end': int((start + 1) * 1000 / fps),
        'type': 'object',
    }

    return result


def extract_original_video(assets, content_type):
    """Extracts the signedUri for the oldest asset of the specified content type."""
    logging.debug("Extracting video from assets {}".format(assets))
    # filter by video assets only
    filtered_assets = [asset for asset in assets if asset['contentType'] == content_type]

    if not filtered_assets:
        return None

    # Assume an oldest asset is original
    asset = min(filtered_assets, key=lambda x: x['createdDateTime'])
    return asset['signedUri']
