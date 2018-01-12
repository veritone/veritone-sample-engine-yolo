import glob
import os
from darkflow.net.build import TFNet
import cv2
import logging
from helper import extract_original_video

DARKFLOW_DIR = "darkflow/"
TEMP_DIR = "temp/"

def process(assets, detectionThreshold, fps):
    video_url = extract_original_video(assets, 'video/mp4')
    if not video_url:
        raise ValueError("Can't find original video URL")

    os.chdir(DARKFLOW_DIR)
    jpegs = extract_frames(video_url, fps)
    predictions_per_frame = predict(jpegs, detectionThreshold, fps)

    return predictions_per_frame

def extract_frames(video_file, fps):
    """
    Extract frames from a video file
    :param video_file: uri to a local or external file
    :param fps: the number of frames to extract per second
    :return: List of paths to extracted frames
    """
    logging.info("Generating thumbs for video file {0}".format(video_file))

    image_dir = TEMP_DIR + "jpeg/"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    image_path_template = image_dir + "frame{0}.jpg"
    frame_template = image_path_template.format("%09d")
    command = "ffmpeg -i \"{0}\" -f image2 -vf fps=fps={2} {1}".format(video_file, frame_template, fps)
    logging.info("Executing command: {0}".format(command))
    os.system(command)

    jpeg_file_mask = image_path_template.format("*")
    jpegs = glob.glob(jpeg_file_mask)
    jpegs_count = len(jpegs)
    logging.debug("Files generated = {0} at the dir {1}".format(jpegs_count, image_dir))

    if jpegs_count == 0:
        raise ValueError("No thumbs were generated")

    return jpegs


def predict(images, detectionThreshold, fps):
    """
    Runs object detection on every frame
    :param images: List of paths to extracted frames
    :param detectionThreshold: Minimum confidence value for detection
    :param fps: Frames per second used to calculate time between frames
    :return: formatted dict of detected objects
    """
    images.sort()

    results = []
    options = {"model": "cfg/yolo.cfg",
               "load": "yolo.weights",
               "threshold": detectionThreshold}

    tfnet = TFNet(options)

    for index, img in enumerate(images):
        imgcv = cv2.imread(img)
        predictions = tfnet.return_predict(imgcv)
        results.append(predictions)

    return results