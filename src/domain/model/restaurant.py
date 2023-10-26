from dataclasses import dataclass

@dataclass
class Restaurant:
    
    id: str = None
    rating: int 
    name: str 
    site: str   
    email: str 
    phone: str 
    street: str 
    city: str
    state: str 
    lat: float 
    lng: float 
