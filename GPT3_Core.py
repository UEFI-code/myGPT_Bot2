import os

from myGPT_Drv import GPT3_Drv, chat_Drv, GPT4_Drv
import time
class theGPT3():
    def __init__(self, apiKey, endpoint = 'https://mygpt233.openai.azure.com/openai/deployments/myGPT3/completions?api-version=2022-12-01', name='CuteGPT'):
        self.maxTry = 3
        self.gptdrv = GPT3_Drv(apiKey=apiKey, endpoint=endpoint)
        #self.gptdrv = GPT4_Drv(apiKey=apiKey, endpoint=endpoint, maxReadToken=8192, maxOutToken=4096)
        #self.gptdrv = chat_Drv(apiKey=apiKey)
        self.chatHistory = ''
        self.actionHistory = ''
        self.emotionHistory = ''
        self.context2Introduction = f'Your name is {name}. This is a special context format. Follow this format strictly. Line 0 is this context struct introduction, do not change that; Line 1 is the chat history, do not change that; Line 2 is the emotion history, do not change that; Line 3 is the body action history, do not change that; Line 4 is your action, you can do anything; Line 5 is your text output, you can say anything. Please respond a full complete context strictly with this format.'
        self.name = name
    
    def stepShrinkWithMakeContext(self):
        x = self.makeContext2()
        while(len(x.encode()) > self.gptdrv.maxReadToken - 100):
            self.chatHistory.split('. ')
            self.chatHistory = '. '.join(self.chatHistory[1:])
            self.emotionHistory.split(';')
            self.emotionHistory = ';'.join(self.emotionHistory[1:])
            self.actionHistory.split(';')
            self.actionHistory = ';'.join(self.actionHistory[1:])
            x = self.makeContext2()
        return x

    def makeContext2(self):
        context2 = self.context2Introduction + '\n'
        context2 += 'ChatHistory: ' + self.chatHistory + '\n'
        context2 += 'EmotionHistory: ' + self.emotionHistory + '\n'
        context2 += 'BodyActHistory: ' + self.actionHistory + '\n'
        context2 += '!!!!!!!!Below is Your Output!!!!!!!!\n'
        context2 += 'Emotional: ...Fill out here.\n'
        context2 += 'BodyAct: ...Fill out here.\n'
        context2 += 'TxtOutput: ...Fill out here.\n'
        context2 += '-------------------------------\n'
        context2 += '!!!!!!!!Below is Your Output!!!!!!!!\n'
        return context2

    def interactive(self, x, username = 'User'):
        x = x.replace('\n', ' ')
        self.chatHistory += username + ': ' + x + '. '
        x = self.stepShrinkWithMakeContext()
        i = 0
        while(i < self.maxTry):
            try:
                res = self.gptdrv.forward(x).split('\n')
                #print(res)
                Emotional = res[0].split(': ')[1]
                Action = res[1].split(': ')[1]
                TxtOutput = '\n'.join(res[2:])
                TxtOutput = ''.join(TxtOutput.split(': ')[1:])
                self.emotionHistory += Emotional + ';'
                self.actionHistory += time.ctime().replace(' ', '_') + ' ' + Action + ';'
                if '\n' in TxtOutput:
                    self.chatHistory += self.name + ': ' + TxtOutput.replace('\n', '<br>') + '. '
                else:
                    self.chatHistory += self.name + ': ' + TxtOutput + '. '
                return Emotional, Action, TxtOutput
            except Exception as e:
                print('Emmmm GPT give a bad response ' + str(e) + str(res))
                i += 1
                time.sleep(5)
                continue
        return None
    
    def just_add_chat_history(self, x, username = 'User'):
        x = x.replace('\n', ' ')
        self.chatHistory += username + ': ' + x + '. '

if __name__ == '__main__':
    import json
    jsonparam = json.load(open('gpt3token.key', 'r'))
    myGPT = theGPT3(apiKey=jsonparam['key'], endpoint=jsonparam['endpoint'])
    #myGPT3.ask('Hello World!')
    while True:
        res = myGPT.interactive(input('Type something: '))
        print(res)