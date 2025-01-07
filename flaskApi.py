from flask import Flask,request
# from ML_and_Data_Science.glovo_pricing import getPriceInfo
from bs4 import BeautifulSoup
import requests
import re
import json
import time
from tester import main
import asyncio


app = Flask(__name__)



@app.route('/',methods=['POST'])
def hello():
    print(request.json)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    res=asyncio.run(main(request.json))
    return res

def getPriceInfo(store:str,searchWord:str):
    try:
        start=time.time()
        url=f"https://glovoapp.com/ke/en/nairobi/{store}-nbo?search={searchWord}"
        page=requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')
        ingredientsPart=soup.find_all('script')[9].text
        ingredientsInfo = re.search(r'data:\{title:".*?",.*?elements:\[(.*?)\]\}', ingredientsPart, flags=re.S).group(1)
        ingredientsInfo = re.sub(r'(\d+)n', r'\1', ingredientsInfo)
        ingredientsInfo = ingredientsInfo.replace('https:', 'PLACEHOLDER_HTTPS')
        ingredientsInfo = ingredientsInfo.replace('dh:', 'PLACEHOLDER_DH')
        ingredientsInfo = re.sub(r'(\w+):', r'"\1":', ingredientsInfo)
        ingredientsInfo = f"[{ingredientsInfo}]"
        ingredientsInfo = ingredientsInfo.replace('PLACEHOLDER_HTTPS', 'https:')
        ingredientsInfo = ingredientsInfo.replace('PLACEHOLDER_DH', 'dh:')
        ingredientsInfo = json.loads(ingredientsInfo)
        print(ingredientsInfo[0])
        print(time.time()-start)
        
        return ingredientsInfo
    except Exception as e:
        print('error',e)
        return