# Author: Third Musketeer
# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session

from .models import Integration
from .enums import IntegrationEnum


def create_integration(db: Session, integration: Integration):
    db.add(integration)
    db.commit()
    db.refresh(integration)
    return integration


def delete_integration(db: Session, integration: IntegrationEnum):
    db.delete(integration)
    db.commit()
    return integration
