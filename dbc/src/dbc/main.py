import os 
from fastapi import FastAPI , Request , Response , Form 
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse 
from pathlib import Path
from dotenv import load_dotenv
from geopy.distance import geodesic 
from pydantic import BaseModel
import httpx

class CITY(BaseModel):
    city  : str

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent 
API_KEY = os.getenv("GEOCODING_API_KEY")
UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")



if not API_KEY:
    print("API KEY NOT FOUND")



app = FastAPI()

templates = Jinja2Templates(directory=str(BASE_DIR/"templates"))


async def get_lat_lon(city : CITY):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=3&appid={API_KEY}"
    
    
    async with httpx.AsyncClient() as client:
        try:
        
            response  = await client.get(url , timeout=5.0)
            response.raise_for_status()

            if response.status_code == 200:
                data = response.json()

                if not data :
                    return None

                lat = data[0]["lat"]
                lon = data[0]["lon"]

                return lat , lon

        except httpx.HTTPStatusError as e:
            return {
                "error": "Bad response",
                "status": e.response.status_code
            }

        except httpx.RequestError as e:
            return {
                "error": "Network problem",
                "message": str(e)
            }
    

\
@app.get("/" , response_class=HTMLResponse)
def Home(request : Request):
    return templates.TemplateResponse(
        "index.html" , 
        {"request" : request}
    )



@app.post("/distance" , response_class=HTMLResponse)
async def distance(request : Request , city1 : str = Form() , city2 :str =  Form() , unit : str = Form()):
    c1_geocode = await get_lat_lon(city1) 
    c2_geocode = await get_lat_lon(city2) 
    d_unit = unit 

    if d_unit == "km":
        distance = geodesic(c1_geocode , c2_geocode).km 
    elif d_unit == "mi":
        distance = geodesic(c1_geocode , c2_geocode).miles

    return templates.TemplateResponse(
        "index.html" , 
        {
            "request" : request , 
            "distance" : distance
        }
    )