# simple_face_recognition
> A simple face recognition for ROS
## Install face_recognition
```shell=
pip3 install face_recognition
```
![ref.](https://github.com/ageitgey/face_recognition)

## Input known image
![image](https://user-images.githubusercontent.com/61956056/171125147-612eed3c-7737-42b9-be34-980d9320e920.png)

## Run Node
You should run roscore before run node.
```shell=
python3 simple_face_rec_node.py
```
Node info
> Adapted Realsense
```
Node [/simple_face_rec]
Publications: 
 * /output/image_raw/compressed [sensor_msgs/CompressedImage]
 * /rosout [rosgraph_msgs/Log]

Subscriptions: 
 * /camera/color/image_raw/compressed [unknown type]
Node [/simple_face_rec]
Publications: 
 * /output/image_raw/compressed [sensor_msgs/CompressedImage]
 * /rosout [rosgraph_msgs/Log]

Subscriptions: 
 * /camera/color/image_raw/compressed [unknown type]
```
## Demo
https://user-images.githubusercontent.com/61956056/171126573-54bd30df-d413-4fdc-b5a2-6d7cdac17b50.mp4

