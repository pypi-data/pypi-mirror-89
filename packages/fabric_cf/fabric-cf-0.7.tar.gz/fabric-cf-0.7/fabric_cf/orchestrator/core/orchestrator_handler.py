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
import traceback

from fabric_cf.actor.boot.inventory.neo4j_resource_pool_factory import Neo4jResourcePoolFactory
from fabric_cf.actor.core.apis.i_actor import ActorType
from fabric_cf.actor.core.apis.i_mgmt_controller import IMgmtController
from fabric_cf.actor.core.common.constants import Constants
from fabric_cf.actor.core.util.id import ID
from fabric_cf.actor.security.acess_checker import AccessChecker
from fabric_cf.actor.security.fabric_token import FabricToken
from fabric_cf.actor.security.pdp_auth import ActionId, ResourceType
from fabric_cf.orchestrator.core.exceptions import OrchestratorException
from fabric_cf.orchestrator.core.orchestrator_state import OrchestratorStateSingleton


class OrchestratorHandler:
    def __init__(self):
        self.controller_state = OrchestratorStateSingleton.get()
        from fabric_cf.actor.core.container.globals import GlobalsSingleton
        self.logger = GlobalsSingleton.get().get_logger()
        self.jwks_url = GlobalsSingleton.get().get_config().get_oauth_config().get(
            Constants.property_conf_o_auth_jwks_url, None)
        self.pdp_config = GlobalsSingleton.get().get_config().get_global_config().get_pdp_config()

    def get_logger(self):
        return self.logger

    def validate_credentials(self, *, token) -> dict:
        try:
            fabric_token = FabricToken(logger=self.logger, token=token)

            return fabric_token.validate()
        except Exception as e:
            self.logger.error(traceback.format_exc())
            self.logger.error("Exception occurred while validating the token e: {}".format(e))

    def get_broker(self, *, controller: IMgmtController) -> ID:
        try:
            brokers = controller.get_brokers()
            self.logger.debug("Brokers: {}".format(brokers))
            self.logger.error("Last Error: {}".format(controller.get_last_error()))
            if brokers is not None:
                return ID(uid=next(iter(brokers), None).get_guid())

        except Exception:
            self.logger.error(traceback.format_exc())

        return None

    def discover_types(self, *, controller: IMgmtController, token: str) -> dict:
        broker = self.get_broker(controller=controller)
        if broker is None:
            raise OrchestratorException("Unable to determine broker proxy for this controller. "
                                        "Please check Orchestrator container configuration and logs.")

        self.controller_state.set_broker(broker=str(broker))

        my_pools = controller.get_pool_info(broker=broker, id_token=token)
        if my_pools is None:
            raise OrchestratorException("Could not discover types: {}".format(controller.get_last_error()))

        response = None
        for p in my_pools:
            try:
                bqm = p.properties.get(Constants.broker_query_model, None)
                if bqm is not None:
                    graph = Neo4jResourcePoolFactory.get_graph_from_string(graph_str=bqm)
                    graph.validate_graph()
                    Neo4jResourcePoolFactory.delete_graph(graph_id=graph.get_graph_id())
                    response = bqm
            except Exception as e:
                self.logger.error(traceback.format_exc())
                self.logger.debug("Could not process discover types response {}".format(e))

        return response

    def list_resources(self, *, token: str):
        try:
            AccessChecker.check_access(action_id=ActionId.query, resource_type=ResourceType.resources, token=token,
                                       actor_type=ActorType.Orchestrator)
            self.controller_state.close_dead_slices()
            controller = self.controller_state.get_management_actor()
            self.logger.debug("list resources invoked controller:{}".format(controller))

            try:
                abstract_models = self.discover_types(controller=controller, token=token)
            except Exception as e:
                self.logger.error("Failed to populate abstract models e: {}".format(e))
                raise e

            if abstract_models is None:
                raise OrchestratorException("Failed to populate abstract models")

            return abstract_models

        except Exception as e:
            self.logger.error(traceback.format_exc())
            self.logger.error("Exception occurred processing list resource e: {}".format(e))
            raise e
