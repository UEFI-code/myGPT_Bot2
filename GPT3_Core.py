import os
import openai

class theGPT3():
    def __init__(self, apiKey, maxTokens):
        openai.api_key = apiKey
        self.maxTokens = maxTokens
        self.context = ''

    def contextSpace(self):
        if(len(self.context) > self.maxTokens - 100):
            exceedNum = len(self.context) - (self.maxTokens - 100)
            self.context = self.context[exceedNum:]

    def ask(self, x):
        if x[-2:] != '\n\n':
            if x[-1] == '\n':
                x += '\n'
            else:
                x += '\n\n'
        self.context += x
        self.contextSpace()
        response = openai.Completion.create(model="text-davinci-003",prompt=self.context,temperature=0.7,max_tokens=self.maxTokens,top_p=1,frequency_penalty=0,presence_penalty=0)
        res = response['choices'][0].text
        try:
            while res[0] == '\n':
                res = res[1:]
            if(res[-2:] != '\n\n'):
                if res[-1] == '\n':
                    self.context += (res + '\n')
                else:
                    self.context += (res + '\n\n')
            else:
                self.context += res
        except:
            pass
        return res