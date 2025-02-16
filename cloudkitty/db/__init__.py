# -*- coding: utf-8 -*-
# Copyright 2014 Objectif Libre
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
from oslo_config import cfg
from oslo_db.sqlalchemy import session

_FACADE = None


def _create_facade_lazily():
    global _FACADE
    if _FACADE is None:
        # FIXME(priteau): Remove autocommit=True (and ideally use of
        # LegacyEngineFacade) asap since it's not compatible with SQLAlchemy
        # 2.0.
        _FACADE = session.EngineFacade.from_config(cfg.CONF, sqlite_fk=True,
                                                   autocommit=True)
    return _FACADE


def get_engine():
    facade = _create_facade_lazily()
    return facade.get_engine()


def get_session(**kwargs):
    facade = _create_facade_lazily()
    return facade.get_session(**kwargs)
