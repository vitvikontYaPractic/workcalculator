from peewee import *


db = SqliteDatabase('database/date.db')


class BaseModel(Model):
    """Шаблон базовых моделей баз данных"""
    class Meta:
        database = db


class Product(BaseModel):
    """Конкретная модель базы данных"""
    class Meta:
        db_table = "Products"

    brigade = CharField(max_length=10)
    number = CharField(max_length=10)
    product = CharField(max_length=10)
    diameter_first = CharField(max_length=10)
    diameter_last = CharField(max_length=10)
    height = CharField(max_length=10)
    length = CharField(max_length=10)
    created = DateTimeField(
        constraints=[SQL("DEFAULT (datetime('now'))")])


if __name__ == "__main__":
    db.create_tables([Product])

