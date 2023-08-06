#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2020 FABRIC Testbed
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# Author: Komal Thareja (kthare10@renci.org)
from __future__ import annotations
from typing import TYPE_CHECKING

from fabric_cf.actor.core.apis.i_delegation import IDelegation
from fabric_cf.actor.core.core.unit_set import UnitSet
from fabric_cf.actor.core.core.pool_manager import PoolManager
from fabric_cf.actor.core.plugins.substrate.substrate import Substrate

if TYPE_CHECKING:
    from fabric_cf.actor.core.core.actor import Actor
    from fabric_cf.actor.core.plugins.config.config import Config
    from fabric_cf.actor.core.apis.i_substrate_database import ISubstrateDatabase
    from fabric_cf.actor.core.apis.i_reservation import IReservation
    from fabric_cf.actor.core.apis.i_slice import ISlice


class AuthoritySubstrate(Substrate):
    def __init__(self, *, actor: Actor, db: ISubstrateDatabase, config: Config):
        super().__init__(actor=actor, db=db, config=config)
        self.pool_manager = None
        self.initialized = False

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['logger']
        del state['ticket_factory']
        del state['actor']
        del state['initialized']
        del state['pool_manager']

        del state['db']

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.logger = None
        self.ticket_factory = None
        self.actor = None
        self.initialized = None
        self.pool_manager = None

    def initialize(self):
        if not self.initialized:
            super().initialize()
            self.pool_manager = PoolManager(db=self.get_database(), identity=self.actor,
                                            logger=self.get_logger())
            self.initialized = True

    def get_pool_manager(self) -> PoolManager:
        return self.pool_manager

    def revisit(self, *, slice_obj: ISlice = None, reservation: IReservation = None,
                delegation: IDelegation = None):
        if slice_obj is not None and slice_obj.is_inventory():
            self.recover_inventory_slice(slice_obj=slice_obj)

    def recover_inventory_slice(self, *, slice_obj: ISlice):
        return

    def get_units(self, *, slice_obj: ISlice) -> UnitSet:
        # TODO recovery from database
        return None
