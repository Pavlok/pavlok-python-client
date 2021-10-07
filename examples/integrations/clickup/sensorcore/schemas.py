# Author: Third Musketeer
# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Integration(BaseModel):
    id: int
    pavlok_user_id: str
    name: str
    url: Optional[str]
    access_token: Optional[str]
    refresh_token: Optional[str]
    created_at: Optional[datetime]
    metadata: Optional[str]
