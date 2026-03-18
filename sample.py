## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ## ctrl + A , then ctrl + / , to uncomment first. to avoid conflicts whole code is been commented
## %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# # for CLI project we can use requests to fecth api data
# # requests , geopy and dotenv are in pip. better copy the code and use it in other folder to avoid conflicts




# # method 1 : easiest method , using geopy module of python
# import requests 
# import os
# from dotenv import load_dotenv
# from geopy.distance import geodesic


# load_dotenv()

# API_KEY = os.getenv("GEOCODING_API_KEY")


# if not API_KEY:
#     print("API KEY NOT FOUND")

# c1 = input("Enter first city name: ")
# c2 = input("Enter second city name: ")






# def get_lat_lon(city):
#     url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=3&appid={API_KEY}"
#     try:
#         response = requests.get(url)
#         if response.status_code == 200 :
#             data = response.json()
#         else:
#             return {
#                 "status" : "error"
#             }
#     except requests.exceptions.RequestException as e:
#         print("Error" , e)
#         return None
    
#     lat = data[0]["lat"]
#     lon = data[0]["lon"]

#     return lat , lon 



# c1_geocode = get_lat_lon(c1)
# c2_geocode = get_lat_lon(c2)


# distance_with_module = geodesic(c1_geocode , c2_geocode).km 

# print(f"The distance between {c1} and {c2} is : {distance_with_module:.2f} km")



# #method 2 , getting distance from scratch 

# """
# DISTANCE CALCULATION FORMULA (Haversine)
# ---------------------------------------
# d = 2r * arcsin(sqrt(sin²(Δϕ/2) + cos(ϕ1) * cos(ϕ2) * sin²(Δλ/2)))

# Variables:
# - d: Distance between the two cities.
# - r: Radius of the Earth (approx. 6,371 km or 3,959 miles).   ||   r 
# - ϕ1, ϕ2: Latitude of city 1 and city 2 (in radians).         ||   c1_geocode and c2_geocode
# - Δϕ: Difference between the latitudes (ϕ2 - ϕ1).             ||   del_lat
# - Δλ: Difference between the longitudes (λ2 - λ1).            ||   del_lon
# """

# import math
# # 1. Radius of the Earth in km
# r = 6371  

# # 2. Extract coordinates from your geocode tuples
# lat1, lon1 = c1_geocode
# lat2, lon2 = c2_geocode

# # 3. CONVERT DEGREES TO RADIANS (CRITICAL STEP)
# # Math functions like sin/cos expect radians
# phi1, phi2 = math.radians(lat1), math.radians(lat2)
# lam1, lam2 = math.radians(lon1), math.radians(lon2)

# # 4. Calculate Differences
# del_phi = phi2 - phi1
# del_lam = lam2 - lam1

# # 5. The Haversine "a" term
# a = math.sin(del_phi / 2)**2 + \
#     math.cos(phi1) * math.cos(phi2) * \
#     math.sin(del_lam / 2)**2

# # 6. The central angle "c"
# # Use atan2 for better numerical stability than arcsin
# c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# # 7. Final Result
# distance_from_scratch = r * c

# print(f"Calculated from scratch: {distance_from_scratch:.2f} km")