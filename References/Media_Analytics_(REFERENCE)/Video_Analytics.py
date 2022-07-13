import cv2
import torch
import pickle
import imutils
import numpy as np
from PIL import Image, ImageEnhance
import face_recognition


# Load the FR model
data = pickle.loads(open('/content/drive/MyDrive/OPPA_Face_Recognition/encodings.pickle', "rb").read())
print("Face Encodings has loaded!")

# Load the YOLO model
model = torch.hub.load('/content/drive/MyDrive/yolov5', 'custom', path='/content/drive/MyDrive/yolov5/runs/train/exp/weights/best.pt', source='local')
print("YOLO model has loaded!")
classes = model.names 

# Create VideoCapture object to READ in the video
cap = cv2.VideoCapture("/content/drive/MyDrive/What do Russia's moves in Ukraine mean_.mp4")

# Get the dimensions of the video
frame_width = int(cap.get(3)) 
frame_height = int(cap.get(4))

# Create VideoWriter object to WRITE the video (after bounding boxes and texts are drawn)
output_video = cv2.VideoWriter('/content/drive/MyDrive/Video_Output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

if (cap.isOpened()== False):
  print("Error opening video stream or file")

# Continuous loop for the duration of the video
while(cap.isOpened()):
  ret, frame = cap.read()
  if ret == True:
    output = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# FACE RECOGNITION DETECTIONS:
    boxes = face_recognition.face_locations(frame, model='cnn')
    encodings = face_recognition.face_encodings(frame, boxes)
    names = []

    for encoding in encodings:
      matches = face_recognition.compare_faces(data["encodings"], encoding, tolerance=0.4)
      name = "Unknown"

      if True in matches:
        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
        counts = {}

        for i in matchedIdxs:
          name = data["names"][i]
          counts[name] = counts.get(name, 0) + 1

        name = max(counts, key=counts.get)

      names.append(name)

    for ((top, right, bottom, left), name) in zip(boxes, names):
      cv2.rectangle(output, (left, top), (right, bottom), (147,20, 255), 2)
      y = top - 15 if top - 15 > 15 else top + 15
      cv2.putText(output, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (147,20, 255), 3)


# OBJECT DETECTIONS:
    frame = [frame]
    OD_Results = model(frame)

    # Retrieve the labels and coordinates of ALL the objects detected in that one frame
    labels, coordinates = OD_Results.xyxyn[0][:, -1], OD_Results.xyxyn[0][:, :-1]
    n = len(labels)
    x_shape, y_shape = output.shape[1], output.shape[0]

    # looping through the detections
    for i in range(n):
        bbox = coordinates[i]
        label = classes[int(labels[i])]

        # Set a threshold value
        if bbox[4] >= 0.10:

          # Convert the "NORMALISED" coordinates of the bbox back to their orginal value relative to the frame dimensions
          x1, y1, x2, y2 = int(bbox[0]*x_shape), int(bbox[1]*y_shape), int(bbox[2]*x_shape), int(bbox[3]*y_shape)

          if label == 'Soldier':
            # Draw the rectangles and labels
            cv2.rectangle(output, (x1, y1), (x2, y2), (0,140,255), 2)
            cv2.putText(output, label + f" {round(float(bbox[4]),2)}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 140,255), 3)
          
          elif label == 'Civilian':
            # Draw the rectangles and labels
            cv2.rectangle(output, (x1, y1), (x2, y2), (0,255,255), 2)
            cv2.putText(output, label + f" {round(float(bbox[4]),2)}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255,255), 3)

          elif label == 'Weapon':
            # Draw the rectangles and labels
            cv2.rectangle(output, (x1, y1), (x2, y2), (0,69,255), 2)
            cv2.putText(output, label + f" {round(float(bbox[4]),2)}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 69,255), 3)

          elif label == 'Tank':
            # Draw the rectangles and labels
            cv2.rectangle(output, (x1, y1), (x2, y2), (35,142,107), 2)
            cv2.putText(output, label + f" {round(float(bbox[4]),2)}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (35, 142, 107), 3)

          elif label == 'Helicopter':
            # Draw the rectangles and labels
            cv2.rectangle(output, (x1, y1), (x2, y2), (255,255,0), 2)
            cv2.putText(output, label + f" {round(float(bbox[4]),2)}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,0), 3)

          elif label == 'Armoured Vehicle':
            # Draw the rectangles and labels
            cv2.rectangle(output, (x1, y1), (x2, y2), (255,105,65), 2)
            cv2.putText(output, label + f" {round(float(bbox[4]),2)}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,105,65), 3)

    output_video.write(output)
    
  else:
    break

cap.release()
output_video.release()
cv2.destroyAllWindows()