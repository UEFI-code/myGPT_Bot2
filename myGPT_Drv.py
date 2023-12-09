# This driver aimed to not using openai libary, but using requests libary to call openai API directly.
import requests
import json

class GPT3_Drv:
    def __init__(self, endpoint="https://mygpt233.openai.azure.com/openai/deployments/myGPT3/completions?api-version=2022-12-01", apiKey="233333"):
        self.endpoint = endpoint
        self.header = {
            "Content-Type": "application/json",
            "api-key": apiKey
        }
        self.body = {
            "prompt": "Hello World",
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "stop": None
        }
    
    def forward(self, x = 'Hello World'):
        self.body['prompt'] = x
        self.body['max_tokens'] = 4000 - len(x)
        if (self.body['max_tokens'] < 0):
            raise Exception('The input text is too long.')
        response = requests.post(self.endpoint, headers=self.header, data=json.dumps(self.body))
        return response.json()['choices'][0]['text']

class chat_Drv:
    def __init__(self, endpoint="https://mygpt233.openai.azure.com/openai/deployments/myGPTChat_3_5/chat/completions?api-version=2023-03-15-preview", apiKey="233333"):
        self.endpoint = endpoint
        self.header = {
            "Content-Type": "application/json",
            "api-key": apiKey
        }
        self.messages = [{"role":"system","content":"You are a smart robot girl, and help user practice Japanese now."}]
        self.body = {
            "messages": None,
            "max_tokens": 256,
            "temperature": 0.7,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "stop": None
        }
    
    def forward(self, x = 'Hello World'):
        x = x[-3800:]
        self.body['messages'] = self.messages + [{"role":"user","content":x}]
        self.body['max_tokens'] = 3900 - len(x)
        if (self.body['max_tokens'] < 0):
            raise Exception('The input text is too long.')
        response = requests.post(self.endpoint, headers=self.header, data=json.dumps(self.body))
        return response.json()['choices'][0]['message']['content']

class GPT4_Drv:
    def __init__(self, endpoint="https://mygpt233.openai.azure.com/openai/deployments/myGPT4_32K/chat/completions?api-version=2023-03-15-preview", apiKey="233333", maxTokens = 8000):
        self.endpoint = endpoint
        self.header = {
            "Content-Type": "application/json",
            "api-key": apiKey
        }
        self.messages = [{"role":"system","content":"You are a smart robot girl."}]
        self.body = {
            "messages": None,
            "max_tokens": 2048,
            "temperature": 0.7,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "stop": None
        }
        self.maxTokens = maxTokens

    def forward(self, x = 'Hello World'):
        x = x[-(self.maxTokens - 100):]
        self.body['messages'] = self.messages + [{"role":"user","content":x}]
        self.body['max_tokens'] = self.maxTokens - len(x)
        if (self.body['max_tokens'] < 0):
            raise Exception('The input text is too long.')
        response = requests.post(self.endpoint, headers=self.header, data=json.dumps(self.body))
        try:
            return response.json()['choices'][0]['message']['content']
        except:
            return 'Net Error ' + str(response)
    
if __name__ == '__main__':
    #gpt3 = GPT3_Drv(apiKey=open('azgpt3.key', 'r').readline())
    #print(gpt3.forward('Hello World'))
    # chatgpt = GPT4_Drv(apiKey=open('azgpt3.key', 'r').readline())
    # print(chatgpt.forward('Hello World'))
    # chatgpt = chat_Drv(apiKey=open('azgpt3.key', 'r').readline())
    # print(chatgpt.forward('Hello World'))
    import json
    jsonparam = json.load(open('gpt4token.key', 'r'))
    gpt4 = GPT4_Drv(apiKey=jsonparam['key'], endpoint=jsonparam['endpoint'])
    print(gpt4.forward('Hello World'))
