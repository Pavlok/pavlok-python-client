# Author: Third Musketeer
# -*- coding: utf-8 -*-
from pyclickup import ClickUp
from sqlalchemy.orm import Session

from core.models import Integration
from core.enums import IntegrationEnum
from core.services import create_integration, delete_integration


def connect_clickup(pavlok_user_id, clickup_token, db: Session):
    db_integration = Integration(
        pavlok_user_id=pavlok_user_id,
        name=IntegrationEnum.CLICKUP,
        access_token=clickup_token,
    )
    create_integration(db, db_integration)


def disconnect_clickup(pavlok_user_id, db: Session):
    db_integration = (
        db.query(Integration)
        .filter_by(name=IntegrationEnum.CLICKUP, pavlok_user_id=pavlok_user_id)
        .one()
    )
    delete_integration(db, db_integration)


def get_clickup_token(pavlok_user_id, db: Session):
    db_clickup_integration = (
        db.query(Integration)
        .filter_by(name=IntegrationEnum.CLICKUP, pavlok_user_id=pavlok_user_id)
        .first()
    )
    if not db_clickup_integration:
        return False, False, "ClickUp not integrated for user"
    else:
        if not db_clickup_integration.access_token:
            return True, False, "Clickup not connected for user"
        else:
            return True, True, db_clickup_integration


def get_tasks(pavlok_user_id, db: Session):
    is_integrated, is_token_present, integration = get_clickup_token(pavlok_user_id, db)
    if not is_integrated or not is_token_present:
        return is_integrated, is_token_present, integration
    else:
        clickup = ClickUp(integration.access_token)
        main_team = clickup.teams[0]
        tasks = clickup._get_tasks(team_id=main_team.id)
        return is_integrated, is_token_present, tasks
