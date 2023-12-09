import os
#import openai
import myShellDrv
from myGPT_Drv import GPT3_Drv, chat_Drv, GPT4_Drv
import time
class theGPT3():
    def __init__(self, apiKey, endpoint = 'https://mygpt233.openai.azure.com/openai/deployments/myGPT3/completions?api-version=2022-12-01', name='CuteGPT'):
        self.maxTry = 3
        #self.gptdrv = GPT3_Drv(apiKey=apiKey, endpoint=endpoint)
        self.gptdrv = GPT4_Drv(apiKey=apiKey, endpoint=endpoint, maxTokens=8000)
        #self.gptdrv = chat_Drv(apiKey=apiKey)
        self.chatHistory = ''
        self.actionHistory = ''
        self.emotionHistory = ''
        self.context2Introduction = 'This is a special context format. Follow this format strictly. Line 0 is this context struct introduction, do not change that; Line 1 is the chat history, do not change that; Line 2 is the emotion history, do not change that; Line 3 is the body action history, do not change that; Line 4 is your action, you can do anything; Line 5 is your text output, you can say anything. Please respond a full complete context strictly with this format.'
        # self.MaxMemForChatHistory = 512
        # self.MaxMemForActionHistory = 128
        # self.MaxMemForEmotionHistory = 128
        self.MaxCountForChatHistory = 10
        self.MaxCountForActionHistory = 10
        self.MaxCountForChatHistory = 10
        self.name = name

    def shrink(self, x, type = 0):
        if type == 0:
            x = x.split('. ')
            #print('Debug: ' + str(x))
            x = x[-self.MaxCountForChatHistory:]
            x = '. '.join(x)
        elif type == 1:
            x = x.split(';')
            x = x[-self.MaxCountForActionHistory:]
            x = ';'.join(x)
        elif type == 2:
            x = x.split(';')
            x = x[-self.MaxCountForChatHistory:]
            x = ';'.join(x)
        return x

    def makeContext2(self, userTxtInput = 'Hello'):
        context2 = self.context2Introduction + '\n'
        context2 += 'ChatHistory: ' + self.chatHistory + '\n'
        context2 += 'EmotionHistory: ' + self.emotionHistory + '\n'
        context2 += 'BodyActHistory: ' + self.actionHistory + '\n'
        #context2 += 'UserTxtInput: ' + userTxtInput + '\n'
        context2 += 'Emotional: ...Fill out here.\n'
        context2 += 'BodyAct: ...Fill out here.\n'
        context2 += 'TxtOutput: ...Fill out here.\n'
        context2 += '-------------------------------\n'
        context2 += self.context2Introduction + '\n'
        context2 += 'ChatHistory: ' + self.chatHistory + '\n'
        context2 += 'EmotionHistory: ' + self.emotionHistory + '\n'
        context2 += 'BodyActHistory: ' + self.actionHistory + '\n'
        #context2 += 'UserTxtInput: ' + userTxtInput + '\n'
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
                #print(res)
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
            except Exception as e:
                print('Emmmm GPT give a bad response ' + str(e))
                i += 1
                time.sleep(5)
                continue
        return None

if __name__ == '__main__':
    myGPT3 = theGPT3(open('azgpt3.key','r').readline())
    #myGPT3.ask('Hello World!')
    while True:
        res = myGPT3.interactive(input('Type something: '))
        #print(res)
