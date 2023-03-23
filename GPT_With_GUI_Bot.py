import GPT3_Core
import os
import cv2
myGPT3 = GPT3_Core.theGPT3(open('azgpt3.key','r').readline(), 2048)
#myGPT3.ask('Hello World!')

def show_simliar_figure(description):
    allfigures = os.listdir('figs')
    maxsimliar = 0
    selectedfigure = None
    for i in allfigures:
        simliar = 0
        for j in description:
            if j in i:
                simliar += 1
        if simliar > maxsimliar:
            maxsimliar = simliar
            selectedfigure = i
    print('Selected Figure: ' + selectedfigure)
    cv2.imshow('Bot', cv2.imread('figs/' + selectedfigure))
    # make sure the window is on top
    cv2.setWindowProperty('Bot', cv2.WND_PROP_TOPMOST, 1)
    cv2.waitKey(1)

while True:
    res = myGPT3.interactive(input('Type something: '))
    #print(res)
    Emotional = res[0].split(': ')[1]
    Action = res[4].split(': ')[1]
    TxtOutput = res[5].split(': ')[1]
    DesiredFigFile = Emotional.split(' ')[0] + '_' + Action.split(' ')[0] + '.png'
    print('Emotional: ' + Emotional)
    print('Action: ' + Action)
    #print('Founding Figure: ' + FigFile)
    show_simliar_figure(DesiredFigFile)
    print('TxtOutput: ' + TxtOutput)