from fastapi import APIRouter
import requests


API_KEY = "VjvXklMTSYwENfd+XvOH4Q==HLVgfWvrGCaWcS7Z"
router = APIRouter(prefix='/planets',tags={"planets"})

@router.get('/{planet_name}')
def get_planet(planet_name:str):
    API_URL = f'https://api.api-ninjas.com/v1/planets?name={planet_name}'
    headers = {"X-Api-Key": API_KEY}  
    response = requests.get(API_URL,headers=headers)
    data = response.json()
    return data

