# -*- coding: utf-8 -*-
from apollo.dal.service import Service
from apollo.messaging.rmodels import Message


class MessageService(Service):
    __model__ = Message
