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

import time
import unittest
from typing import TYPE_CHECKING

from fabric_cf.actor.core.common.constants import Constants
from fabric_cf.actor.core.common.resource_pool_attribute_descriptor import ResourcePoolAttributeDescriptor, \
    ResourcePoolAttributeType
from fabric_cf.actor.core.common.resource_pool_descriptor import ResourcePoolDescriptor
from fabric_cf.actor.core.core.ticket import Ticket
from fabric_cf.actor.core.core.unit import Unit
from fabric_cf.actor.core.core.unit_set import UnitSet
from fabric_cf.actor.core.kernel.client_reservation_factory import ClientReservationFactory
from fabric_cf.actor.core.kernel.resource_set import ResourceSet
from fabric_cf.actor.core.policy.resource_control import ResourceControl
from fabric_cf.actor.core.policy.vm_control import VMControl
from fabric_cf.actor.core.util.id import ID
from fabric_cf.actor.core.util.resource_data import ResourceData
from fabric_cf.actor.test.core.policy.authority_calendar_policy_test import AuthorityCalendarPolicyTest

if TYPE_CHECKING:
    from fabric_cf.actor.core.policy.authority_calendar_policy import AuthorityCalendarPolicy
    from fabric_cf.actor.core.apis.i_actor import IActor
    from fabric_cf.actor.core.apis.i_slice import ISlice
    from fabric_cf.actor.core.time.term import Term
    from fabric_cf.actor.core.util.resource_type import ResourceType
    from fabric_cf.actor.core.apis.i_authority import IAuthority
    from fabric_cf.actor.core.util.update_data import UpdateData
    from fabric_cf.actor.core.apis.i_authority_reservation import IAuthorityReservation
    from fabric_cf.actor.core.apis.i_reservation import IReservation


class VMControlTest(AuthorityCalendarPolicyTest, unittest.TestCase):
    VMMemory = 300
    VmmCapacity = 3

    from fabric_cf.actor.core.container.globals import Globals
    Globals.config_file = "./config/config.test.yaml"
    Constants.superblock_location = './state_recovery.lock'

    from fabric_cf.actor.core.container.globals import GlobalsSingleton
    GlobalsSingleton.get().start(force_fresh=True)
    while not GlobalsSingleton.get().start_completed:
        time.sleep(0.0001)

    def get_control(self, policy: AuthorityCalendarPolicy = None):
        if policy:
            return policy.controls_by_guid.values().__iter__().__next__()
        else:
            control = VMControl()
            properties = {ResourceControl.PropertyControlResourceTypes: str(self.Type)}
            control.configure(properties=properties)
            return control

    def get_pool_descriptor(self) -> ResourcePoolDescriptor:
        rd = ResourcePoolDescriptor()
        rd.set_resource_type(rtype=self.Type)
        rd.set_resource_type_label(rtype_label=self.Label)
        ad = ResourcePoolAttributeDescriptor()
        ad.set_key(value=Constants.resource_memory)
        ad.set_label(label="Memory")
        ad.set_unit(unit="MB")
        ad.set_type(rtype=ResourcePoolAttributeType.INTEGER)
        ad.set_value(value=str(self.VMMemory))
        rd.add_attribute(attribute=ad)
        return rd

    def get_source(self, units: int, rtype: ResourceType, term: Term, actor: IActor, slice_obj: ISlice):
        resources = ResourceSet(units=units, rtype=rtype, rdata=ResourceData())
        properties = resources.get_resource_properties()
        rd = self.get_pool_descriptor()
        resources.set_resource_properties(p=rd.save(properties=properties, prefix=None))

        local = resources.get_local_properties()
        local[VMControl.PropertyIPSubnet] = "255.255.255.0"
        local[VMControl.PropertyIPList] = "192.168.1.2/24"
        local[VMControl.PropertyCapacity] = self.VmmCapacity

        delegation = actor.get_plugin().get_ticket_factory().make_delegation(units=units, term=term, rtype=rtype,
                                                                             vector=None)
        ticket = actor.get_plugin().get_ticket_factory().make_ticket(delegation=delegation, source=None)
        cs = Ticket(ticket=ticket, plugin=actor.get_plugin())
        resources.set_resources(cset=cs)
        source = ClientReservationFactory.create(rid=ID(), resources=resources, term=term, slice_object=slice_obj)
        return source

    def get_donate_set(self, authority: IAuthority) -> ResourceSet:
        rset = ResourceSet(units=self.DonateUnits, rtype=self.Type, rdata=ResourceData())
        properties = rset.get_resource_properties()
        rd = self.get_pool_descriptor()
        properties = rd.save(properties=properties, prefix=None)
        rset.set_resource_properties(p=properties)
        local = rset.get_local_properties()
        local[VMControl.PropertyIPSubnet] = "255.255.255.0"
        local[VMControl.PropertyIPList] = "192.168.1.2/24"
        local[VMControl.PropertyCapacity] = self.VmmCapacity
        uset = UnitSet(plugin=authority.get_plugin())

        for i in range(self.DonateUnits):
            host = Unit(uid=ID())
            host.set_property(name=Constants.unit_host_name, value="Host" + str(i))
            host.set_property(name=Constants.unit_management_ip, value="192.168.123." + str(i + 1))
            host.set_property(name=Constants.unit_control, value="192.168.123." + str(i + 1))
            uset.add_unit(u=host)

        rset.set_resources(cset=uset)

        return rset

    def check_before_donate_set(self, authority: IAuthority):
        super().check_before_donate_set(authority)
        policy = authority.get_policy()
        control = self.get_control(policy=policy)
        self.assertIsNotNone(control.inventory)
        self.assertEqual(0, len(control.inventory))

    def check_after_donate_set(self, authority: IAuthority, rset: ResourceSet):
        policy = authority.get_policy()
        control = self.get_control(policy)

        self.assertEqual(1, len(control.inventory))
        pool = control.inventory.values().__iter__().__next__()

        self.assertEqual(self.DonateUnits, pool.get_vmms_count())
        self.assertEqual(self.VmmCapacity, pool.get_capacity())
        self.assertEqual(self.Type, pool.get_type())

        self.assertIsNotNone(pool.vmms)

        for vmm in pool.get_vmm_set():
            self.assertIsNotNone(vmm.get_host())
            self.assertEqual(self.VmmCapacity, vmm.get_available())
            self.assertEqual(self.VmmCapacity, vmm.get_capacity())
            self.assertEqual(0, vmm.get_hosted_count())

    my_unit = None

    def check_incoming_lease(self, authority: IAuthority, request: IAuthorityReservation, incoming: IReservation,
                             udd: UpdateData):
        super().check_incoming_lease(authority, request, incoming, udd)
        policy = authority.get_policy()
        control = self.get_control(policy)
        rset = incoming.get_resources()
        uset = rset.get_resources()
        self.assertIsNotNone(uset)
        # TODO KOMAL
        if uset.get_units() != 0:
            print("Checking units")
            self.assertEqual(self.TicketUnits, uset.get_units())
            u = uset.get_set().values().__iter__().__next__()
            self.assertEqual(self.VMMemory, int(u.get_property(name=Constants.unit_memory)))
            self.assertIsNotNone(u.get_property(name=Constants.unit_management_ip))
            self.assertIsNotNone(u.get_property(name=Constants.unit_manage_subnet))

            vmm_host_id = u.get_parent_id()
            self.assertIsNotNone(vmm_host_id)

            pool = control.inventory.get(self.Type)
            self.assertIsNotNone(pool)

            vmm = pool.get_vmm(uid=vmm_host_id)
            self.assertIsNotNone(vmm)

            self.assertEqual(self.TicketUnits, vmm.get_hosted_count())
            self.assertEqual(self.VmmCapacity - self.TicketUnits, vmm.get_available())
            self.assertTrue(u in vmm.get_hosted_vms())
            print("Unit= {}".format(u))
            self.my_unit = u
        else:
            print("It should never enter here")
            assert (1 != 0)

    def check_incoming_close_lease(self, authority: IAuthority, request: IAuthorityReservation, incoming: IReservation,
                                   udd: UpdateData):
        super().check_incoming_close_lease(authority, request, incoming, udd)
        policy = authority.get_policy()
        control = self.get_control(policy)

        self.assertIsNotNone(self.my_unit)

        rset = incoming.get_resources()
        uset = rset.get_resources()
        self.assertIsNotNone(uset)
        self.assertEqual(0, uset.get_units())

        vmm_host_id = self.my_unit.get_parent_id()
        self.assertIsNotNone(vmm_host_id)

        pool = control.inventory.get(self.Type)
        self.assertIsNotNone(pool)

        vmm = pool.get_vmm(uid=vmm_host_id)
        self.assertIsNotNone(vmm)

        self.assertEqual(0, vmm.get_hosted_count())
        self.assertEqual(self.VmmCapacity, vmm.get_available())
        self.assertFalse(self.my_unit in vmm.get_hosted_vms())

    def check_incoming_extend_lease(self, authority: IAuthority, request: IAuthorityReservation, incoming: IReservation,
                                    update_data: UpdateData):
        super().check_incoming_extend_lease(authority, request, incoming, update_data)
        policy = authority.get_policy()
        control = self.get_control(policy)

        rset = incoming.get_resources()
        uset = rset.get_resources()
        self.assertIsNotNone(uset)
        self.assertEqual(self.TicketUnits, uset.get_units())

        u = uset.get_set().values().__iter__().__next__()
        self.assertEqual(self.VMMemory, int(u.get_property(name=Constants.unit_memory)))
        self.assertIsNotNone(u.get_property(name=Constants.unit_management_ip))
        self.assertIsNotNone(u.get_property(name=Constants.unit_manage_subnet))

        vmm_host_id = self.my_unit.get_parent_id()
        self.assertIsNotNone(vmm_host_id)

        pool = control.inventory.get(rtype=self.Type)
        self.assertIsNotNone(pool)

        vmm = pool.get_vmm(uid=vmm_host_id)
        self.assertIsNotNone(vmm)

        self.assertEqual(self.TicketUnits, vmm.get_hosted_count())
        self.assertEqual(self.VmmCapacity - self.TicketUnits, vmm.get_available())
        self.assertTrue(u in vmm.get_hosted_vms())
        print("Extend Unit= {}".format(u))
        self.assertEqual(self.my_unit, u)