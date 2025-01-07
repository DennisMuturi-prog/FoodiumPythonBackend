import aiohttp
import asyncio
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import re
import json

# List of URLs to fetch data from


async def fetch(session,searchParams):
    """
    Asynchronously fetches the content from a given URL using the provided session.
    """
    url=f"https://glovoapp.com/ke/en/nairobi/{searchParams['store']}-nbo?search={searchParams['name']}"
    async with session.get(url) as response:
        content = await response.text()
        # print(f"Fetched URL: {url}")
        return content

def parse(html):
    soup = BeautifulSoup(html, "lxml")
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
    allIngredientsInfo=[]
    for item in ingredientsInfo:
        try:
            info={
                "name":item['data']['name'],
                "imageUrl":item['data']['imageUrl'],
                "price":item['data']['price']
            }
            allIngredientsInfo.append(info)
        except Exception as e:
            print(f"error in parser:{e} {item['data']['name']}")
            continue
    return allIngredientsInfo

async def main(items):
    """
    Main function to fetch URLs concurrently and parse their HTML content.
    """
    results=[]
    async with aiohttp.ClientSession() as session:
        # Create a list of tasks for fetching URLs
        tasks = [fetch(session, url) for url in items]
        # Gather all responses concurrently
        htmls = await asyncio.gather(*tasks)

        # Use ThreadPoolExecutor to parse HTML content in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            results=list(executor.map(parse, htmls))
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
    final=asyncio.run(main(items))
    print('result:',final)