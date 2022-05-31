import face_recognition as fr
import cv2
import numpy as np
import rospy
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError
import glob

# Load a sample picture and learn how to recognize it.
john_image = fr.load_image_file("john.jpg")
john_face_encoding = fr.face_encodings(john_image)[0]
# Load a second sample picture and learn how to recognize it.
lemon_image = fr.load_image_file("lemon.jpg")
lemon_face_encoding = fr.face_encodings(lemon_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    john_face_encoding,
    lemon_face_encoding
]
known_face_names = [
    "John",
    "Lemon"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

def get_users():

    known_names=[]
    known_encods=[]

    for i in glob.glob("john/*.jpg"):
        img = fr.load_image_file(i)
        encoding = fr.face_encodings(img)[0]
        known_encods.append(encoding)
        known_names.append('john')

    return known_names, known_encods 

# known_face_encodings ,known_face_names = get_users()

def face_rec(frame):
    # Grab a single frame of video
    # ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    # Find all the faces and face encodings in the current frame of video
    face_locations = fr.face_locations(rgb_small_frame)
    face_encodings = fr.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = fr.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = fr.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    return frame

class getImage():
    def __init__(self):
        self.bridge = CvBridge()
        self.pub = rospy.Publisher("/output/image_raw/compressed", CompressedImage, queue_size=1)
        self.image_topic = "/camera/color/image_raw/compressed"
        self.process_this_frame = True

    def callback(self, msg):
        # ROS_INFO("Received an image!")
        try:
            if self.process_this_frame:
                # Convert your ROS Image message to OpenCV2
                cv2_img = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
                msg = CompressedImage()
                msg.header.stamp = rospy.Time.now()
                msg.format = "jpeg"
                cv2_img = face_rec(cv2_img)
                msg.data = np.array(cv2.imencode('.jpg', cv2_img)[1]).tostring()
                self.pub.publish(msg)
        except CvBridgeError as e:
            print(e)
        self.process_this_frame = not self.process_this_frame

def main():
    get_image = getImage()
    rospy.init_node('simple_face_rec')
    rospy.Subscriber(get_image.image_topic, CompressedImage, get_image.callback, queue_size=1)
    print("Start face recognition ...")
    rospy.spin()

if __name__ == "__main__":
    main()
