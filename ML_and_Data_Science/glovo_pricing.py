from bs4 import BeautifulSoup
import requests
import re
import json
from pydantic import BaseModel
import time

class PriceRequest(BaseModel):
    items:list[str]
    store:str
session = requests.Session()

def getPriceInfo(store:str,searchWord:str):
    try:
        start=time.time()
        url=f"https://glovoapp.com/ke/en/nairobi/{store}-nbo?search={searchWord}"
        page=session.get(url)
        print(time.time()-start)
        soup = BeautifulSoup(page.content, 'lxml')
        ingredientsPart=soup.find_all('script')[9].text
        print(time.time()-start)
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

def getItemsPrices(ingredients:PriceRequest):
    response={}
    for ingredient in ingredients['items']:
        info=getPriceInfo(ingredients['store'],ingredient)
        ingredientPriceInfo=[]
        for item in info:
            try:
                parsedInfo={
                    "name":item['data']['name'],
                    "imageUrl":item['data']['imageUrl'],
                    "price":item['data']['price']
                }
                ingredientPriceInfo.append(parsedInfo)
            except Exception as e:
                continue       
        response[ingredient]=ingredientPriceInfo
    return response

if __name__=='__main__':
    # cProfile.run("getPriceInfo('naivas','milk')")
    goods={
        'store':'',
        'items':''
    }
    goods['store']='naivas'
    goods['items']=['pen','book','pencil']
    
    getItemsPrices(goods)
    
def getPriceInfo(store:str,searchWord:str):
    try:
        start=time.time()
        url=f"https://glovoapp.com/ke/en/nairobi/{store}-nbo?search={searchWord}"
        page=session.get(url)
        print(time.time()-start)
        soup = BeautifulSoup(page.content, 'lxml')
        ingredientsPart=soup.find_all('script')[9].text
        print(time.time()-start)
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
    
    
    
    