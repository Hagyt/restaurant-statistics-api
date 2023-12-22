from geoalchemy2.functions import ST_DWithin, ST_GeomFromText
from sqlalchemy.exc import SQLAlchemyError

from src.domain.model import Restaurant
from src.external.persistence.models import RestaurantModel
from src.external.persistence.databases import sqlalchemy_db as db
from src.domain import INSIDE_CIRCLE_SEARCH


class SqlalchemyRestaurantRepository:
    base_class = RestaurantModel
    DEFAULT_NOT_FOUND_MESSAGE = "Restaurant model was not found"
    DEFAULT_PAGINATE = True
    DEFAULT_PER_PAGE = 10
    DEFAULT_PAGE = 1


    def create(self, data: dict) -> Restaurant:
        try:
            created_object = self.base_class(**data)
            db.session.add(created_object)
            db.session.commit()
            return created_object
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            raise Exception("Error creating object in database")


    def update(self, object_id: str, data: dict) -> Restaurant:
        try:
            update_object = self.get(object_id)
            update_object.update(db, data)
            return update_object
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception("Error updating object")


    def delete(self, object_id) -> Restaurant:
        try:
            delete_object = self.get(object_id)
            delete_object.delete(db)
            return delete_object
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception("Error deleting object")
        

    def get_all(self, query_params=None) -> dict:
        try:
            query_set = self.base_class.query

            if query_params is not None:
                query_set = self._apply_query_params(query_set, query_params)

            return self.create_pagination(query_params, query_set)
        except SQLAlchemyError as e:
            print(e)
            raise Exception("Error getting all objects")
    

    def get(self, object_id):
            return self.base_class.query.filter_by(id=object_id) \
                .first_or_404(self.DEFAULT_NOT_FOUND_MESSAGE)
    

    def _apply_query_params(self, query, query_params):
        function_query_param = query_params.get("function")

        if function_query_param == INSIDE_CIRCLE_SEARCH:
            radius_query_param = query_params.get("radius")
            center_query_param = query_params.get("center_point")
            postgis_point = ST_GeomFromText(f"SRID=4326;{center_query_param.wkt}")
            query = query.filter(
                ST_DWithin(self.base_class._geom, postgis_point, radius_query_param)
            )
        return query


    def create_pagination(self, query_params, query_set):
        if query_params is None:
            query_params = {}

        paginate = query_params.get("PAGINATE", self.DEFAULT_PAGINATE)

        if not paginate:
            return query_set.all()
        page = query_params.get("PAGE", self.DEFAULT_PAGE)
        per_page = query_params.get(
            "PER_PAGE", self.DEFAULT_PER_PAGE
        )

        try:
            page = int(page)
        except ValueError:
            page = self.DEFAULT_PAGE

        try:
            per_page = int(per_page)
        except ValueError:
            per_page = self.DEFAULT_PER_PAGE

        paginated = query_set.paginate(page=int(page), per_page=int(per_page))
        return {
            'total': paginated.total,
            'page': paginated.page,
            'per_page': paginated.per_page,
            'items': paginated.items,
        }