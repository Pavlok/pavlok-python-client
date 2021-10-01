# Author: Third Musketeer
# -*- coding: utf-8 -*-
from pydantic import BaseModel
from .utils import get_stimulus_api_url


class StimuliResponse:
    class StimuliSchema(BaseModel):
        success: bool
        id: str
        url: str

    @classmethod
    def get_stimuli_response(cls, stimulus_type: str):
        return {
            "200": {
                "description": "Successful Response",
                "content": {
                    "application/json": {
                        "example": {
                            "success:": "true",
                            "id": "pending_until_stimulus_delievered",
                            "url": get_stimulus_api_url(stimulus_type),
                        }
                    }
                },
            }
        }
