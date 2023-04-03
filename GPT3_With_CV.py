import GPT3_Core_old as GPT3_Core
import torchvision
import cv2
import drawer
import os
import random
import time
import subprocess

def processData(res, origimg=[]):
    final = ''
    for id in range(len(res[0]['scores'])):
        if res[0]['scores'][id] > 0.8:
            theRect = res[0]['boxes'][id]
            thePoints = res[0]['keypoints'][id]
            final += 'Rect: ' + str(theRect.int().tolist()) + '\n'
            #final += 'Points: ' + str(thePoints) + '\n'
            if origimg != []:
                drawer.draw(origimg, theRect, thePoints)
                cv2.imshow('frame', origimg)
                cv2.waitKey(1)
    return final
            
randomID = str(random.randint(0, 1000000))

model = torchvision.models.detection.keypointrcnn_resnet50_fpn(pretrained=True).eval()

camera = cv2.VideoCapture(0)

myAgent = GPT3_Core.theGPT3(open('gpt3.key','r').readline(), 2048)

print('----------Program Start----------')
myAgent.ask("""From now, you are react like a human. If you see line start with 'Rect:', it means that the CV model has detected a person, and the values after 'Rect:' is the bounding box of that person which including left-top corner (x1, y1) and right-botom corner(x2, y2). You can count the number of currently 'Rect:' to determine how many peoples are here. If you see a line start with 'UserInput:', it means a user is asking you a question.

For example, if you see:
{
Rect: [123, 123, 321, 321]
Rect: [400, 400, 700, 700]
UserInput: How many people are there?
}
It means that there are two people actually in the frame: the first people's left-top is (123, 123) and the first people's right-botom is (321, 321); the second people's left-top is (400, 400) and the second people's right-botom is (700, 700). One of them is asking how many people are there.

Please note, do not seem the 'Rect:' in the chat history as the currently Rect, only consider the 'Rect:' near the current 'UserInput:' as the currently Rect.

Directly answer the question, do not append 'Answer:' or 'GPT3:' or something like that.

OK, lets start! Don't do stupid things!
""")

print('----------Dump initial Context----------')
print(myAgent.context)
print('----------OK, Lets Play----------')

# voicePipline = subprocess.Popen(["say", "-v", "Tingting"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# voicePipline.stdin.write('Lets Start!'.encode('utf-8'))
# os.system('say -v Tingting Lets Start!')

while True:
    ret, frame = camera.read()
    if ret:
        res = model([torchvision.transforms.ToTensor()(frame)])
        data = processData(res, origimg=frame)
        if(len(data) > 5):
            userPrompt = 'UserInput: ' + input('Your question: ')
            gptRespond = myAgent.ask(data + userPrompt)
            print('GPT3: ' + gptRespond)
            open('/tmp/voice_' + randomID, 'wb').write(gptRespond.encode('utf-8'))
            os.system('say -v Tingting -f /tmp/voice_' + randomID)
            # print('----------Dump Context----------')
            # print(myAgent.context)

