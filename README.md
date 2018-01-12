# Veritone Sample Object Detection Engine - YOLO

This project demonstrates how to create an object detection engine Yolo recognition engine for running on Veritone's platform.
https://pjreddie.com/darknet/yolo/
https://github.com/pjreddie/darknet/wiki/YOLO:-Real-Time-Object-Detection

## Configuration
Located in conf/config.json

```
baseUri: Veritone GraphQL API endpoint
detectionThreshold: Range 0.0 - 1.0. Minimum confidence level to detect objects
fps: Positive Float. Sampling rate to perform object recognition. Highest FPS
```


#This version is provided with the pre-trained model which Yolo already provides
```
person
bicycle
car
motorbike
aeroplane
bus
train
truck
boat
traffic light
fire hydrant
stop sign
parking meter
bench
bird
cat
dog
horse
sheep
cow
elephant
bear
zebra
giraffe
backpack
umbrella
handbag
tie
suitcase
frisbee
skis
snowboard
sports ball
kite
baseball bat
baseball glove
skateboard
surfboard
tennis racket
bottle
wine glass
cup
fork
knife
spoon
bowl
banana
apple
sandwich
orange
broccoli
carrot
hot dog
pizza
donut
cake
chair
sofa
pottedplant
bed
diningtable
toilet
tvmonitor
laptop
mouse
remote
keyboard
cell phone
microwave
oven
toaster
sink
refrigerator
book
clock
vase
scissors
teddy bear
hair drier
toothbrush
```


# License
Copyright 2017, Veritone Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.