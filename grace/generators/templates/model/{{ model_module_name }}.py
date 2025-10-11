from grace.model import Model, Field


class {{ model_name | to_camel }}(Model):
    id: int | None = Field(default=None, primary_key=True)
    {{ model_columns | join('\n    ') }}
