# Author: Third Musketeer
# -*- coding: utf-8 -*-
from enum import Enum


class IntegrationEnum(str, Enum):
    CLICKUP = "clickup"
    TODOIST = "todoist"
    MICROSOFT_TASKS = "microsoft_tasks"
    TRELLO = "trello"
