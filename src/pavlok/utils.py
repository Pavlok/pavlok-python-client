# Author: Third Musketeer
# -*- coding: utf-8 -*-
from .constants import PAVLOK_STIMULI_API_URL


def get_stimulus_api_url(stimulus_type: str, strength: str = "200"):
    return PAVLOK_STIMULI_API_URL + stimulus_type + "/" + strength + "/"
