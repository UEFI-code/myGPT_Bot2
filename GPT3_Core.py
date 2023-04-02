import os
#import openai
from myGPT_Drv import GPT3_Drv
import time
class theGPT3():
    def __init__(self, apiKey, maxTokens):
        # openai.api_key = apiKey
        # openai.api_type = "azure"
        # openai.api_base = "https://mygpt233.openai.azure.com/"
        # openai.api_version = "2022-12-01"
        self.gptdrv = GPT3_Drv(maxTokens=maxTokens, apiKey=apiKey)
        self.maxTokens = maxTokens
        self.Emotional = '...'
        self.chatHistory = ''
        self.actionHistory = ''
        self.context2Introduction = 'This is a special context format. Line 0 is this context struct introduction, do not change that; Line 1 is your emotional, you can manage it yourself freedom; Line 2 is courrent zone time, do not change that; Line 3 is the chat history, do not change that; Line 4 is your action history, do not change that; Line 5 is users text input, you cannot change that; Line 6 is your action, you can do anything; Line 7 and later is your text output, you can say anything. Please respond a full complete context strictly with this format.'

        self.MaxMemForChatHistory = 1024
        self.MaxMemForActionHistory = 4000 - maxTokens - len(self.context2Introduction) - self.MaxMemForChatHistory - 128
        self.maxTry = 3

    def shrink(self, x, type = 0):
        if (type == 0):
            if (len(x) > self.MaxMemForChatHistory):
                x = x[len(x) - self.MaxMemForChatHistory:]
        else:
            if (len(x) > self.MaxMemForActionHistory):
                x = x[len(x) - self.MaxMemForActionHistory:]
        return x

    def makeContext2(self, userTxtInput = 'Hello'):
        context2 = self.context2Introduction + '\n'
        context2 += 'Emotional: ' + self.Emotional + '(change here to your realtime feeling)\n'
        context2 += 'TimeNow: ' + time.ctime() + '\n'
        context2 += 'ChatHistory: ' + self.chatHistory + '\n'
        context2 += 'ActionHistory: ' + self.actionHistory + '\n'
        context2 += 'UserTxtInput: ' + userTxtInput + '\n'
        context2 += 'Action: ...Fill out here.\n'
        context2 += 'TxtOutput: ...Fill out here.\n'
        context2 += '-------------------------------\n'
        context2 += self.context2Introduction + '\n'
        return context2

    def interactive(self, x):
        x = x.replace('\n', ' ')
        self.chatHistory += 'User: ' + x + '. '
        self.chatHistory = self.shrink(self.chatHistory, 0)
        x = self.makeContext2(userTxtInput=x)
        i = 0
        while(i < self.maxTry):
            try:
                res = self.gptdrv.forward(x).split('\n')
                self.Emotional = res[0].split(': ')[1]
                self.actionHistory += time.ctime().replace(' ', '_') + ' ' + res[5].split(':')[1][1:] + ';'
                self.actionHistory = self.shrink(self.actionHistory, 1)
                self.chatHistory += 'Bot: ' + res[6].split(': ')[1]
                if (len(res) > 7):
                    for i in range(7, len(res)):
                        self.chatHistory += '<br>' + res[i]
                self.chatHistory += ' '
                return res
            except:
                print('Emmmm GPT give a bad response, try again...')
                i += 1
                continue
        return None

if __name__ == '__main__':
    myGPT3 = theGPT3(open('azgpt3.key','r').readline(), 2048)
    #myGPT3.ask('Hello World!')
    while True:
        res = myGPT3.interactive(input('Type something: '))
        print(res)
        # print('Line 0:' + res[0])
        # print('Line 1:' + res[1])
        # print('Line 2:' + res[2])
        # print('Line 3:' + res[3])