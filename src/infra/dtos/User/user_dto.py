from enum import Enum
from typing import List
from wsgiref.validate import validator
import json

from src.domain.entities.enums import ACCESS_LEVEL, ROLE
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
            if data.get(i) and i != 'password':
                self.userAttributes.append(defaultDataTemplate(i, str(data[i])))

    @staticmethod
    def fromKeyValuePair(data: dict):
        dataDict = {}
        for i in data:
            field = i['Name'].removeprefix('custom:')
            try:
                value = i['Value'] if (field != 'accessLevel' and field != 'role') else ACCESS_LEVEL(i['Value']) if field == 'accessLevel' else ROLE(i['Value'])
                dataDict[field] = value
            except:
                pass
        return CognitoUserDTO(dataDict)






