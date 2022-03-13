# initialize the video stream
# import cv2


# video_cap = cv2.VideoCapture('rtsp://admin:SFYZEV@78.113.98.174:554/H.264')

# # grab the width, height, and fps of the frames in the video stream.
# frame_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# frame_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fps = int(video_cap.get(cv2.CAP_PROP_FPS))

# # initialize the FourCC and a video writer object
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# output = cv2.VideoWriter('output.mp4', fourcc, fps, (frame_width, frame_height))

# while True:
#     success, frame = video_cap.read()
#     cv2.imshow("frame", frame)
#     # write the frame to the output file
#     output.write(frame)
#     if cv2.waitKey(20) == ord('q'):
#         break

# video_cap.release()
# output.release()
# cv2.destroyAllWindows()
from deepface import DeepFace

DeepFace.verify('sample1/sample.jpg', 'storedFace/chair_1_customer_1.jpg',model_name='Facenet512',prog_bar=False,enforce_detection=False)