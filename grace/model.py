from sqlmodel import *
from typing import TYPE_CHECKING, TypeVar, Type, List, Optional, Self, Any, Union
from sqlmodel.main import SQLModelMetaclass

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
        self.session: Session = model_class.get_session()
        self.statement: Union[Select, SelectOfScalar] = select(model_class)

    def where(self, *conditions) -> Self:
        for condition in conditions:
            self.statement = self.statement.where(condition)
        return self

    def limit(self, count: int) -> Self:
        self.statement = self.statement.limit(count)
        return self

    def offset(self, count: int) -> Self:
        self.statement = self.statement.offset(count)
        return self

    def order_by(self, *columns) -> Self:
        self.statement = self.statement.order_by(*columns)
        return self

    def all(self) -> List[T]:
        return list(self.session.exec(self.statement).all())

    def first(self) -> Optional[T]:
        return self.session.exec(self.statement).first()

    def one(self) -> Type[T]:
        return self.session.exec(self.statement).one()

    def count(self) -> int:
        count_statement: SelectOfScalar[int] = select(func.count()).select_from(
            self.statement.subquery()
        )
        return self.session.exec(count_statement).one()


class Model(SQLModel, metaclass=_ModelMeta):
    _session: Session | None = None

    @classmethod
    def set_session(cls, session: Session):
        cls._session = session

    @classmethod
    def get_session(cls) -> Session:
        """Get the current session"""
        if cls._session is None:
            raise RuntimeError(
                f"No session set for {cls.__name__}. Call Model.set_session() first."
            )
        return cls._session

    @classmethod
    def create(cls: Type[T], **kwargs) -> T:
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def where(cls: Type[T], *conditions) -> Query:
        return Query(cls).where(*conditions)

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        return Query(cls).all()

    @classmethod
    def first(cls: Type[T]) -> Optional[T]:
        return Query(cls).first()

    @classmethod
    def find(cls: Type[T], id_: Any) -> Optional[T]:
        return cls.get_session().get(cls, id_)

    @classmethod
    def count(cls: Type[T]) -> int:
        return Query(cls).count()

    def save(self: T) -> T:
        self.get_session().add(self)
        self.get_session().commit()
        self.get_session().refresh(self)
        return self

    def delete(self) -> None:
        self.get_session().delete(self)
        self.get_session().commit()

    def update(self, **kwargs) -> Self:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self.save()
