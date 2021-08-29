# bson
import bson

class Restaurant(object):

    id = None

    def __init__(self, rating: str, name: str, site: str,
                 email: str, phone: str, street: str, city: str,
                 state: str, lat: float, lng: float, id: str=None) -> None:
        self.id = id
        self.rating = rating
        self.name = name
        self.site = site
        self.email = email
        self.phone = phone
        self.street = street
        self.city = city
        self.state = state
        self.lat = lat
        self.lng = lng

    def set_generated_id(self) -> None:
        generated_id = bson.objectid.ObjectId()
        self.id = str(generated_id)
