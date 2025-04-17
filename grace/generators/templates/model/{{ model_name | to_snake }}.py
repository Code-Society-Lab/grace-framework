from sqlalchemy import Column, Integer{{ ", {}".format(','.join(model_column_types)) }}
from bot import app
from grace.model import Model


class {{ model_name | to_camel }}(app.base, Model):
    __tablename__ = "{{ model_name | to_snake | pluralize }}"

    id = Column(Integer, primary_key=True)
    {{ model_columns | join('\n    ') }}
