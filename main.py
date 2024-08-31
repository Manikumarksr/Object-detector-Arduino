a=['bicycle',
   'person',
 'car',
 'motorcycle',
 'bus',
 'train',
 'truck',
 'bench',
 # 'cat',
 'dog',
 'cow',
 'backpack',
 'umbrella',
 'shoe',
 'eye glasses',
 # 'handbag',
 # 'suitcase',
 'bottle',
 'plate',
 'cup',
 'knife',
 'spoon',
 'bowl',
 'banana',
 'apple',
 'chair',
 'couch',
 'potted plant',
 'bed',
 'dining table',
 'desk',
 'toilet',
 'door',
 'tv',
 'laptop',
 'remote',
 'keyboard',
 'cell phone',
 'refrigerator',
 'book',
 'clock',
 'scissors',
 ]
from kivy.app import App
from kivy.uix.label import Label
#from kvdroid.tools import speech
# from plyer import tts

# from kivy.uix.boxlayout import BoxLayout
# from kivy.core.window import Window
# from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.clock import Clock
import numpy as np
import threading
import cv2
import pyttsx3
import urllib.request
import re
# import os
# app_folder = os.path.dirname(os.path.abspath(__file__))
url = r"http://192.168.4.22/"

objs =[""]
dist =[]
times = 0
thres = 0.6 
prevname=''
distance=0

classNames = []
classFile = "Object_Detection_Files/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "Object_Detection_Files/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def getObjects(img, thres, nms,objects=[]):

    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)

    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])


    for object in objectInfo:
        obj = object[len(object)-1]
        for obje in a:
            if(obje == obj):
                objs.append(obj)
    url_response = urllib.request.urlopen(url)
    # url_response=""
    # def connect(host='http://google.com'):
    #     try:
    #         url_response = urllib.request.urlopen(url)
    #         return True
    #     except:
    #         return False
    # print("connected" if connect() else "no internet!")
    url_contents = url_response.read().decode()
    data = re.findall(r'\d+', url_contents)
    # if (abs(dist[-1] - int(data[0])) < 50):
        # print("data is ", data[0])
    if(int(data[0])>5 and int(data[0])<500 ):
        dist.append(int(data[0]))

    return img,objectInfo

def most_frequent(List):
    return max(set(List), key = List.count)

def text_speech():
    objname=''
    global prevname
    global distance
    speech = pyttsx3.init()
    count = 0
    index = 0
    temp = 0
    for x in range(0,len(objs)):
        if(x !='person'):
            temp = objs.count(objs[x])
            if(temp > count):
                count = temp
                index=x
    # size=len(dist)
    avg = most_frequent(dist)
    # if(len(dist)>1):
    #     dist.pop(0)
    #     avg =most_frequent(dist)
    # else:
    #     avg =most_frequent(dist)
    # print(objs[index],avg)
    if (objs[index]!= ""):
        # voice = objs[index]+"is in",str(avg),"centimeters"
        # speech.say(objs[index]+"is in"+str(int(avg))+"centimeters")
        objname=objs[index]
    elif('person' in objs):
        # speech.say("person is in" + str(int(avg)) + "centimeters")
        objname='person'
    else:
        objname = 'Unidentified object'
        # tts.speak("Unidentified object is in" + str(int(avg)) + "centimeters")
    if(objname != prevname or (int(avg)< distance-5 or int(avg)> distance+5)):
        speech.say(objname + " is in " + str(int(avg)) + " centimeters")
        prevname = objname
        distance = int(avg)
        speech.runAndWait()
    objs.clear()
    # x = dist[-1]
    # print(dist)
    dist.clear()
    objs.append("")
    # dist.append(x)


def main_func():
    # speech.say("Object detection started sucessfully", "en")

    # "http://192.168.4.25:81/stream"
    # cap = cv2.VideoCapture(r"http://192.168.4.25:81/stream",cv2.CAP_ANY)
    # # cap.set(cv2.CV_CAP_PROP_FPS, 60)
    # cap.set(cv2.CAP_PROP_BUFFERSIZE, 5)
    # cap.set(3, 480)
    # cap.set(4, 320)
    # cap.set(10,70)
    while True:
        img_resp = urllib.request.urlopen("http://192.168.4.25/cam-hi.jpg")
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgnp, -1)

        # bbox, label, conf = cv.detect_common_objects(im)

        # success, img = cap.read()
        # if(success):
            # result, objectInfo = getObjects(img, thres, 0.2)
        getObjects(img, thres, 0.2)
            # print("object info: ",objectInfo)
            # print("Result: ",result)
            # cv2.imshow("Output",img)
        global times
        times += 1
        if (times % 10) == 0:
            times = 0
            text_speech()
        # cv2.waitKey(1)

thread1 = threading.Thread(target= main_func)

class Main_App(App):
    def build(self):
        return Label(text="Welcome\n\nRunning...",halign='center')


if __name__ == '__main__':
    Main_app=Main_App()
    thread1.start()
    threading.Thread(target=Main_app.run())



