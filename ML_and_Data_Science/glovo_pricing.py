from bs4 import BeautifulSoup
import requests
import re
import json
import pprint

def getPriceInfo(store:str,searchWord:str):
    url=f"https://glovoapp.com/ke/en/nairobi/{store}-nbo?search={searchWord}"
    page=requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
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
    pprint.pprint(ingredientsInfo)
    print(ingredientsInfo[0]['data']['name'])


getPriceInfo('quickmart','milk')
    
    
    
    
    