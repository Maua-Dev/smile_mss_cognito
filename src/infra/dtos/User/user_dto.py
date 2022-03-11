from enum import Enum
from typing import List
from wsgiref.validate import validator
import json

from src.infra.dtos.db_base import DbBaseModel


class CognitoUserDTO(DbBaseModel):
    userAttributes: List[dict] = []

    def __init__(self, data: dict):
        super().__init__(data)
        customAttributes = ['accessLevel', 'cpfRne', 'ra', 'role']
        defaultDataTemplate = lambda field, value: {
            "Name": field if field not in customAttributes else f"custom:{field}",
            "Value": value
        }
        for i in self.to_dict():
            if data[i] and i != 'password':
                self.userAttributes.append(defaultDataTemplate(i, str(data[i])))







