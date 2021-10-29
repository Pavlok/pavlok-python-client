# Author: Third Musketeer
# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
import todoist

from core.models import Integration
from core.enums import IntegrationEnum
from core.services import create_integration, delete_integration

# https://todoist.com/oauth/authorize?client_id=0123456789abcdef&scope=data:read,data:delete&state=secretstring


def connect_todoist(pavlok_user_id, token, db: Session):
    db_integration = Integration(
        pavlok_user_id=pavlok_user_id,
        name=IntegrationEnum.TODOIST,
        access_token=token,
    )
    create_integration(db, db_integration)


def disconnect_todoist(pavlok_user_id, db: Session):
    db_integration = (
        db.query(Integration)
        .filter_by(name=IntegrationEnum.CLICKUP, pavlok_user_id=pavlok_user_id)
        .one()
    )
    delete_integration(db, db_integration)


def get_todoist_token(pavlok_user_id, db: Session):
    db_todoist_integration = (
        db.query(Integration)
        .filter_by(name=IntegrationEnum.TODOIST, pavlok_user_id=pavlok_user_id)
        .first()
    )
    if not db_todoist_integration:
        return False, False, "Todoist not integrated for user"
    else:
        if not db_todoist_integration.access_token:
            return True, False, "Todoist not connected for user"
        else:
            return True, True, db_todoist_integration


def get_projects(pavlok_user_id, db: Session):
    is_integrated, is_token_present, integration = get_todoist_token(pavlok_user_id, db)
    if not is_integrated or not is_token_present:
        return is_integrated, is_token_present, integration
    else:
        api = todoist.TodoistAPI(integration.access_token)
        api.sync()
        projects = api.state["projects"]
        return is_integrated, is_token_present, projects
