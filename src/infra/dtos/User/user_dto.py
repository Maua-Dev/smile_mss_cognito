from enum import Enum
from typing import List
from wsgiref.validate import validator
import json

from src.domain.entities.enums import ACCESS_LEVEL, ROLE
from src.domain.entities.user import User
from src.infra.dtos.db_base import DbBaseModel


class CognitoUserDTO(DbBaseModel):
    userAttributes: List[dict] = []
    userSub: str

    def __init__(self, data: dict):
        super().__init__(data)
        self.userSub = data['sub'] if 'sub' in data else None
        customAttributes = ['accessLevel', 'cpfRne', 'ra', 'role', 'acceptedTerms', 'acceptedNotific', 'socialName']
        defaultDataTemplate = lambda field, value: {
            "Name": field if field not in customAttributes else f"custom:{field}",
            "Value": value
        }
        for i in self.to_dict():
            if self.__getattribute__(i) and i != 'password':
                self.userAttributes.append(defaultDataTemplate(i, str(self.__getattribute__(i))))


    def toEntity(self):
        return User(
        name=self.name,
        cpfRne=self.cpfRne,
        ra=self.ra,
        email=self.email,
        role=self.role,
        accessLevel=self.accessLevel,
        acceptedTerms=self.acceptedTerms,
        acceptedNotifications=self.acceptedNotific,
        socialName=self.socialName,
        id=self.userSub if self.userSub else None
        )

    @staticmethod
    def fromKeyValuePair(data: dict):
        dataDict = {}
        for i in data:
            field = i['Name'].removeprefix('custom:')
            try:
                value = i['Value'] if (field != 'accessLevel' and field != 'role') else ACCESS_LEVEL(i['Value']) if field == 'accessLevel' else ROLE(i['Value'])
                fixedField = field if field != 'acceptedNotific' else 'acceptedNotifications'
                dataDict[fixedField] = value
            except:
                pass
        return CognitoUserDTO(dataDict)






