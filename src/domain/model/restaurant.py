class Restaurant:

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

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"id='{self.id}', "
            f"rating='{self.rating}', "
            f"name='{self.name}', "
            f"site='{self.site}', "
            f"email='{self.email}', "
            f"phone='{self.phone}', "
            f"street='{self.street}', "
            f"city='{self.city}', "
            f"state='{self.state}', "
            f"lat='{self.lat}', "
            f"lng='{self.lng}',)"
        )