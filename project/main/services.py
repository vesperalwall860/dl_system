from flask_servicelayer import SQLAlchemyService

from .. import db, models


class ExtFuncsMixin(object):
    def __init__(self):
        self.columns = self.__model__.columns()

    @staticmethod
    def prepare_pagination(items):
        # pagination
        pagination = items.paginate(per_page=10)

        page = request.args.get('page')

        # if some page is chosen otherwise than the first
        if page or pagination.pages > 1:
            try:
                page = int(page)
            except (ValueError, TypeError):
                page = 1
            items = items.paginate(page=page, per_page=10).items

        return (pagination, items)


class UserService(ExtFuncsMixin, SQLAlchemyService):
    __model__ = models.User
    __db__ = db