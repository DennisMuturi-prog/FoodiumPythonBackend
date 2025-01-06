from fastapi import FastAPI
from ML_and_Data_Science.glovo_pricing import getItemsPrices,PriceRequest
# from .ML_and_Data_Science.food_recommendation import makePrediction
from ML_and_Data_Science.nutrient_values import testing
from fastapi import HTTPException

# class PriceRequest(BaseModel):
#     items:list[str]
#     store:str

app=FastAPI()

@app.get("/")
def getItems():
    testingo=testing()
    print(testingo)
    return list(testingo)

@app.post("/pricing")
async def getPricesInfo(ingredients:PriceRequest):
    try:
        response=await getItemsPrices(ingredients)
        return response
    except:
        raise HTTPException(status_code=404, detail="Items not found")

# @app.post("/recommendation")
# async def getRecommendations(ingredients:list[str]):
#     try:
#         response=makePrediction(ingredients)
#         return response
#     except Exception:
#         raise HTTPException(status_code=404, detail="predictions for recommendations failed")
        
        
        
        
    
