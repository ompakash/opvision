from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FeatureDetectionSerializer
from .models import FeatureDetection
import cv2
import numpy as np
from pathlib import Path
import os


class FeatureDetectionView(APIView):
    serializer_class = FeatureDetectionSerializer

    def get(self, request):
        images = FeatureDetection.objects.all()
        img = FeatureDetectionSerializer(many=True)

        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        BASE_DIR = Path(__file__).resolve().parent.parent

        image_path = os.path.join(
            BASE_DIR, 'media\\FeatureDetection\\images\\bbd.jpg')
        print(image_path)

        # featureDetection(image_path)
        FeatureMatching(image_path)
        # Open image file stored in the database
        # f = open(image_path, "r")
        # print(f)
        return Response(img.data)

    def post(self, request):
        img = FeatureDetectionSerializer(data=request.data)
        if img.is_valid():
            img.save()
            return Response({"details": 'image uploaded'})


def featureDetection(image_path):

    # Getting the Image ready for feature detection
    input_image = cv2.imread(image_path)
    input_image = cv2.resize(input_image, (400, 550),
                             interpolation=cv2.INTER_AREA)
    gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

    # ORB ALGORITHM
    orb = cv2.ORB_create(nfeatures=1000)

    # find the keypoints with ORB
    keypoints, descriptors = orb.detectAndCompute(gray_image, None)

    # draw only the location of the keypoints without size or
    final_keypoints = cv2.drawKeypoints(
        gray_image, keypoints, input_image, (0, 255, 0))

    cv2.imshow('ORB keypoints', final_keypoints)
    cv2.waitKey()


# Initilizing the ORB Feature Detector
MIN_MATCHES = 20
detector = cv2.ORB_create(nfeatures=5000)

# Preparing the FLANN Based matcher
index_params = dict(algorithm=1, trees=3)
search_params = dict(checks=100)
flann = cv2.FlannBasedMatcher(index_params, search_params)

# Function for Loading input image and Keypoints


def load_input(image_path):
    print(image_path)
    input_image = cv2.imread(image_path)
    # input_image = cv2.imread('meluha.jpg')
    input_image = cv2.resize(input_image, (400, 550),
                             interpolation=cv2.INTER_AREA)
    gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    # find the keypoints with ORB
    keypoints, descriptors = detector.detectAndCompute(gray_image, None)
    return gray_image, keypoints, descriptors

# Function for Computing Matches between the train and query descriptors
def compute_matches(descriptors_input, descriptors_output):
	
	if(len(descriptors_output)!=0 and len(descriptors_input)!=0):
		matches = flann.knnMatch(np.asarray(descriptors_input,np.float32),np.asarray(descriptors_output,np.float32),k=2)
		good = []
		for m,n in matches:
			if m.distance < 0.68*n.distance:
				good.append([m])
		return good
	else:
		print('Returning none..')
		return None

# Main Working Logic
def FeatureMatching(image_path):
    print(image_path)

    # Getting Information form the Input image
    input_image, input_keypoints, input_descriptors = load_input(image_path)

    print('load input returned..')
    # Getting camera ready
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    print(ret, frame)

    while(ret):
        ret, frame = cap.read()

        # Condition Check for error escaping
        if(len(input_keypoints)<MIN_MATCHES):
            continue
        # Resizing input image for fast computation
        frame = cv2.resize(frame, (700,600))
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Computing and matching teh Keypoints of Input image and query Image
        output_keypoints, output_descriptors = detector.detectAndCompute(frame_bw, None)
        matches = compute_matches(input_descriptors, output_descriptors)

        if(matches!=None):
            output_final = cv2.drawMatchesKnn(input_image,input_keypoints,frame,output_keypoints,matches,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            cv2.imshow('Final Output', output_final)
        else:
            cv2.imshow('Final Output', frame)
        key = cv2.waitKey(5)
        if(key==27):
            break

