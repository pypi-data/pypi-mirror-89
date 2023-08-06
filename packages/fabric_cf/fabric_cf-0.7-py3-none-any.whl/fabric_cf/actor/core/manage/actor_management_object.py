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
from typing import TYPE_CHECKING, List

from fabric_mb.message_bus.messages.reservation_mng import ReservationMng
from fabric_mb.message_bus.messages.reservation_state_avro import ReservationStateAvro
from fabric_mb.message_bus.messages.result_delegation_avro import ResultDelegationAvro
from fabric_mb.message_bus.messages.result_reservation_avro import ResultReservationAvro
from fabric_mb.message_bus.messages.result_reservation_state_avro import ResultReservationStateAvro
from fabric_mb.message_bus.messages.result_string_avro import ResultStringAvro
from fabric_mb.message_bus.messages.result_avro import ResultAvro
from fabric_mb.message_bus.messages.result_slice_avro import ResultSliceAvro
from fabric_mb.message_bus.messages.slice_avro import SliceAvro

from fabric_cf.actor.core.apis.i_actor_runnable import IActorRunnable
from fabric_cf.actor.core.common.constants import Constants, ErrorCodes
from fabric_cf.actor.core.common.exceptions import ReservationNotFoundException, SliceNotFoundException, \
    DelegationNotFoundException, ManageException
from fabric_cf.actor.core.delegation.delegation_factory import DelegationFactory
from fabric_cf.actor.core.kernel.reservation_factory import ReservationFactory
from fabric_cf.actor.core.kernel.reservation_states import ReservationStates, ReservationPendingStates
from fabric_cf.actor.core.kernel.slice_factory import SliceFactory
from fabric_cf.actor.core.manage.converter import Converter
from fabric_cf.actor.core.manage.management_object import ManagementObject
from fabric_cf.actor.core.manage.management_utils import ManagementUtils
from fabric_cf.actor.core.manage.proxy_protocol_descriptor import ProxyProtocolDescriptor
from fabric_cf.actor.core.apis.i_actor_management_object import IActorManagementObject
from fabric_cf.actor.security.acess_checker import AccessChecker
from fabric_cf.actor.security.pdp_auth import ActionId, ResourceType
from fabric_cf.actor.core.proxies.kafka.translate import Translate
from fabric_cf.actor.core.registry.actor_registry import ActorRegistrySingleton
from fabric_cf.actor.core.util.id import ID
from fabric_cf.actor.security.auth_token import AuthToken

if TYPE_CHECKING:
    from fabric_cf.actor.core.apis.i_actor import IActor
    from fabric_cf.actor.core.apis.i_slice import ISlice


class ActorManagementObject(ManagementObject, IActorManagementObject):
    def __init__(self, *, actor: IActor = None):
        super().__init__()
        self.actor = actor
        self.db = None
        if actor is not None:
            self.set_actor(actor=actor)

    def register_protocols(self):
        from fabric_cf.actor.core.manage.local.local_actor import LocalActor
        local = ProxyProtocolDescriptor(protocol=Constants.protocol_local, proxy_class=LocalActor.__name__,
                                        proxy_module=LocalActor.__module__)

        from fabric_cf.actor.core.manage.kafka.kafka_actor import KafkaActor
        kafka = ProxyProtocolDescriptor(protocol=Constants.protocol_kafka, proxy_class=KafkaActor.__name__,
                                        proxy_module=KafkaActor.__module__)

        self.proxies = []
        self.proxies.append(local)
        self.proxies.append(kafka)

    def save(self) -> dict:
        properties = super().save()
        properties[Constants.property_class_name] = ActorManagementObject.__name__
        properties[Constants.property_module_name] = ActorManagementObject.__module__

        return properties

    def recover(self):
        actor_name = None
        if Constants.property_actor_name in self.serial:
            actor_name = self.serial[Constants.property_actor_name]
        else:
            raise ManageException(Constants.not_specified_prefix.format("actor name"))

        actor = ActorRegistrySingleton.get().get_actor(actor_name_or_guid=actor_name)

        if actor is None:
            raise ManageException(Constants.object_not_found.format("Managed Object", actor_name))

        self.set_actor(actor=actor)

    def set_actor(self, *, actor: IActor):
        if self.actor is None:
            self.actor = actor
            self.db = actor.get_plugin().get_database()
            self.logger = actor.get_logger()
            self.id = actor.get_guid()

    def get_slices(self, *, slice_id: ID, caller: AuthToken, id_token: str = None) -> ResultSliceAvro:
        result = ResultSliceAvro()
        result.status = ResultAvro()

        if caller is None:
            result.status.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.status.set_message(ErrorCodes.ErrorInvalidArguments.name)
        else:
            slice_list = None
            try:
                if id_token is not None:
                    AccessChecker.check_access(action_id=ActionId.query, resource_type=ResourceType.slice,
                                               token=id_token, logger=self.logger, actor_type=self.actor.get_type(),
                                               resource_id=str(slice_id))
                try:
                    slice_list = None
                    if slice_id is None:
                        slice_list = self.db.get_slices()
                    else:
                        slice_obj = self.db.get_slice(slice_id=slice_id)
                        if slice_obj is not None:
                            slice_list = [slice_obj]
                except Exception as e:
                    self.logger.error("getSlices:db access {}".format(e))
                    result.status.set_code(ErrorCodes.ErrorDatabaseError.value)
                    result.status.set_message(ErrorCodes.ErrorDatabaseError.name)
                    result.status = ManagementObject.set_exception_details(result=result.status, e=e)
                if slice_list is not None:
                    result.slices = Translate.fill_slices(slice_list=slice_list, full=True)
                else:
                    result.status.set_code(ErrorCodes.ErrorNoSuchSlice.value)
                    result.status.set_message(ErrorCodes.ErrorNoSuchSlice.name)
            except Exception as e:
                self.logger.error("getSlices {}".format(e))
                result.status.set_code(ErrorCodes.ErrorInternalError.value)
                result.status.set_message(ErrorCodes.ErrorInternalError.name)
                result.status = ManagementObject.set_exception_details(result=result.status, e=e)
        return result

    def add_slice(self, *, slice_mng: SliceAvro, caller: AuthToken) -> ResultStringAvro:
        result = ResultStringAvro()
        result.status = ResultAvro()

        if slice_mng is None or caller is None:
            result.status.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.status.set_message(ErrorCodes.ErrorInvalidArguments.name)

        else:
            try:
                data = Converter.get_resource_data(slice_mng=slice_mng)
                slice_obj = SliceFactory.create(slice_id=ID(), name=slice_mng.get_slice_name(), data=data)

                slice_obj.set_description(description=slice_mng.get_description())
                slice_obj.set_owner(owner=self.actor.get_identity())
                slice_obj.set_inventory(value=True)

                class Runner(IActorRunnable):
                    def __init__(self, *, actor: IActor):
                        self.actor = actor

                    def run(self):
                        try:
                            self.actor.register_slice(slice_object=slice_obj)
                        except Exception as e:
                            self.actor.get_plugin().release_slice(slice_obj=slice_obj)
                            raise e

                        return None

                self.actor.execute_on_actor_thread_and_wait(runnable=Runner(actor=self.actor))

                result.set_result(str(slice_obj.get_slice_id()))
            except Exception as e:
                self.logger.error("addslice: {}".format(e))
                result.status.set_code(ErrorCodes.ErrorInternalError.value)
                result.status.set_message(ErrorCodes.ErrorInternalError.name)
                result.status = ManagementObject.set_exception_details(result=result.status, e=e)

        return result

    def remove_slice(self, *, slice_id: ID, caller: AuthToken) -> ResultAvro:
        result = ResultAvro()
        if slice_id is None or caller is None:
            result.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.set_message(ErrorCodes.ErrorInvalidArguments.name)
            return result

        try:
            class Runner(IActorRunnable):
                def __init__(self, *, actor: IActor):
                    self.actor = actor

                def run(self):
                    self.actor.remove_slice_by_slice_id(slice_id=slice_id)
                    return None

            self.actor.execute_on_actor_thread_and_wait(runnable=Runner(actor=self.actor))
        except Exception as e:
            self.logger.error("remove_slice: {}".format(e))
            result.set_code(ErrorCodes.ErrorInternalError.value)
            result.set_message(ErrorCodes.ErrorInternalError.name)
            result = ManagementObject.set_exception_details(result=result, e=e)
        return result

    def update_slice(self, *, slice_mng: SliceAvro, caller: AuthToken) -> ResultAvro:
        result = ResultAvro()
        if slice_mng is None or slice_mng.get_slice_id() is None or caller is None:
            result.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.set_message(ErrorCodes.ErrorInvalidArguments.name)
            return result

        try:
            slice_id = ID(uid=slice_mng.get_slice_id())

            class Runner(IActorRunnable):
                def __init__(self, *, actor: IActor):
                    self.actor = actor

                def run(self):
                    result = ResultAvro()
                    slice_obj = self.actor.get_slice(slice_id=slice_id)
                    if slice_obj is None:
                        result.set_code(ErrorCodes.ErrorNoSuchSlice.value)
                        result.set_message(ErrorCodes.ErrorNoSuchSlice.name)
                        return result
                    slice_obj = ManagementUtils.update_slice(slice_obj=slice_obj, slice_mng=slice_mng)

                    try:
                        self.actor.get_plugin().get_database().update_slice(slice_object=slice_obj)
                    except Exception as e:
                        print("Could not commit slice update {}".format(e))
                        result.set_code(ErrorCodes.ErrorDatabaseError.value)
                        result.set_message(ErrorCodes.ErrorDatabaseError.name)
                        result = ManagementObject.set_exception_details(result=result, e=e)

                    return result

            result = self.actor.execute_on_actor_thread_and_wait(runnable=Runner(actor=self.actor))
        except Exception as e:
            self.logger.error("update_slice: {}".format(e))
            result.set_code(ErrorCodes.ErrorInternalError.value)
            result.set_message(ErrorCodes.ErrorInternalError.name)
            result = ManagementObject.set_exception_details(result=result, e=e)

        return result

    def _get_slice_by_id(self, *, slc_id: int) -> ISlice:
        ss = self.db.get_slice_by_id(slc_id=slc_id)
        slice_obj = SliceFactory.create_instance(properties=ss)
        return slice_obj

    def get_slice_by_guid(self, *, guid: str, id_token: str = None) -> ISlice:
        ss = self.db.get_slice(slice_guid=guid)
        slice_obj = SliceFactory.create_instance(properties=ss)
        return slice_obj

    def get_reservations(self, *, caller: AuthToken, id_token: str = None, state: int = None,
                         slice_id: ID = None, rid: ID = None) -> ResultReservationAvro:
        result = ResultReservationAvro()
        result.status = ResultAvro()

        if caller is None:
            result.status.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.status.set_message(ErrorCodes.ErrorInvalidArguments.name)
            return result

        try:
            AccessChecker.check_access(action_id=ActionId.query, resource_type=ResourceType.sliver,
                                       token=id_token, logger=self.logger, actor_type=self.actor.get_type(),
                                       resource_id=str(rid))
            res_list = None
            try:
                if rid is not None:
                    res = self.db.get_reservation(rid)
                    if res is not None:
                        res_list = [res]
                    else:
                        result.status.set_code(ErrorCodes.ErrorNoSuchReservation.value)
                        result.status.set_message(ErrorCodes.ErrorNoSuchReservation.name)
                elif slice_id is not None and state is not None:
                    res_list = self.db.get_reservations_by_slice_id_state(slc_guid=slice_id, rsv_state=state)
                elif slice_id is not None:
                    res_list = self.db.get_reservations_by_slice_id(slc_guid=slice_id)
                elif state is not None:
                    res_list = self.db.get_reservations_by_state(rsv_state=state)
                else:
                    res_list = self.db.get_reservations()
            except Exception as e:
                self.logger.error("getReservations:db access {}".format(e))
                result.status.set_code(ErrorCodes.ErrorDatabaseError.value)
                result.status.set_message(ErrorCodes.ErrorDatabaseError.name)
                result.status = ManagementObject.set_exception_details(result=result.status, e=e)

            if res_list is not None:
                result.reservations = []
                for r in res_list:
                    slice_id = ReservationFactory.get_slice_id(properties=r)
                    if slice_id is None:
                        self.logger.error("Inconsistent state reservation does not belong to a slice: {}".format(r))

                    slice_obj = None
                    if slice_id is not None:
                        slice_obj = self._get_slice_by_id(slc_id=slice_id)
                    rsv_obj = ReservationFactory.create_instance(properties=r, actor=self.actor, slice_obj=slice_obj,
                                                                 logger=self.actor.get_logger())
                    if rsv_obj is not None:
                        rr = Converter.fill_reservation(reservation=rsv_obj, full=False)
                        result.reservations.append(rr)
        except ReservationNotFoundException as e:
            self.logger.error("getReservations: {}".format(e))
            result.status.set_code(ErrorCodes.ErrorNoSuchReservation.value)
            result.status.set_message(e.text)
        except Exception as e:
            self.logger.error("getReservations: {}".format(e))
            result.status.set_code(ErrorCodes.ErrorInternalError.value)
            result.status.set_message(ErrorCodes.ErrorInternalError.name)
            result.status = ManagementObject.set_exception_details(result=result.status, e=e)

        return result

    def remove_reservation(self, *, caller: AuthToken, rid: ID) -> ResultAvro:
        result = ResultAvro()

        if rid is None or caller is None:
            result.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.set_message(ErrorCodes.ErrorInvalidArguments.name)
            return result

        try:
            class Runner(IActorRunnable):
                def __init__(self, *, actor: IActor):
                    self.actor = actor

                def run(self):
                    self.actor.remove_reservation(rid=rid)
                    return None

            self.actor.execute_on_actor_thread_and_wait(runnable=Runner(actor=self.actor))
        except ReservationNotFoundException as e:
            self.logger.error("remove_reservation: {}".format(e))
            result.set_code(ErrorCodes.ErrorNoSuchReservation.value)
            result.set_message(e.text)
        except Exception as e:
            self.logger.error("remove_reservation: {}".format(e))
            result.set_code(ErrorCodes.ErrorInternalError.value)
            result.set_message(ErrorCodes.ErrorInternalError.name)
            result = ManagementObject.set_exception_details(result=result, e=e)

        return result

    def close_reservation(self, *, caller: AuthToken, rid: ID) -> ResultAvro:
        result = ResultAvro()

        if rid is None or caller is None:
            result.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.set_message(ErrorCodes.ErrorInvalidArguments.name)
            return result

        try:
            class Runner(IActorRunnable):
                def __init__(self, *, actor: IActor):
                    self.actor = actor

                def run(self):
                    self.actor.close_by_rid(rid=rid)
                    return True

            self.actor.execute_on_actor_thread_and_wait(runnable=Runner(actor=self.actor))
        except ReservationNotFoundException as e:
            self.logger.error("close_reservation: {}".format(e))
            result.set_code(ErrorCodes.ErrorNoSuchReservation.value)
            result.set_message(e.text)
        except Exception as e:
            self.logger.error("close_reservation: {}".format(e))
            result.set_code(ErrorCodes.ErrorInternalError.value)
            result.set_message(ErrorCodes.ErrorInternalError.name)
            result = ManagementObject.set_exception_details(result=result, e=e)

        return result

    def close_slice_reservations(self, *, caller: AuthToken, slice_id: ID) -> ResultAvro:
        result = ResultAvro()

        if slice_id is None or caller is None:
            result.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.set_message(ErrorCodes.ErrorInvalidArguments.name)
            return result

        try:
            class Runner(IActorRunnable):
                def __init__(self, *, actor: IActor):
                    self.actor = actor

                def run(self):
                    self.actor.close_slice_reservations(slice_id=slice_id)
                    return None

            self.actor.execute_on_actor_thread_and_wait(runnable=Runner(actor=self.actor))
        except SliceNotFoundException as e:
            self.logger.error("close_slice_reservations: {}".format(e))
            result.set_code(ErrorCodes.ErrorNoSuchSlice.value)
            result.set_message(e.text)
            result = ManagementObject.set_exception_details(result=result, e=e)
        except Exception as e:
            self.logger.error("close_slice_reservations: {}".format(e))
            result.set_code(ErrorCodes.ErrorInternalError.value)
            result.set_message(ErrorCodes.ErrorInternalError.name)
            result = ManagementObject.set_exception_details(result=result, e=e)
        return result

    def get_actor(self) -> IActor:
        return self.actor

    def get_actor_name(self) -> str:
        if self.actor is not None:
            return self.actor.get_name()

        return None

    def update_reservation(self, *, reservation: ReservationMng, caller: AuthToken) -> ResultAvro:
        result = ResultAvro()
        if reservation is None or caller is None:
            result.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.set_message(ErrorCodes.ErrorInvalidArguments.name)
            return result

        try:
            rid = ID(uid=reservation.get_reservation_id())

            class Runner(IActorRunnable):
                def __init__(self, *, actor: IActor):
                    self.actor = actor

                def run(self):
                    result = ResultAvro()
                    r = self.actor.get_reservation(rid=rid)
                    if r is None:
                        result.set_code(ErrorCodes.ErrorNoSuchReservation.value)
                        result.set_message(ErrorCodes.ErrorNoSuchReservation.name)
                        return result
                    r = ManagementUtils.update_reservation(res_obj=r, rsv_mng=reservation)
                    r.set_dirty()

                    try:
                        self.actor.get_plugin().get_database().update_reservation(reservation=r)
                    except Exception as e:
                        print("Could not commit slice update {}".format(e))
                        result.set_code(ErrorCodes.ErrorDatabaseError.value)
                        result.set_message(ErrorCodes.ErrorDatabaseError.name)
                        result = ManagementObject.set_exception_details(result=result, e=e)
                    return result

            result = self.actor.execute_on_actor_thread_and_wait(runnable=Runner(actor=self.actor))
        except ReservationNotFoundException as e:
            self.logger.error("update_reservation: {}".format(e))
            result.set_code(ErrorCodes.ErrorNoSuchReservation.value)
            result.set_message(e.text)
        except Exception as e:
            self.logger.error("update_reservation: {}".format(e))
            result.set_code(ErrorCodes.ErrorInternalError.value)
            result.set_message(ErrorCodes.ErrorInternalError.name)
            result = ManagementObject.set_exception_details(result=result, e=e)

        return result

    def get_reservation_state_for_reservations(self, *, caller: AuthToken, rids: List[str],
                                               id_token: str = None) -> ResultReservationStateAvro:
        result = ResultReservationStateAvro()
        result.status = ResultAvro()

        if rids is None or len(rids) == 0 or caller is None:
            result.status.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.status.set_message(ErrorCodes.ErrorInvalidArguments.name)
            return result

        for rid in rids:
            if rid is None:
                result.status.set_code(ErrorCodes.ErrorInvalidArguments.value)
                result.status.set_message(ErrorCodes.ErrorInvalidArguments.name)
                return result

        try:
            AccessChecker.check_access(action_id=ActionId.query, resource_type=ResourceType.sliver,
                                       token=id_token, logger=self.logger, actor_type=self.actor.get_type())
            res_list = None
            try:
                res_list = self.db.get_reservations_by_rids(rid=rids)
            except Exception as e:
                self.logger.error("get_reservation_state_for_reservations:db access {}".format(e))
                result.status.set_code(ErrorCodes.ErrorDatabaseError.value)
                result.status.set_message(ErrorCodes.ErrorDatabaseError.name)
                result.status = ManagementObject.set_exception_details(result=result.status, e=e)
                return result

            if len(res_list) == len(rids):
                result.reservation_states = []
                for r in res_list:
                    result.reservation_states.append(Converter.fill_reservation_state(res=res_list))
            elif len(res_list) > len(rids):
                raise ManageException("The database provided too many records")
            else:
                i = 0
                j = 0
                result.reservation_states = []
                while i < len(rids):
                    properties = res_list[j]
                    if rids[i] == ReservationFactory.get_reservation_id(properties=properties):
                        result.reservation_states.append(Converter.fill_reservation_state(res=res_list))
                        j += 1

                    else:
                        state = ReservationStateAvro()
                        state.set_state(ReservationStates.Unknown.value)
                        state.set_pending_state(ReservationPendingStates.Unknown.value)
                        result.reservation_states.append(state)
                    i += 1
        except ReservationNotFoundException as e:
            self.logger.error("get_reservation_state_for_reservations: {}".format(e))
            result.status.set_code(ErrorCodes.ErrorNoSuchReservation.value)
            result.status.set_message(e.text)
        except Exception as e:
            self.logger.error("get_reservation_state_for_reservations {}".format(e))
            result.status.set_code(ErrorCodes.ErrorInternalError.value)
            result.status.set_message(ErrorCodes.ErrorInternalError.name)
            result.status = ManagementObject.set_exception_details(result=result.status, e=e)

        return result

    def get_delegations(self, *, caller: AuthToken, id_token: str = None, slice_id: ID = None,
                        did: ID = None) -> ResultDelegationAvro:
        result = ResultDelegationAvro()
        result.status = ResultAvro()

        if caller is None:
            result.status.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.status.set_message(ErrorCodes.ErrorInvalidArguments.name)
            return result

        try:
            if id_token is not None:
                AccessChecker.check_access(action_id=ActionId.query, resource_type=ResourceType.delegation,
                                           token=id_token, logger=self.logger, actor_type=self.actor.get_type())
            res_list = None
            try:
                if did is not None:
                    res = self.db.get_delegation(dlg_graph_id=did)
                    if res is not None:
                        res_list = [res]
                    else:
                        result.status.set_code(ErrorCodes.ErrorNoSuchDelegation.value)
                        result.status.set_message(ErrorCodes.ErrorNoSuchDelegation.name)
                elif slice_id is not None:
                    res_list = self.db.get_delegations_by_slice_id(slice_id=slice_id)
                else:
                    res_list = self.db.get_delegations()
            except Exception as e:
                self.logger.error("getDelegations:db access {}".format(e))
                result.status.set_code(ErrorCodes.ErrorDatabaseError.value)
                result.status.set_message(ErrorCodes.ErrorDatabaseError.name)
                result.status = ManagementObject.set_exception_details(result=result.status, e=e)

            if res_list is not None:
                result.delegations = []
                for r in res_list:
                    slice_id = ReservationFactory.get_delegation_slice_id(properties=r)
                    if slice_id is None:
                        self.logger.error("Inconsistent state delegation does not belong to a slice: {}".format(r))

                    slice_obj = None
                    if slice_id is not None:
                        slice_obj = self._get_slice_by_id(slc_id=slice_id)
                    dlg_obj = DelegationFactory.create_instance(properties=r, actor=self.actor, slice_obj=slice_obj,
                                                                logger=self.actor.get_logger())
                    if dlg_obj is not None:
                        rr = Translate.translate_delegation_to_avro(delegation=dlg_obj)
                        result.delegations.append(rr)
        except DelegationNotFoundException as e:
            self.logger.error("getDelegations: {}".format(e))
            result.status.set_code(ErrorCodes.ErrorNoSuchDelegation.value)
            result.status.set_message(e.text)
        except Exception as e:
            self.logger.error("getDelegations: {}".format(e))
            result.status.set_code(ErrorCodes.ErrorInternalError.value)
            result.status.set_message(ErrorCodes.ErrorInternalError.name)
            result.status = ManagementObject.set_exception_details(result=result.status, e=e)

        return result
