from fastapi import FastAPI
from ML_and_Data_Science.glovo_pricing import getPriceInfo
from ML_and_Data_Science.food_recommendation import makePrediction
# from ML_and_Data_Science.nutrient_values import testing
from fastapi import HTTPException
from pydantic import BaseModel

class PriceRequest(BaseModel):
    names:list[str]
    store:str
class RecommendationRequest(BaseModel):
    names:list[str]
    store:str

app=FastAPI()

# @app.get("/")
# def getItems():
#     testingo=testing()
#     print(testingo)
#     return list(testingo)
@app.get("/")
def testing():
    return ['hello','people']
@app.post("/pricing")
async def getPricesInfo(ingredients:PriceRequest):
    try:
        # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        # response= asyncio.run(main(ingredients))
        response= await getPriceInfo(ingredients)
        return response
    except Exception as e:
        print('ERROR:',e)
        raise HTTPException(status_code=404, detail="Items not found")

    
    
@app.post("/recommendation")
async def getRecommendations(ingredients:list[str]):
    print(ingredients)
    try:
        response=makePrediction(ingredients)
        return response
    except Exception:
        raise HTTPException(status_code=404, detail="predictions for recommendations failed")
        
        
        
        
    
