from sqlalchemy import create_engine, Column, Integer, Date, Time, String, DateTime  # Añadir Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DefensaTesis(Base):
    __tablename__ = 'defensas_tesis'
    
    id = Column(Integer, primary_key=True)  # Ahora funciona
    fecha = Column(DateTime)
    estudiante = Column(String(150))
    tutores = Column(String(300))
    presidente = Column(String(150))
    miembro_1 = Column(String(150))
    miembro_2 = Column(String(150))
    oponente = Column(String(150))
    hora = Column(String(10))
    lugar = Column(String(100))

def crear_tabla(engine):
    Base.metadata.create_all(engine)