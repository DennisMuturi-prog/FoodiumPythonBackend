from fastapi import FastAPI
# from ML_and_Data_Science.glovo_pricing import getItemsPrices,PriceRequest,getPriceInfo
# from ML_and_Data_Science.food_recommendation import makePrediction
# from ML_and_Data_Science.nutrient_values import testing
from tester import main
from fastapi import HTTPException
from pydantic import BaseModel
import asyncio

class PriceRequest(BaseModel):
    name:str
    store:str

app=FastAPI()

# @app.get("/")
# def getItems():
#     testingo=testing()
#     print(testingo)
#     return list(testingo)

@app.post("/pricing")
async def getPricesInfo(ingredients:list[PriceRequest]):
    try:
        # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        # response= asyncio.run(main(ingredients))
        ingredients_dict = [ingredient.model_dump() for ingredient in ingredients]
        print(ingredients_dict)
        response= await main(ingredients_dict)
        return response
    except Exception as e:
        print('ERROR:',e)
        raise HTTPException(status_code=404, detail="Items not found")

    
    
# @app.post("/recommendation")
# async def getRecommendations(ingredients:list[str]):
#     try:
#         response=makePrediction(ingredients)
#         return response
#     except Exception:
#         raise HTTPException(status_code=404, detail="predictions for recommendations failed")
        
        
        
        
    
