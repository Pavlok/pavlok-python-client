# Author: Third Musketeer
# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, DateTime

from .database import Base
from .enums import IntegrationEnum


class Integration(Base):
    __tablename__ = "integrations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pavlok_user_id = Column(Integer, nullable=False)
    name = Column("value", Enum(IntegrationEnum), nullable=False)

    url = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
    meta_data = Column(String)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
