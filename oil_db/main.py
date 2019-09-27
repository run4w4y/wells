from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from sqlalchemy.dialects.postgresql import ARRAY as Array
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from .exceptions import *

_Base = declarative_base()
_Session = sessionmaker()
_db_session = None


class db_sync:
    def __init__(
        self,
        f
    ):
        self.f = f
    
    def __call__(
        self,
        init_self,
        *args,
        **kwargs
    ):
        self.f(init_self, *args, **kwargs)
        assert _db_session is not None
        _db_session.add(init_self)
        _db_session.commit()


class LayerProperties(_Base):
    __tablename__ = 'layer_properties'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    color = Column(String)
    translation = Column(String)
    layers = relationship('Layer', uselist=True, back_populates='properties') 

    @db_sync
    def __init__(
        self, 
        name, 
        color, 
        translation
    ):
        self.name = name
        self.color = color
        self.translation = translation
    
    @classmethod
    def from_name(
        cls, 
        name
    ):
        search = list(_db_session.query(cls).filter_by(name=name))
        if not search:
            raise LayerTypeNotFound('layer with name {} couldnt be found'.format(name))
        
        return search[0]

    def __repr__(self): 
        return '<WellType(id={}, name={}, color={}, trans={})>'.format(
            self.id,
            self.name,
            self.color,
            self.translation
        )


class Layer(_Base):
    __tablename__ = 'layers'
    id = Column(Integer, primary_key=True)
    d_from = Column(Integer)
    d_to = Column(Integer)
    properies_id = Column(Integer, ForeignKey('layer_properties.id'))
    properties = relationship('LayerProperties', back_populates='layers')
    well_id = Column(Integer, ForeignKey('wells.id'))
    well = relationship('Well', uselist=False, back_populates='layers')

    @db_sync
    def __init__(
        self, 
        prop_name, 
        d_from, 
        d_to
    ):
        self.d_from = d_from
        self.d_to = d_to
        self.properties = LayerProperties.from_name(prop_name)
    
    @classmethod
    def from_prop_id(
        cls,
        prop_id,
        d_from,
        d_to
    ):
        return cls(
            _db_session.query(LayerProperties).filter_by(id=prop_id).first().name,
            d_from,
            d_to
        )

    def __repr__(self):
        return '<Layer(id={}, from={}, to={}, prop={}>'.format(
            self.id,
            self.d_from,
            self.d_to,
            self.properties
        )


class WellType(_Base):
    __tablename__ = 'well_types'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    wells = relationship('Well', uselist=True, back_populates='well_type')

    @db_sync
    def __init__(
        self,
        name
    ):
        self.name = name

    @classmethod
    def from_name(
        cls, 
        name
    ):
        search = list(_db_session.query(cls).filter_by(name=name))
        if not search:
            raise WellTypeNotFound('layer with name {} couldnt be found'.format(name))
        
        return search[0]

    def __repr__(self): 
        return '<WellType(id={}, name={})>'.format(
            self.id,
            self.name
        )


class Well(_Base):
    __tablename__ = 'wells'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    capacity = Column(Integer)
    depth = Column(Integer)
    well_type_id = Column(Integer, ForeignKey('well_types.id'))
    well_type = relationship('WellType', uselist=False, back_populates='wells')
    layers = relationship('Layer', uselist=True, back_populates='well')

    # each layer format: { 'name': str, 'from': int, 'to': int } 
    @db_sync
    def __init__(
        self, 
        name, 
        type_name,
        capacity,
        depth, 
        layers
    ):
        self.name = name
        self.well_type = WellType.from_name(type_name)
        self.capacity = capacity
        self.depth = depth
        self.layers = list(map(lambda x: Layer.from_prop_id(x['id'], x['from'], x['to']), layers))

    def __repr__(self):
        return '<Well(id={}, capacity={}, depth={} type={}, layers={})>'.format(
            self.id,
            self.capacity,
            self.depth,
            self.well_type,
            self.layers
        )


class MainDB:
    def add_well(
        self, 
        well
    ):
        if type(well) != Well:
            raise TypeError('well argument has to be of the type Well')
        
        self.wells.append(well)

    def __init__(
        self, 
        name,
        verbose=False
    ):
        self.db_name = name
        self.verbose = verbose

        self.db_engine = create_engine(
            'postgresql:///{}'.format(self.db_name), 
            echo=self.verbose, 
            client_encoding='utf-8'
        )
        global _db_session
        _Base.metadata.create_all(self.db_engine)
        _Session.configure(bind=self.db_engine)
        _db_session = _Session()
        self.db_session = _db_session

        self.wells = list(_db_session.query(Well))
