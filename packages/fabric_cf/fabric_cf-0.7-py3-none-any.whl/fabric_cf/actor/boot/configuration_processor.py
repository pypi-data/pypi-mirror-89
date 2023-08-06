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

import traceback
from typing import TYPE_CHECKING, List

from fabric_cf.actor.boot.configuration_exception import ConfigurationException
from fabric_cf.actor.boot.inventory.pool_creator import PoolCreator
from fabric_cf.actor.core.apis.i_authority import IAuthority
from fabric_cf.actor.core.common.constants import Constants
from fabric_cf.actor.core.common.resource_pool_attribute_descriptor import ResourcePoolAttributeDescriptor, \
    ResourcePoolAttributeType
from fabric_cf.actor.core.common.resource_pool_descriptor import ResourcePoolDescriptor
from fabric_cf.actor.core.container.remote_actor_cache import RemoteActorCacheSingleton, RemoteActorCache
from fabric_cf.actor.core.core.authority import Authority
from fabric_cf.actor.core.core.broker import Broker
from fabric_cf.actor.core.core.controller import Controller
from fabric_cf.actor.core.delegation.simple_resource_ticket_factory import SimpleResourceTicketFactory
from fabric_cf.actor.core.kernel.slice_factory import SliceFactory
from fabric_cf.actor.core.manage.management_utils import ManagementUtils
from fabric_cf.actor.core.manage.messages.client_mng import ClientMng
from fabric_cf.actor.core.plugins.base_plugin import BasePlugin
from fabric_cf.actor.core.plugins.config.config import Config
from fabric_cf.actor.core.plugins.db.server_actor_database import ServerActorDatabase
from fabric_cf.actor.core.plugins.substrate.authority_substrate import AuthoritySubstrate
from fabric_cf.actor.core.plugins.substrate.substrate import Substrate
from fabric_cf.actor.core.plugins.substrate.db.substrate_actor_database import SubstrateActorDatabase
from fabric_cf.actor.core.policy.authority_calendar_policy import AuthorityCalendarPolicy
from fabric_cf.actor.core.policy.broker_simpler_units_policy import BrokerSimplerUnitsPolicy
from fabric_cf.actor.core.policy.controller_simple_policy import ControllerSimplePolicy
from fabric_cf.actor.core.util.id import ID
from fabric_cf.actor.core.util.reflection_utils import ReflectionUtils
from fabric_cf.actor.core.util.resource_type import ResourceType
from fabric_cf.actor.core.core.actor import Actor
from fabric_cf.actor.security.auth_token import AuthToken
from fabric_cf.actor.core.apis.i_actor import ActorType

if TYPE_CHECKING:
    from fabric_cf.actor.boot.configuration import Configuration, ActorConfig, PolicyConfig, Peer
    from fabric_cf.actor.core.apis.i_actor import IActor
    from fabric_cf.actor.core.apis.i_mgmt_actor import IMgmtActor


class ExportAdvertisement:
    """
    Encapsulates information needed for the delegations to be exported which are later claimed by broker
    """
    def __init__(self, *, exporter: IMgmtActor, client: ClientMng, delegation: str, topic: str):
        self.exporter = exporter
        self.client = client
        self.delegation = delegation
        self.client_topic = topic
        self.exported = None


class ConfigurationProcessor:
    """
    Processing the Configuration loaded and brings up the required actors, peers and various threads
    """
    def __init__(self, *, config: Configuration):
        from fabric_cf.actor.core.container.globals import GlobalsSingleton
        self.logger = GlobalsSingleton.get().get_logger()
        self.config = config
        self.actor = None
        self.to_export = []
        self.to_advertise = []
        self.pools = {}
        self.resources = None
        self.aggregate_delegation_models = None

    def process(self):
        """
        Instantiates the configuration
        @raises ConfigurationException in case of error
        """
        try:
            self.create_actor()
            self.initialize_actor()
            self.logger.info("There are {} actors".format(Actor.actor_count))
            self.register_actor()
            self.create_default_slice()
            self.populate_inventory_neo4j()
            self.populate_inventory()
            self.recover_actor()
            self.enable_ticking()
            self.process_topology()
            self.logger.info("Processing exports with actor count {}".format(Actor.actor_count))
            self.process_advertise()
            self.logger.info("Processing exports completed")
        except Exception as e:
            self.logger.error(traceback.format_exc())
            raise ConfigurationException("Unexpected error while processing configuration {}".format(e))
        self.logger.info("Finished instantiating actors.")
        print("End process")

    def create_actor(self):
        """
        Instantiates all actors
        @raises ConfigurationException in case of error
        """
        try:
            if self.config.get_actor() is not None:
                self.logger.debug("Creating Actor: name={}".format(self.config.get_actor().get_name()))
                self.actor = self.do_common(actor_config=self.config.get_actor())
                self.do_specific(actor=self.actor, config=self.config.get_actor())
        except Exception as e:
            raise ConfigurationException("Unexpected error while creating actor {}".format(e))

    def do_common(self, *, actor_config: ActorConfig):
        """
        Perform the common operations for actor creation
        @param actor_config actor config
        @raises ConfigurationException in case of error
        """
        actor = self.make_actor_instance(actor_config=actor_config)
        actor.set_plugin(plugin=self.make_plugin_instance(actor=actor, actor_config=actor_config))
        actor.set_policy(policy=self.make_actor_policy(actor=actor, config=actor_config))
        return actor

    @staticmethod
    def make_actor_instance(*, actor_config: ActorConfig) -> IActor:
        """
        Creates Actor instance
        @param actor_config actor config
        @raises ConfigurationException in case of error
        """
        actor_type = ActorType.get_actor_type_from_string(actor_type=actor_config.get_type())
        actor = None
        if actor_type == ActorType.Orchestrator:
            actor = Controller()
        elif actor_type == ActorType.Broker:
            actor = Broker()
        elif actor_type == ActorType.Authority:
            actor = Authority()
        else:
            raise ConfigurationException("Unsupported actor type: {}".format(actor_type))

        actor_guid = ID()
        if actor_config.get_guid() is not None:
            actor_guid = ID(uid=actor_config.get_guid())
        auth_token = AuthToken(name=actor_config.get_name(), guid=actor_guid)
        actor.set_identity(token=auth_token)
        if actor_config.get_description() is not None:
            actor.set_description(description=actor_config.get_description())

        from fabric_cf.actor.core.container.globals import GlobalsSingleton
        actor.set_actor_clock(clock=GlobalsSingleton.get().get_container().get_actor_clock())

        return actor

    def make_plugin_instance(self, *, actor: IActor, actor_config: ActorConfig):
        """
        Creates Plugin instance for the Actor
        @param actor actor
        @param actor_config actor config
        @raises ConfigurationException in case of error
        """
        plugin = None
        if actor.get_plugin() is None:
            if actor.get_type() == ActorType.Authority:
                # TODO replacement of ANT CONFIG
                plugin = AuthoritySubstrate(actor=actor, db=None, config=Config())

            elif actor.get_type() == ActorType.Orchestrator:
                # TODO replacement of ANT CONFIG
                plugin = Substrate(actor=actor, db=None, config=Config())

            elif actor.get_type() == ActorType.Broker:
                plugin = BasePlugin(actor=actor, db=None, config=Config())

        if plugin is None:
            raise ConfigurationException("Cannot instantiate plugin for actor: {}".format(
                actor_config.get_name()))

        if plugin.get_database() is None:
            db = None
            user = self.config.get_global_config().get_database()[Constants.property_conf_db_user]
            password = self.config.get_global_config().get_database()[Constants.property_conf_db_password]
            db_host = self.config.get_global_config().get_database()[Constants.property_conf_db_host]
            db_name = self.config.get_global_config().get_database()[Constants.property_conf_db_name]
            if isinstance(plugin, Substrate):
                db = SubstrateActorDatabase(user=user, password=password, database=db_name, db_host=db_host,
                                            logger=self.logger)
            else:
                db = ServerActorDatabase(user=user, password=password, database=db_name, db_host=db_host,
                                         logger=self.logger)

            plugin.set_database(db=db)

        ticket_factory = SimpleResourceTicketFactory()
        ticket_factory.set_actor(actor=actor)
        plugin.set_ticket_factory(ticket_factory=ticket_factory)
        return plugin

    def make_actor_policy(self, *, actor: IActor, config: ActorConfig):
        """
        Creates Actor Policy instance
        @param actor actor
        @param actor_config actor config
        @raises ConfigurationException in case of error
        """
        policy = None
        if config.get_policy() is None:
            if actor.get_type() == ActorType.Authority:
                policy = self.make_site_policy(config=config)
            elif actor.get_type() == ActorType.Broker:
                policy = BrokerSimplerUnitsPolicy()
            elif actor.get_type() == ActorType.Orchestrator:
                policy = ControllerSimplePolicy()
        else:
            policy = self.make_policy(policy=config.get_policy())

        if policy is None:
            raise ConfigurationException("Could not instantiate policy for actor: {}".format(config.get_name()))
        return policy

    def make_site_policy(self, *, config: ActorConfig):
        """
        Creates AM Policy instance and set up controls
        @param config actor config
        @raises ConfigurationException in case of error
        """
        # TODO KOMAL
        #if config.get_controls() is None or len(config.get_controls()) == 0:
        #    raise ConfigurationException("Missing authority policy but no control has been specified")

        policy = AuthorityCalendarPolicy()
        for c in config.get_controls():
            try:
                if c.get_module_name() is None or c.get_class_name() is None:
                    raise ConfigurationException("Missing control class name")

                control = ReflectionUtils.create_instance(module_name=c.get_module_name(),
                                                          class_name=c.get_class_name())

                if c.get_type() is None:
                    raise ConfigurationException("No type specified for control")

                control.add_type(rtype=ResourceType(resource_type=c.get_type()))
                policy.register_control(control=control)
            except Exception as e:
                traceback.print_exc()
                raise ConfigurationException("Could not create control {}".format(e))
        return policy

    @staticmethod
    def make_policy(*, policy: PolicyConfig):
        """
        Creates Policy Instance
        @param policy policy config
        @raises ConfigurationException in case of error
        """
        if policy.get_class_name() is None or policy.get_module_name() is None:
            raise ConfigurationException("Policy is missing class name")

        return ReflectionUtils.create_instance(module_name=policy.get_module_name(), class_name=policy.get_class_name())

    def do_specific(self, *, actor: IActor, config: ActorConfig):
        """
        Do Actor specify intialization
        @param actor actor
        @param config actor config
        @raises ConfigurationException in case of error
        """
        if isinstance(actor, IAuthority):
            self.pools = self.read_resource_pools(config=config)
            self.resources = self.read_resource_pools2(config=config)

    def read_resource_pools(self, *, config: ActorConfig) -> dict:
        """
        Read Resource pools and create pools
        @param config actor config
        @raises ConfigurationException in case of error
        """
        result = {}
        pools = config.get_pools()
        if pools is None or len(pools) == 0:
            return result

        for p in pools:
            descriptor = ResourcePoolDescriptor()
            descriptor.set_resource_type(rtype=ResourceType(resource_type=p.get_type()))
            descriptor.set_resource_type_label(rtype_label=p.get_label())
            descriptor.set_units(units=p.get_units())
            descriptor.set_start(start=p.get_start())
            descriptor.set_end(end=p.get_end())
            descriptor.set_pool_factory_class(factory_class=p.get_factory_class())
            descriptor.set_pool_factory_module(factory_module=p.get_factory_module())
            handler = p.get_handler()
            if handler is not None:
                descriptor.set_handler_class(handler_class=handler.get_class_name())
                descriptor.set_handler_module(module=handler.get_module_name())
                descriptor.set_handler_properties(properties=handler.get_properties())

            descriptor.pool_properties = p.get_properties()

            for attr in p.get_attributes():
                attribute = ResourcePoolAttributeDescriptor()
                attribute.set_key(value=attr.get_key())
                attribute.set_value(value=attr.get_value())
                if attr.get_type().lower() == "integer":
                    attribute.set_type(rtype=ResourcePoolAttributeType.INTEGER)
                elif attr.get_type().lower() == "string":
                    attribute.set_type(rtype=ResourcePoolAttributeType.STRING)
                elif attr.get_type().lower() == "neo4j":
                    attribute.set_type(rtype=ResourcePoolAttributeType.NEO4J)
                elif attr.get_type().lower() == "class":
                    attribute.set_type(rtype=ResourcePoolAttributeType.CLASS)
                else:
                    raise ConfigurationException("Unsupported attribute type: {}".format(attr.get_type()))
                descriptor.add_attribute(attribute=attribute)

            result[descriptor.get_resource_type()] = descriptor
        return result

    def read_resource_pools2(self, *, config: ActorConfig) -> dict:
        """
        Read resource pool config and create pools
        @param config actor config
        @raises ConfigurationException in case of error
        """
        result = {}
        resources = config.get_resources()
        if resources is None or len(resources) == 0:
            return result

        for r in resources:
            descriptor = ResourcePoolDescriptor()
            descriptor.set_resource_type(rtype=ResourceType(resource_type=r.get_type()))
            descriptor.set_resource_type_label(rtype_label=r.get_label())

            # TODO for now it holds the control name
            descriptor.set_pool_factory_class(factory_class=r.get_control().get_class_name())
            descriptor.set_pool_factory_module(factory_module=r.get_control().get_module_name())

            handler = r.get_handler()
            if handler is not None:
                descriptor.set_handler_class(handler_class=handler.get_class_name())
                descriptor.set_handler_module(module=handler.get_module_name())
                descriptor.set_handler_properties(properties=handler.get_properties())

            descriptor.pool_properties = r.get_properties()

            for attr in r.get_attributes():
                attribute = ResourcePoolAttributeDescriptor()
                attribute.set_key(value=attr.get_key())
                attribute.set_value(value=attr.get_value())
                if attr.get_type().lower() == "integer":
                    attribute.set_type(rtype=ResourcePoolAttributeType.INTEGER)
                elif attr.get_type().lower() == "string":
                    attribute.set_type(rtype=ResourcePoolAttributeType.STRING)
                elif attr.get_type().lower() == "neo4j":
                    attribute.set_type(rtype=ResourcePoolAttributeType.NEO4J)
                elif attr.get_type().lower() == "class":
                    attribute.set_type(rtype=ResourcePoolAttributeType.CLASS)
                else:
                    raise ConfigurationException("Unsupported attribute type: {}".format(attr.get_type()))
                descriptor.add_attribute(attribute=attribute)

            result[descriptor.get_resource_type()] = descriptor
        return result

    def initialize_actor(self):
        """
        Initialize actor
        @raises ConfigurationException in case of error
        """
        try:
            Actor.actor_count += 1
            self.actor.initialize()
        except Exception as e:
            raise ConfigurationException("Actor failed to initialize: {} {}".format(self.actor.get_name(), e))

    def register_actor(self):
        """
        Register actor
        @raises ConfigurationException in case of error
        """
        try:
            from fabric_cf.actor.core.container.globals import GlobalsSingleton
            GlobalsSingleton.get().get_container().register_actor(actor=self.actor)
        except Exception as e:
            raise ConfigurationException("Could not register actor: {} {}".format(self.actor.get_name(), e))

    def create_default_slice(self):
        """
        Create default slice
        @raises ConfigurationException in case of error
        """
        if self.actor.get_type() != ActorType.Authority:
            slice_obj = SliceFactory.create(slice_id=ID(), name=self.actor.get_name())
            slice_obj.set_inventory(value=True)
            try:
                self.actor.register_slice(slice_object=slice_obj)
            except Exception as e:
                traceback.print_exc()
                raise ConfigurationException("Could not create default slice for actor: {} {}".format(
                    self.actor.get_name(), e))

    def populate_inventory(self):
        """
        Populate inventory
        @raises ConfigurationException in case of error
        """
        if isinstance(self.actor, IAuthority) and isinstance(self.actor.get_plugin(), AuthoritySubstrate):
            creator = PoolCreator(substrate=self.actor.get_plugin(), pools=self.pools,
                                  neo4j_config=self.config.get_global_config().get_neo4j_config())
            creator.process()

    def populate_inventory_neo4j(self):
        """
        Load Aggregate Resource model
        @raises ConfigurationException in case of error
        """
        if isinstance(self.actor, IAuthority) and isinstance(self.actor.get_plugin(), AuthoritySubstrate):
            creator = PoolCreator(substrate=self.actor.get_plugin(), pools=self.resources,
                                  neo4j_config=self.config.get_global_config().get_neo4j_config())
            self.aggregate_delegation_models = creator.process_neo4j(actor_name=self.actor.get_name(),
                                                                     substrate_file=self.config.get_actor().
                                                                     get_substrate_file())

    def recover_actor(self):
        """
        Recover an actor on stateful restart
        @raises ConfigurationException in case of error
        """
        try:
            self.actor.recover()
        except Exception as e:
            raise ConfigurationException("Recovery failed for actor: {} e: {}".format(self.actor.get_name(), e))

    def enable_ticking(self):
        """
        Enable the Actor tick
        """
        from fabric_cf.actor.core.container.globals import GlobalsSingleton
        GlobalsSingleton.get().get_container().register(tickable=self.actor)

    def process_topology(self):
        """
        Set up Peer registry with identity and kafka topic information
        @raises ConfigurationException in case of error
        """
        if self.config.get_peers() is None or len(self.config.get_peers()) == 0:
            self.logger.debug("No peers specified")
        else:
            self.create_proxies(peers=self.config.get_peers())

    def process_advertise(self):
        """
        Set up Aggregate Delegation models for the peers
        @raises ConfigurationException in case of error
        """
        if self.aggregate_delegation_models is None and len(self.to_advertise) > 0:
            raise ConfigurationException("No delegations found in Aggregate Resource Model")

        for ei in self.to_advertise:
            self.advertise(info=ei)

    def create_proxies(self, *, peers: List[Peer]):
        """
        Set up proxies
        @param peers List of the Peer config
        @raises ConfigurationException in case of error
        """
        for e in peers:
            self.process_peer(peer=e)

    def vertex_to_registry_cache(self, *, peer: Peer):
        """
        Add peer to Registry Cache
        @param peer peer config
        @raises ConfigurationException in case of error
        """
        self.logger.debug("Adding vertex for {}".format(peer.get_name()))

        if peer.get_name() is None:
            raise ConfigurationException("Actor must specify a name")

        if peer.get_guid() is None:
            raise ConfigurationException("Actor must specify a guid")

        protocol = Constants.protocol_local
        kafka_topic = None
        if peer.get_kafka_topic() is not None:
            protocol = Constants.protocol_kafka
            kafka_topic = peer.get_kafka_topic()

        actor_type = peer.get_type().lower()

        entry = {
            RemoteActorCache.actor_name: peer.get_name(),
            RemoteActorCache.actor_guid: ID(uid=peer.get_guid()),
            RemoteActorCache.actor_type: actor_type,
            RemoteActorCache.actor_protocol: protocol
        }
        if kafka_topic is not None:
            entry[RemoteActorCache.actor_location] = kafka_topic

        RemoteActorCacheSingleton.get().add_partial_cache_entry(guid=ID(uid=peer.get_guid()), entry=entry)

    def process_peer(self, *, peer: Peer):
        """
        Process a peer
        @param peer peer
        @raises ConfigurationException in case of error
        """
        from_guid = ID(uid=peer.get_guid())
        from_type = ActorType.get_actor_type_from_string(actor_type=peer.get_type())
        to_guid = self.actor.get_guid()
        to_type = self.actor.get_type()

        # We only like peers broker->site and service->broker
        # Reverse the peer if it connects site->broker or broker->service

        if from_type == ActorType.Authority and to_type == ActorType.Broker:
            from_guid, to_guid = to_guid, from_guid
            from_type, to_type = to_type, from_type

        if from_type == ActorType.Broker and to_type == ActorType.Orchestrator:
            from_guid, to_guid = to_guid, from_guid
            from_type, to_type = to_type, from_type

        # peers between actors of same type aren't allowed unless the actors are both brokers
        if from_type == to_type and from_type != ActorType.Broker:
            raise ConfigurationException(
                "Invalid peer type: broker can only talk to broker, orchestrator or site authority")

        container = ManagementUtils.connect(caller=self.actor.get_identity())
        to_mgmt_actor = container.get_actor(guid=to_guid)
        if to_mgmt_actor is None:
            self.logger.debug("to_mgmt_actor={} to_guid={}".format(type(to_mgmt_actor), to_guid))
            if container.get_last_error() is not None:
                self.logger.error(container.get_last_error())
        from_mgmt_actor = container.get_actor(guid=from_guid)
        if from_mgmt_actor is None:
            self.logger.debug("from_mgmt_actor={} from_guid={}".format(type(from_mgmt_actor), from_guid))
            if container.get_last_error() is not None:
                self.logger.error(container.get_last_error())

        self.vertex_to_registry_cache(peer=peer)

        try:
            client = RemoteActorCacheSingleton.get().establish_peer(from_guid=from_guid,
                                                                    from_mgmt_actor=from_mgmt_actor,
                                                                    to_guid=to_guid, to_mgmt_actor=to_mgmt_actor)
            self.logger.debug("Client returned {}".format(client))
            if client is not None:
                self.parse_exports(peer=peer, client=client, mgmt_actor=to_mgmt_actor)
        except Exception as e:
            raise ConfigurationException("Could not process exports from: {} to {}. e= {}" .format(
                peer.get_guid(), self.actor.get_guid(), e))

    def parse_exports(self, *, peer: Peer, client: ClientMng, mgmt_actor: IMgmtActor):
        """
        Identify all the delegations to be advertised
        @param peer peer config
        @param client client
        @param mgmt_actor management actor
        """
        if peer.get_delegation() is not None:
            info = ExportAdvertisement(exporter=mgmt_actor, client=client,
                                       delegation=peer.get_delegation(),
                                       topic=peer.get_kafka_topic())
            self.to_advertise.append(info)

    def advertise(self, *, info: ExportAdvertisement):
        """
        Advertise a delegation
        @param info advertisement information
        @raises ConfigurationException in case of error
        """
        self.logger.debug("Using Server Actor {} to export resources".format(info.exporter.__class__.__name__))

        delegation = self.aggregate_delegation_models.get(info.delegation, None)

        if delegation is None:
            raise ConfigurationException("Aggregate Delegation Model not found for delegation: {}".format(
                info.delegation))

        info.exported = info.exporter.advertise_resources(delegation=delegation,
                                                          client=AuthToken(name=info.client.get_name(),
                                                                           guid=ID(uid=info.client.get_guid())))

        if info.exported is None:
            raise ConfigurationException("Could not export resources from actor: {} to actor: {} Error = {}".format(
                info.exporter.get_name(), info.client.get_name(), info.exporter.get_last_error()))
