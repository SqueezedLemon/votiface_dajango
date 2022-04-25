from django.shortcuts import get_object_or_404
from requests import request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from votiface_django import firebase
from face_recognition_api.checkfaces import findEncoding
import numpy as np
import cv2

class UserRecordView(APIView):
  def post(self, request):
    user = (get_token(request.data['email'],request.data['password']))
    if (user is not False):
      return Response(user , status = status.HTTP_202_ACCEPTED)
    else:
      return Response(status = status.HTTP_401_UNAUTHORIZED)

class UserDataView(APIView):
  def post(self, request):
    id = request.data['idToken']
    user = firebase.auth.get_account_info(id)
    user = user['users']
    user = user[0]
    user = str(user['localId'])
    data = firebase.db.child("Users").child(user).get()
    return Response(data.val(), status = status.HTTP_202_ACCEPTED)


class SetProfileImage(APIView):
  def post(self, request):
    try:
      id = request.data['idToken']
      user = firebase.auth.get_account_info(id)
      user = user['users']
      user = user[0]
      user = str(user['localId'])
      img = cv2.imdecode(np.fromstring(request.data['profileImage'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
      encode = findEncoding(img)
      encode = encode.tolist()
      image = request.data['profileImage']
      img = firebase.storage.child("profile-images/"+user+".jpeg").put(image, id)
      img_url = firebase.storage.child("profile-images/"+user+".jpeg").get_url(img['downloadTokens'])
      firebase.db.child("Users").child(user).child("profile_img").set(img_url,id)
      firebase.db.child("Users").child(user).child("Encode").set(encode,id)
      return Response(status = status.HTTP_202_ACCEPTED)
    except:
      return Response(status = status.HTTP_400_BAD_REQUEST)


def get_token(email , password):
  try:
    user = firebase.auth.sign_in_with_email_and_password(email , password)
    return {'idToken': user['idToken']}
  except:
    return False
