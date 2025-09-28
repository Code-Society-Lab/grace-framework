from sqlmodel import *
from sqlalchemy import Engine
from typing import TypeVar, Type, List, Optional, Any

# Type variable for proper type hints
T = TypeVar('T', bound='Model')

class _ModelMeta(type(SQLModel)):
    """Metaclass to make table=True the default"""

    def __new__(cls, name, bases, namespace, **kwargs):
        if name != 'Model':
            if 'table' not in kwargs:
                kwargs['table'] = True
        return super().__new__(cls, name, bases, namespace, **kwargs)


class Model(SQLModel, metaclass=_ModelMeta):
    _engine: Engine = None

    @classmethod
    def set_engine(cls, engine: Engine):
        """Set the database engine for all models"""
        cls._engine = engine

    @classmethod
    def create(cls: Type[T], **kwargs) -> T:
        """Create and save a new record"""
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def where(cls: Type[T], *conditions) -> 'QueryBuilder[T]':
        """Start a query with WHERE conditions"""
        return QueryBuilder(cls).where(*conditions)

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        """Get all records"""
        return QueryBuilder(cls).all()

    @classmethod
    def first(cls: Type[T]) -> Optional[T]:
        """Get first record"""
        return QueryBuilder(cls).first()

    @classmethod
    def find(cls: Type[T], id: Any) -> Optional[T]:
        """Find by primary key"""
        with Session(cls._engine) as session:
            return session.get(cls, id)

    def save(self: T) -> T:
        """Save the current instance to database"""
        with Session(self._engine) as session:
            session.add(self)
            session.commit()
            session.refresh(self)
            return self

    def delete(self) -> None:
        """Delete the current instance from database"""
        with Session(self._engine) as session:
            # Get the instance from the session
            instance = session.get(self.__class__, self.id)
            if instance:
                session.delete(instance)
                session.commit()

    def update(self, **kwargs) -> 'Model':
        """Update instance attributes and save"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self.save()


class QueryBuilder:
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
        self.statement = select(model_class)

    def where(self, *conditions) -> 'QueryBuilder[T]':
        for condition in conditions:
            self.statement = self.statement.where(condition)
        return self

    def limit(self, count: int) -> 'QueryBuilder[T]':
        self.statement = self.statement.limit(count)
        return self

    def offset(self, count: int) -> 'QueryBuilder[T]':
        self.statement = self.statement.offset(count)
        return self

    def order_by(self, *columns) -> 'QueryBuilder[T]':
        self.statement = self.statement.order_by(*columns)
        return self

    def all(self) -> List[T]:
        """Execute query and return all results"""
        with Session(self.model_class._engine) as session:
            return list(session.exec(self.statement).all())

    def first(self) -> Optional[T]:
        """Execute query and return first result"""
        with Session(self.model_class._engine) as session:
            return session.exec(self.statement).first()

    def one(self) -> T:
        """Execute query and return exactly one result"""
        with Session(self.model_class._engine) as session:
            return session.exec(self.statement).one()

