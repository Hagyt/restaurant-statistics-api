from .restaurant import blueprint as restaurant_blueprint


def setup_blueprints(app) -> None:
    app.register_blueprint(restaurant_blueprint)
    return app


__all__ = ["setup_blueprints"]