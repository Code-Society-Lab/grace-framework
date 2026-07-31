# Model

`Model` is the ActiveRecord-style base class every generated model subclasses. It combines [SQLModel](https://sqlmodel.tiangolo.com/) with a fluent [`Query`](#grace.model.Query) builder, accessible both from instances (`task.save()`) and directly on the class (`Task.where(...)`) via the `_ModelMeta` metaclass.

```python
from typing import Optional
from grace.model import Field, Model


class User(Model):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    age: int
    active: bool = True


user = User.create(name="Test", email="test@example.com", age=20)
User.find(1)
User.find_by(name="Alice")
User.where(User.age > 25, active=True).order_by(User.age.desc()).limit(10).all()
User.with_("posts", "comments").where(User.active == True).all()
```

See [Models & Migrations](../guides/models.md) for the full guide.

::: grace.model.Model

::: grace.model.Query
