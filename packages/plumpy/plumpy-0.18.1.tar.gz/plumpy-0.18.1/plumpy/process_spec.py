# -*- coding: utf-8 -*-
import collections
import json
import logging

from .ports import PortNamespace, InputPort, OutputPort


class ProcessSpec:
    """
    A class that defines the specifications of a :class:`plumpy.Process`,
    this includes what its inputs, outputs, etc are.

    All methods to modify the spec should have declarative names describe the
    spec e.g.: input, output

    Every Process class has one of these.
    """
    NAME_INPUTS_PORT_NAMESPACE = 'inputs'
    NAME_OUTPUTS_PORT_NAMESPACE = 'outputs'
    PORT_NAMESPACE_TYPE = PortNamespace
    INPUT_PORT_TYPE = InputPort
    OUTPUT_PORT_TYPE = OutputPort

    def __init__(self):
        self._ports = self.PORT_NAMESPACE_TYPE()
        self._validator = None
        self._sealed = False
        self._logger = logging.getLogger(__name__)

        # Create the input and output port namespace
        self._ports.create_port_namespace(self.NAME_INPUTS_PORT_NAMESPACE)
        self._ports.create_port_namespace(self.NAME_OUTPUTS_PORT_NAMESPACE)
        self._exposed_inputs = collections.defaultdict(lambda: collections.defaultdict(list))
        self._exposed_outputs = collections.defaultdict(lambda: collections.defaultdict(list))

    def __str__(self):
        return json.dumps(self.get_description(), sort_keys=True, indent=4)

    @property
    def namespace_separator(self):
        return self.PORT_NAMESPACE_TYPE.NAMESPACE_SEPARATOR

    @property
    def logger(self):
        return self._logger

    def seal(self):
        """
        Seal this specification disallowing any further changes
        """
        self._sealed = True

    @property
    def sealed(self):
        """
        Indicates if the spec is sealed or not

        :return: True if sealed, False otherwise
        :rtype: bool
        """
        return self._sealed

    def get_description(self):
        """
        Get a description of this process specification

        :return: a dictionary with the descriptions of the input and output port namespaces
        """
        description = {'inputs': self.inputs.get_description(), 'outputs': self.outputs.get_description()}

        return description

    @property
    def ports(self):
        return self._ports

    @property
    def inputs(self):
        """
        Get the input port namespace of the process specification

        :return: the input PortNamespace
        """
        return self._ports[self.NAME_INPUTS_PORT_NAMESPACE]

    @property
    def outputs(self):
        """
        Get the output port namespace of the process specification

        :return: the outputs PortNamespace
        """
        return self._ports[self.NAME_OUTPUTS_PORT_NAMESPACE]

    def _create_port(self, port_namespace, port_class, name, **kwargs):
        """
        Create a new Port of a given class and name in a given PortNamespace

        :param port_namespace: PortNamespace to which to add the port
        :param port_class: class of the Port to create
        :param name: name of the port to create
        :param kwargs: options for the port
        """
        if self.sealed:
            raise RuntimeError('Cannot add an output port after the spec has been sealed')

        namespace = name.split(self.namespace_separator)
        port_name = namespace.pop()

        if namespace:
            namespace = self.namespace_separator.join(namespace)
            port_namespace = port_namespace.create_port_namespace(namespace)

        port_namespace[port_name] = port_class(port_name, **kwargs)

    def input(self, name, **kwargs):
        """
        Define an input port in the input port namespace

        :param name: name of the input port to create
        :param kwargs: options for the input port
        """
        self._create_port(self.inputs, self.INPUT_PORT_TYPE, name, **kwargs)

    def output(self, name, **kwargs):
        """
        Define an output port in the output port namespace

        :param name: name of the output port to create
        :param kwargs: options for the output port
        """
        self._create_port(self.outputs, self.OUTPUT_PORT_TYPE, name, **kwargs)

    def input_namespace(self, name, **kwargs):
        """
        Create a new PortNamespace in the input port namespace. The keyword arguments will be
        passed to the PortNamespace constructor. Any intermediate port namespaces that need to
        be created for a nested namespace, will take constructor defaults

        :param name: namespace of the new port namespace
        :param kwargs: keyword arguments for the PortNamespace constructor
        """
        self._create_port(self.inputs, self.PORT_NAMESPACE_TYPE, name, **kwargs)

    def output_namespace(self, name, **kwargs):
        """
        Create a new PortNamespace in the output port namespace. The keyword arguments will be
        passed to the PortNamespace constructor. Any intermediate port namespaces that need to
        be created for a nested namespace, will take constructor defaults

        :param name: namespace of the new port namespace
        :param kwargs: keyword arguments for the PortNamespace constructor
        """
        self._create_port(self.outputs, self.PORT_NAMESPACE_TYPE, name, **kwargs)

    def has_input(self, name):
        """
        Return whether the input port namespace contains a port with the given name

        :param name: key of the port in the input port namespace
        """
        return name in self.inputs

    def has_output(self, name):
        """
        Return whether the output port namespace contains a port with the given name

        :param name: key of the port in the output port namespace
        """
        return name in self.outputs

    def expose_inputs(self, process_class, namespace=None, exclude=None, include=None, namespace_options=None):
        """
        This method allows one to automatically add the inputs from another Process to this ProcessSpec.
        The optional namespace argument can be used to group the exposed inputs in a separated PortNamespace.
        The exclude and include arguments can be used to restrict the set of ports that are exposed. Note that
        these two options are mutually exclusive.

        :param process_class: the Process class whose inputs to expose
        :param namespace: a namespace in which to place the exposed inputs
        :param exclude: list or tuple of input ports that are to be excluded
        :param include: list or tuple of input ports that are to be included
        :param namespace_options: a dictionary with mutable PortNamespace property values to override
        """
        self._expose_ports(
            process_class=process_class,
            source=process_class.spec().inputs,
            destination=self.inputs,
            expose_memory=self._exposed_inputs,
            namespace=namespace,
            exclude=exclude,
            include=include,
            namespace_options=namespace_options,
        )

    def expose_outputs(self, process_class, namespace=None, exclude=None, include=None, namespace_options=None):
        """
        This method allows one to automatically add the ouputs from another Process to this ProcessSpec.
        The optional namespace argument can be used to group the exposed outputs in a separated PortNamespace.
        The exclude and include arguments can be used to restrict the set of ports that are exposed. Note that
        these two options are mutually exclusive.

        :param process_class: the Process class whose outputs to expose
        :param namespace: a namespace in which to place the exposed outputs
        :param exclude: list or tuple of input ports that are to be excluded
        :param include: list or tuple of input ports that are to be included
        :param namespace_options: a dictionary with mutable PortNamespace property values to override
        """
        self._expose_ports(
            process_class=process_class,
            source=process_class.spec().outputs,
            destination=self.outputs,
            expose_memory=self._exposed_outputs,
            namespace=namespace,
            exclude=exclude,
            include=include,
            namespace_options=namespace_options,
        )

    @staticmethod
    def _expose_ports(
        process_class,
        source,
        destination,
        expose_memory,
        namespace,
        exclude,
        include,
        namespace_options=None
    ):  # pylint: disable=too-many-arguments
        """
        Expose ports from a source PortNamespace of the ProcessSpec of a Process class into the destination
        PortNamespace of this ProcessSpec. If the namespace is specified, the ports will be exposed in that sub
        namespace. The set of ports can be restricted using the mutually exclusive exclude and include tuples.
        The namespace_options will be used to override the properties of the PortNamespace into which the ports
        are exposed, whether that has been newly created or existed already.

        :param process_class: the Process class whose outputs to expose
        :param source: the PortNamespace whose ports are to be exposed
        :param destination: the PortNamespace into which the ports are to be exposed
        :param namespace: a namespace in which to place PortNamespace with the exposed outputs
        :param exclude: list or tuple of input ports that are to be excluded
        :param include: list or tuple of input ports that are to be included
        :param namespace_options: a dictionary with mutable PortNamespace property values to override
        """
        if namespace_options is None:
            namespace_options = {}

        if exclude and include is not None:
            raise ValueError('exclude and include are mutually exclusive')

        if namespace:
            port_namespace = destination.create_port_namespace(namespace)
        else:
            port_namespace = destination

        absorbed_ports = port_namespace.absorb(source, exclude, include, namespace_options)
        expose_memory[namespace][process_class] = absorbed_ports
