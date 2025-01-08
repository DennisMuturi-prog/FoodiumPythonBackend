import aiohttp
import asyncio
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import re
import json



async def fetch(session,store,itemName):
    """
    Asynchronously fetches the content from a given URL using the provided session.
    """
    url=f"https://glovoapp.com/ke/en/nairobi/{store}-nbo?search={itemName}"
    async with session.get(url) as response:
        content = await response.text()
        # print(f"Fetched URL: {url}")
        return {
            "htmlContent":content,
            "itemName":itemName   
        }

def parse(fetchResponse):
    soup = BeautifulSoup(fetchResponse['htmlContent'], "lxml")
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
    allIngredientsInfo={
        "itemName":fetchResponse['itemName'],
        "foundItems":[]
    }
    for item in ingredientsInfo:
        try:
            info={
                "name":item['data']['name'],
                "imageUrl":item['data']['imageUrl'],
                "price":item['data']['price']
            }
            allIngredientsInfo['foundItems'].append(info)
        except Exception as e:
            print(f"error in parser:{e} {item['data']['name']}")
            continue
    return allIngredientsInfo

async def getPriceInfo(items):
    """
    Main function to fetch URLs concurrently and parse their HTML content.
    """
    results=[]
    async with aiohttp.ClientSession() as session:
        # Create a list of tasks for fetching URLs
        tasks = [fetch(session,items.store, url) for url in items.names]
        # Gather all responses concurrently
        fetchResponses = await asyncio.gather(*tasks)

        # Use ThreadPoolExecutor to parse HTML content in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            results=list(executor.map(parse, fetchResponses))
    return results

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    items = [
    {
        "name":'potato',
        "store":'naivas'
    },
    {
        "name":'beans',
        "store":'naivas'
    },
    {
        "name":'flour',
        "store":'naivas'
    },
    
    
    ] 
    final=asyncio.run(getPriceInfo(items))
    print('result:',final)