# Author: Third Musketeer
# -*- coding: utf-8 -*-
from pyclickup import ClickUp
from sensorcore.database import query_db
from sensorcore.schemas import Integration


def add_integration(pavlok_user_id, clickup_token):
    # "ON CONFLICT (pavlok_user_id, name) DO UPDATE SET access_token = excluded.access_token"
    integration_query = (
        "INSERT INTO integrations(access_token, pavlok_user_id, name) VALUES('{0}', '{1}', '{2}')"
        "".format(clickup_token, pavlok_user_id, "clickup")
    )
    print(integration_query)
    results = query_db(integration_query)


def get_clickup_token(pavlok_user_id):
    clickup_token_query = "SELECT * FROM integrations WHERE pavlok_user_id = '{0}' AND name='clickup' LIMIT 1".format(
        pavlok_user_id
    )
    results = query_db(clickup_token_query)
    if len(results) == 0:
        return False, False, "ClickUp not integrated for user"
    else:
        result = results[0]
        if not result["access_token"]:
            return True, False, "Clickup not connected for user"
        else:
            return True, True, result


def get_clickup_tasks(pavlok_user_id):
    is_integrated, is_token_present, result = get_clickup_token(pavlok_user_id)
    if not is_integrated or not is_token_present:
        return is_integrated, is_token_present, result
    else:
        user_integration: Integration = Integration(**result)

        clickup = ClickUp(user_integration.access_token)

        main_team = clickup.teams[0]

        tasks = clickup._get_tasks(team_id=main_team.id)
        return is_integrated, is_token_present, tasks
