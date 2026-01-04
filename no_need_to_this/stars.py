from fastapi import APIRouter 
import requests

router = APIRouter(prefix='/stars',tags={"stars"})

API_KEY = "VjvXklMTSYwENfd+XvOH4Q==HLVgfWvrGCaWcS7Z"


@router.get('/{star_name}')
def get_star(star_name:str):
    API_URL = f'https://api.api-ninjas.com/v1/stars?name={star_name}'
    headers = {"X-Api-Key": API_KEY}  
    response = requests.get(API_URL,headers=headers)
    data = response.json()
    return data  
