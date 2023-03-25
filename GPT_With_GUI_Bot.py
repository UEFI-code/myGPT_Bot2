import GPT3_Core
import os
import cv2
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(subscription=open('azspeech.key','r').readline(), region='japaneast')
# Note: the voice setting will not overwrite the voice element in input SSML.
speech_config.speech_synthesis_voice_name = "ja-JP-AoiNeural"
# use the default speaker as audio output.
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

myGPT3 = GPT3_Core.theGPT3(open('azgpt3.key','r').readline(), 2048)
#myGPT3.ask('Hello World!')

def show_simliar_figure(description, txtoutput):
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
    img = cv2.imread('figs/' + selectedfigure)
    txtPos = (int(img.shape[0] * 0.1), int(img.shape[1] * 0.8))
    cv2.putText(img, txtoutput, txtPos, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (128, 128, 255), 2)
    cv2.imshow('Bot', img)
    # make sure the window is on top
    cv2.setWindowProperty('Bot', cv2.WND_PROP_TOPMOST, 1)
    cv2.waitKey(1)

while True:
    res = myGPT3.interactive(input('Type something: '))
    #print(res)
    Emotional = res[0].split(': ')[1]
    Action = res[4].split(': ')[1]
    TxtOutput = res[5].split(': ')[1]
    if(len(res) > 6):
        for i in range(6, len(res)):
            TxtOutput += '\n' + res[i]
    DesiredFigFile = Emotional.split(' ')[0] + '_' + Action.split(' ')[0] + '.png'
    print('Emotional: ' + Emotional)
    print('Action: ' + Action)
    #print('Founding Figure: ' + FigFile)
    show_simliar_figure(DesiredFigFile, TxtOutput)
    print('TxtOutput: ' + TxtOutput)
    result = speech_synthesizer.speak_text_async(TxtOutput).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))