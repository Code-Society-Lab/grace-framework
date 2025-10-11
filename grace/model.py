from sqlmodel import *
from sqlalchemy import Engine
from typing import TYPE_CHECKING, TypeVar, Type, List, Optional, Self, Any, Union
from sqlmodel.main import SQLModelMetaclass
from sqlalchemy.sql import ColumnElement

if TYPE_CHECKING:
    from sqlmodel.sql._expression_select_gen import Select, SelectOfScalar
    from sqlmodel import SQLModel, Session, select, func


T = TypeVar("T", bound="Model")


class _ModelMeta(SQLModelMetaclass):
    """Metaclass to make table=True the default"""

    def __new__(cls, name, bases, namespace, **kwargs):
        if name != "Model":
            if "table" not in kwargs:
                kwargs["table"] = True
        return super().__new__(cls, name, bases, namespace, **kwargs)


class Query:
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
        self.engine: Engine = model_class.get_engine()
        self.statement: Union[Select, SelectOfScalar] = select(model_class)

    def where(self, *conditions) -> Self:
        for condition in conditions:
            self.statement = self.statement.where(condition)
        return self

    def unique(self, column_: ColumnElement) -> Self:
        self.statement = select(
            distinct(column_)
        ).select_from(self.statement.subquery())
        return self

    def order_by(self, *args, **kwargs) -> Self:
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
        self.statement = self.statement.limit(count)
        return self

    def offset(self, count: int) -> Self:
        self.statement = self.statement.offset(count)
        return self

    def all(self) -> List[T]:
        with Session(self.engine) as session:
            return list(session.exec(self.statement).all())

    def first(self) -> Optional[T]:
        with Session(self.engine) as session:
            return session.exec(self.statement).first()

    def one(self) -> Type[T]:
        with Session(self.engine) as session:
            return session.exec(self.statement).one()

    def count(self) -> int:
        with Session(self.engine) as session:
            count_statement: SelectOfScalar[int] = select(func.count()).select_from(
                self.statement.subquery()
            )
            return session.exec(count_statement).one()


class Model(SQLModel, metaclass=_ModelMeta):
    _engine: Engine | None = None

    @classmethod
    def set_engine(cls, engine: Engine):
        cls._engine = engine

    @classmethod
    def get_engine(cls) -> Engine:
        """Get the current session"""
        if cls._engine is None:
            raise RuntimeError(
                f"No session set for {cls.__name__}. Call Model.set_engine() first."
            )
        return cls._engine

    @classmethod
    def query(cls: Type[T]) -> Query:
        return Query(cls)

    @classmethod
    def where(cls: Type[T], *conditions) -> Query:
        return cls.query().where(*conditions)

    @classmethod
    def unique(cls, column_: ColumnElement) -> Query:
        return cls.query().unique(column_)

    @classmethod
    def order_by(cls, *args, **kwargs) -> Query:
        return cls.query().order_by(*args, **kwargs)

    @classmethod
    def find(cls: Type[T], id_: Any) -> Optional[T]:
        with Session(cls.get_engine()) as session:
            return session.get(cls, id_)

    @classmethod
    def find_by(cls: Type[T], **kwargs) -> Optional[T]:
        if not kwargs:
            raise ValueError("At least one keyword argument must be provided.")

        with Session(cls.get_engine()) as session:
            query = select(cls)

            for key, value in kwargs.items():
                column_ = getattr(cls, key, None)

                if column_ is None:
                    raise AttributeError(f"{cls.__name__} has no column '{key}'")
                query = query.where(column_ == value)

            return session.exec(query).first()

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        return cls.query().all()

    @classmethod
    def first(cls: Type[T]) -> Optional[T]:
        return cls.query().first()

    @classmethod
    def count(cls: Type[T]) -> int:
        return cls.query().count()

    @classmethod
    def create(cls: Type[T], **kwargs) -> T:
        instance = cls(**kwargs)
        return instance.save()

    def save(self: T) -> T:
        with Session(self.get_engine()) as session:
            session.add(self)
            session.commit()
            session.refresh(self)
            return self

    def delete(self) -> None:
        with Session(self.get_engine()) as session:
            session.delete(self)
            session.commit()

    def update(self, **kwargs) -> Self:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self.save()
