import os
#import openai
import myShellDrv
from myGPT_Drv import GPT3_Drv, chat_Drv
import time
class theGPT3():
    def __init__(self, apiKey, name='CuteGPT'):
        # openai.api_key = apiKey
        # openai.api_type = "azure"
        # openai.api_base = "https://mygpt233.openai.azure.com/"
        # openai.api_version = "2022-12-01"
        self.maxTry = 3
        self.gptdrv = GPT3_Drv(maxTokens=256, apiKey=apiKey)
        #self.gptdrv = chat_Drv(maxTokens=maxTokens, apiKey=apiKey)
        self.chatHistory = ''
        self.actionHistory = ''
        self.emotionHistory = ''
        self.context2Introduction = 'This is a special context format. Follow this format strictly. Line 0 is this context struct introduction, do not change that; Line 1 is the chat history, do not change that; Line 2 is the emotion history, do not change that; Line 3 is the body action history, do not change that; Line 4 is users text input, you cannot change that; Line 5 is your action, you can do anything; Line 6 is your text output, you can say anything. Please respond a full complete context strictly with this format.'
        self.MaxMemForChatHistory = 512
        self.MaxMemForActionHistory = 256
        self.MaxMemForEmotionHistory = 256
        self.name = name

    def shrink(self, x, type = 0):
        if (type == 0):
            if (len(x) > self.MaxMemForChatHistory):
                x = x[len(x) - self.MaxMemForChatHistory:]
        elif (type == 1):
            if (len(x) > self.MaxMemForActionHistory):
                x = x[len(x) - self.MaxMemForActionHistory:]
        elif (type == 2):
            if (len(x) > self.MaxMemForEmotionHistory):
                x = x[len(x) - self.MaxMemForEmotionHistory:]
        return x

    def makeContext2(self, userTxtInput = 'Hello'):
        context2 = self.context2Introduction + '\n'
        context2 += 'ChatHistory: ' + self.chatHistory + '\n'
        context2 += 'EmotionHistory: ' + self.emotionHistory + '\n'
        context2 += 'BodyActHistory: ' + self.actionHistory + '\n'
        context2 += 'UserTxtInput: ' + userTxtInput + '\n'
        context2 += 'Emotional: ...Fill out here.\n'
        context2 += 'BodyAct: ...Fill out here.\n'
        context2 += 'TxtOutput: ...Fill out here.\n'
        context2 += '-------------------------------\n'
        context2 += self.context2Introduction + '\n'
        context2 += 'ChatHistory: ' + self.chatHistory + '\n'
        context2 += 'EmotionHistory: ' + self.emotionHistory + '\n'
        context2 += 'BodyActHistory: ' + self.actionHistory + '\n'
        context2 += 'UserTxtInput: ' + userTxtInput + '\n'
        return context2

    def interactive(self, x):
        x = x.replace('\n', ' ')
        self.chatHistory += 'User: ' + x + '. '
        self.chatHistory = self.shrink(self.chatHistory, 0)
        x = self.makeContext2(userTxtInput=x)
        #print(x)
        i = 0
        while(i < self.maxTry):
            try:
                res = self.gptdrv.forward(x).split('\n')
                print(res)
                Emotional = res[0].split(': ')[1]
                Action = res[1].split(': ')[1]
                TxtOutput = '\n'.join(res[2:])
                TxtOutput = TxtOutput.split(': ')[1]
                self.emotionHistory += Emotional + ';'
                self.shrink(self.emotionHistory, 2)
                self.actionHistory += time.ctime().replace(' ', '_') + ' ' + Action + ';'
                self.shrink(self.actionHistory, 1)
                if '\n' in TxtOutput:
                    self.chatHistory += self.name + ': ' + TxtOutput.replace('\n', '<br>')
                else:
                    self.chatHistory += self.name + ': ' + TxtOutput + ' '
                return Emotional, Action, TxtOutput
            except:
                print('Emmmm GPT give a bad response, try again...')
                i += 1
                continue
        return None

if __name__ == '__main__':
    myGPT3 = theGPT3(open('azgpt3.key','r').readline(), 1536)
    #myGPT3.ask('Hello World!')
    while True:
        res = myGPT3.interactive(input('Type something: '))
        #print(res)
