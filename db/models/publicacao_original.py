#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import Base

from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship, synonym


class Publicacao_Original(Base):
    __tablename__ = 'Publicacao_Original'

    id = Column(Integer, primary_key=True)
    edicao = Column(Integer)
    numero = Column(Integer)
    data = Column(Date)
    categoria = Column(String)
    orgao = Column(String)
    suborgao = Column(String)
    tipo = Column(String)
    materia = Column(String)
    identificador = Column(Integer)
    corpo = Column(String)


    def __repr__(self):
        return '<Publicacao_Original(id={}, edicao={}, numero={}, data={}, categoria={}, orgao={}, suborgao={}, tipo={}, materia={}, identificador={}, corpo={})>'.format(
            self.id, self.edicao, self.numero, self.data, self.categoria, self.orgao, self.suborgao, self.tipo, self.materia, self.identificador, self.corpo)
