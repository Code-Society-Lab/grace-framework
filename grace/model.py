from sqlmodel import *
from sqlalchemy import Engine
from typing import TYPE_CHECKING, TypeVar, Type, List, Optional, Self, Any, Union
from sqlmodel.main import SQLModelMetaclass
from sqlalchemy.sql import ColumnElement

if TYPE_CHECKING:
    from sqlmodel.sql._expression_select_gen import Select, SelectOfScalar
    from sqlmodel import SQLModel, Session, select, func


T = TypeVar("T", bound="Model")


class Query:
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
        self.engine: Engine = model_class.get_engine()
        self.statement: Union[Select, SelectOfScalar] = select(model_class)

    def find(self, value: Any) -> Optional[T]:
        """
        Finds a record by its primary key (id only).

        Returns `None` if the record does not exist.

        ## Examples
        ```python
        user = User.find(1)
        ```
        """
        mapper = inspect(self.model_class)
        pk_columns = mapper.primary_key

        if not pk_columns:
            raise ValueError(f"No primary key defined for {self.model_class.__name__}")

        if len(pk_columns) > 1:
            raise ValueError("Composite primary keys are not yet supported")

        return self.where(pk_columns[0] == value).first()

    def find_by(self, **kwargs) -> Optional[T]:
        """
        Finds the first record matching the provided conditions.

        Equivalent to calling `.query().where(...).first()`.

        ## Examples
        ```python
        User.find_by(name="Alice")
        User.find_by(email="alice@example.com", active=True)
        ```
        """
        if not kwargs:
            raise ValueError("At least one keyword argument must be provided.")
        return self.where(**kwargs).first()

    def where(self, *conditions, **kwargs) -> Self:
        """
        Adds one or more filtering conditions to the query.

        Accepts both SQLAlchemy expressions (e.g. `User.age > 18`)
        and simple equality filters through keyword arguments.

        ## Examples
        ```python
        # Using SQLAlchemy expressions
        User.where(User.age > 18, User.active == True)

        # Using keyword arguments for equality
        User.where(name="Alice", active=True)

        # Equivalent: combines both styles
        User.where(User.age > 18, active=True)
        ```
        """
        for key, value in kwargs.items():
            column_ = getattr(self.model_class, key, None)
            if column_ is None:
                raise AttributeError(f"{self.model_class.__name__} has no column '{key}'")
            conditions += (column_ == value,)

        for condition in conditions:
            self.statement = self.statement.where(condition)
        return self

    def unique(self, column_: ColumnElement) -> Self:
        """
        Selects distinct values for a given column.

        Useful when you want to retrieve unique records or values.

        ## Examples
        ```python
        User.query().unique(User.email).all()
        ```
        """
        self.statement = select(
            distinct(column_)
        ).select_from(self.statement.subquery())
        return self

    def order_by(self, *args, **kwargs) -> Self:
        """
        Orders query results by one or more columns.

        Supports passing SQLAlchemy expressions directly,
        or using keyword arguments like `name="asc"` or `age="desc"`.

        ## Examples
        ```python
        User.order_by(User.name)
        User.order_by(User.created_at.desc())
        User.order_by(name="asc", age="desc")
        ```
        """
        for key, direction in kwargs.items():
            column_ = getattr(self.model_class, key, None)
            if column_ is None:
                raise AttributeError(f"{self.model_class.__name__} has no column '{key}'")

            if isinstance(direction, str):
                if direction.lower() == "asc":
                    args += (asc(column_),)
                elif direction.lower() == "desc":
                    args += (desc(column_),)
                else:
                    raise ValueError(f"Order direction for '{key}' must be 'asc' or 'desc'")
            else:
                # Allow passing SQLAlchemy ordering objects directly
                args += (direction,)

        if args:
            self.statement = self.statement.order_by(*args)
        return self

    def limit(self, count: int) -> Self:
        """
        Limits the number of results returned by the query.

        ## Examples
        ```python
        User.limit(10).all()
        ```
        """
        self.statement = self.statement.limit(count)
        return self

    def offset(self, count: int) -> Self:
        """
        Skips a given number of records before returning results.

        Useful for pagination.

        ## Examples
        ```python
        User.offset(20).limit(10).all()
        ```
        """
        self.statement = self.statement.offset(count)
        return self

    def all(self) -> List[T]:
        """
        Executes the query and returns all matching records as a list.

        ## Examples
        ```python
        users = User.where(User.active == True).all()
        ```
        """
        with Session(self.engine) as session:
            return list(session.exec(self.statement).all())

    def first(self) -> Optional[T]:
        """
        Executes the query and returns the first matching record.

        Returns `None` if no result is found.

        ## Examples
        ```python
        user = User.where(User.name == "Alice").first()
        ```
        """
        with Session(self.engine) as session:
            return session.exec(self.statement).first()

    def one(self) -> Type[T]:
        """
        Executes the query and returns exactly one result.

        Raises an exception if no result or multiple results are found.

        ## Examples
        ```python
        user = User.where(User.email == "alice@example.com").one()
        ```
        """
        with Session(self.engine) as session:
            return session.exec(self.statement).one()

    def count(self) -> int:
        """
        Returns the number of records matching the current query.

        ## Examples
        ```python
        total = User.where(User.active == True).count()
        ```
        """
        with Session(self.engine) as session:
            count_statement: SelectOfScalar[int] = select(func.count()).select_from(
                self.statement.subquery()
            )
            return session.exec(count_statement).one()


class _ModelMeta(SQLModelMetaclass):
    """
    Metaclass that enables class-level query delegation for models.

    It allows calling query methods directly on the model class
    (e.g. `User.where(...)` instead of `User.query().where(...)`).

    ## Examples
    ```python
    User.where(User.active == True).all()
    User.order_by(User.created_at.desc()).limit(5).all()
    ```
    """

    def __new__(cls, name, bases, namespace, **kwargs):
        """
        Initializes a new instance of the model.

        This method behaves like a regular class constructor,
        but exists explicitly here to avoid conflicts with query delegation.
        """
        if name != "Model":
            if "table" not in kwargs:
                kwargs["table"] = True
        return super().__new__(cls, name, bases, namespace, **kwargs)

    def __getattr__(cls, name: str):
        """
        Delegates missing class attributes or methods to the model's query object.

        When a method such as `where`, `order_by`, or `count` is not found on the model,
        this metaclass automatically forwards it to a `Query` instance.

        This allows expressive query syntax directly on the model.

        ## Examples
        ```python
        # Equivalent to: User.query().where(User.name == "Alice").first()
        user = User.where(User.name == "Alice").first()

        # Equivalent to: User.query().count()
        total = User.count()
        ```
        """
        if name.startswith("_") or name in {"get_engine", "set_engine", "query"}:
            raise AttributeError(name)

        query_instance = cls.query()
        if hasattr(query_instance, name):
            attr = getattr(query_instance, name)
            if callable(attr):
                def wrapper(*args, **kwargs):
                    return attr(*args, **kwargs)
                return wrapper
            return attr
        raise AttributeError(f"{cls.__name__} has no attribute '{name}'")


class Model(SQLModel, metaclass=_ModelMeta):
    _engine: Engine | None = None

    @classmethod
    def set_engine(cls, engine: Engine):
        """
        Sets the database engine used by the model.

        Must be called before performing any queries.

        ## Examples
        ```python
        from sqlmodel import create_engine
        engine = create_engine("sqlite:///db.sqlite3")
        User.set_engine(engine)
        ```
        """
        cls._engine = engine

    @classmethod
    def get_engine(cls) -> Engine:
        """
        Returns the engine currently associated with this model.

        Raises a `RuntimeError` if no engine has been set.

        ## Examples
        ```python
        engine = User.get_engine()
        ```
        """
        if cls._engine is None:
            raise RuntimeError(
                f"No session set for {cls.__name__}. Call Model.set_engine() first."
            )
        return cls._engine

    @classmethod
    def query(cls: Type[T]) -> Query:
        """
        Returns a new query object for the model.

        Enables chaining methods such as `where`, `order_by`, `limit`, etc.

        ## Examples
        ```python
        User.query().where(User.active == True).order_by(User.created_at).all()
        ```
        """
        return Query(cls)

    @classmethod
    def create(cls: Type[T], **kwargs) -> T:
        """
        Creates and saves a new record with the given attributes.

        ## Examples
        ```python
        User.create(name="Alice", email="alice@example.com")
        ```
        """
        instance = cls(**kwargs)
        return instance.save()

    def save(self: T) -> T:
        """
        Saves the current model instance to the database.

        Commits changes immediately and refreshes the instance.

        ## Examples
        ```python
        user = User(name="Alice")
        user.save()
        ```
        """
        with Session(self.get_engine()) as session:
            session.add(self)
            session.commit()
            session.refresh(self)
            return self

    def delete(self) -> None:
        """
        Deletes the current record from the database.

        ## Examples
        ```python
        user = User.find(1)
        user.delete()
        ```
        """
        with Session(self.get_engine()) as session:
            session.delete(self)
            session.commit()

    def update(self, **kwargs) -> Self:
        """
        Updates the current instance with the given attributes
        and saves the changes to the database.

        ## Examples
        ```python
        user = User.find(1)
        user.update(name="Alice Smith", active=False)
        ```
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self.save()
