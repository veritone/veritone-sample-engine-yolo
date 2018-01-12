import unittest
import numpy
import json
import sys
sys.path.insert(0, 'src/')
from helper import create_result, group_recognition_results, extract_original_video

class TestWorkflow(unittest.TestCase):

    def get_prediction_result(self):
        json_data = {
            "confidence": numpy.float32(0.1),
            "label": "car",
            "topleft": {"y": 400, "x": 0},
            "bottomright": {"y": 693, "x": 193}
        }

        return json_data

    def test_create_result(self):
        json_data = self.get_prediction_result()
        result = create_result(json_data, 0, 1.0)
        self.assertEqual(json_data["label"], result["found"])
        self.assertEqual(0, result["start"])
        self.assertEqual(json_data["confidence"], result["confidence"])

    def test_create_group_results(self):
        res1 = self.get_prediction_result()

        res2 = self.get_prediction_result()
        res2["label"] = "blah"

        result1 = create_result(res1, 0, 1.0)
        result2 = create_result(res1, 0, 1.0)
        result3 = create_result(res2, 0, 1.0)

        grouped_1 = group_recognition_results([result1, result2])
        self.assertEqual(1, len(grouped_1))

        grouped_2 = group_recognition_results([result1, result2, result3])
        self.assertEqual(2, len(grouped_2))

    def test_get_original_video(self):
        json_data = '''
        {
          "data": {
            "temporalDataObject": {
              "assets": {
                "records": [
                  {
                    "name": null,
                    "contentType": "video/mp4",
                    "type": "media",
                    "signedUri": "https://example.com",
                    "createdDateTime": 1488966309
                  }
                ]
              }
            }
          }
        }'''

        recording = json.loads(json_data)

        video_url = extract_original_video(recording['data']['temporalDataObject']['assets']['records'], 'video/mp4')
        self.assertEqual("https://example.com", video_url)


if __name__ == '__main__':
    unittest.main()
