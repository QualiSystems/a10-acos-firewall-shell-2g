from cloudshell.devices.driver_helper import get_logger_with_thread_id, get_api, get_cli, \
    parse_custom_commands
from cloudshell.devices.runners.run_command_runner import RunCommandRunner
from cloudshell.devices.runners.state_runner import StateRunner
from cloudshell.devices.standards.firewall.configuration_attributes_structure import \
    create_firewall_resource_from_context as create_resource_from_context
from cloudshell.firewall.firewall_resource_driver_interface import FirewallResourceDriverInterface
from cloudshell.shell.core.driver_context import InitCommandContext, ResourceCommandContext, \
    AutoLoadCommandContext, AutoLoadDetails
from cloudshell.shell.core.driver_utils import GlobalLock
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface

from cloudshell.firewall.a10.cli.a10_cli_handler import A10CliHandler as CliHandler
from cloudshell.firewall.a10.runners.a10_autoload_runner import A10AutoloadRunner as AutoloadRunner
from cloudshell.firewall.a10.snmp.a10_snmp_handler import A10SnmpHandler as SnmpHandler


class A10AcosFirewallShell2GDriver(ResourceDriverInterface, FirewallResourceDriverInterface,
                                   GlobalLock):
    SUPPORTED_OS = [r'ACOS']
    SHELL_NAME = 'A10AcosFirewallShell2G'

    def __init__(self):
        super(A10AcosFirewallShell2GDriver, self).__init__()
        self._cli = None

    def initialize(self, context):
        """Initialize the driver session

        :param InitCommandContext context: the context the command runs on
        :rtype: str
        """

        resource_config = create_resource_from_context(self.SHELL_NAME, self.SUPPORTED_OS, context)

        session_pool_size = int(resource_config.sessions_concurrency_limit)
        self._cli = get_cli(session_pool_size)
        return 'Finished initializing'

    def restore(self, context, cancellation_context, path, configuration_type, restore_method):
        """
        Restores a configuration file
        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str path: The path to the configuration file, including the configuration file name.
        :param str restore_method: Determines whether the restore should append or override the current configuration.
        :param str configuration_type: Specify whether the file should update the startup or running config.
        """
        pass

    def save(self, context, cancellation_context, folder_path, configuration_type):
        """
        Creates a configuration file and saves it to the provided destination
        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str configuration_type: Specify whether the file should update the startup or running config. Value can one
        :param str folder_path: The path to the folder in which the configuration file will be saved.
        :return The configuration file name.
        :rtype: str
        """
        pass

    def load_firmware(self, context, cancellation_context, path):
        """
        Upload and updates firmware on the resource
        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param str path: path to tftp server where firmware file is stored
        """
        pass

    def run_custom_command(self, context, custom_command):
        """Executes a custom command on the device

        :param ResourceCommandContext context: The context object for the command with resource and
            reservation info
        :param str custom_command: The command to run
        :return: the command result text
        :rtype: str
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        resource_config = create_resource_from_context(self.SHELL_NAME, self.SUPPORTED_OS, context)
        cli_handler = CliHandler(self._cli, resource_config, logger, api)

        command_operations = RunCommandRunner(logger, cli_handler)
        return command_operations.run_custom_command(parse_custom_commands(custom_command))

    def run_custom_config_command(self, context, custom_command):
        """Executes a custom command on the device in configuration mode

        :param ResourceCommandContext context: The context object for the command with resource and
            reservation info
        :param str custom_command: The command to run
        :return: the command result text
        :rtype: str
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        resource_config = create_resource_from_context(self.SHELL_NAME, self.SUPPORTED_OS, context)
        cli_handler = CliHandler(self._cli, resource_config, logger, api)

        command_operations = RunCommandRunner(logger, cli_handler)
        return command_operations.run_custom_config_command(parse_custom_commands(custom_command))

    def shutdown(self, context, cancellation_context):
        """
        Sends a graceful shutdown to the device
        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        """
        pass

    # </editor-fold>

    # <editor-fold desc="Orchestration Save and Restore Standard">
    def orchestration_save(self, context, cancellation_context, mode, custom_params):
        """
        Saves the Shell state and returns a description of the saved artifacts and information
        This command is intended for API use only by sandbox orchestration scripts to implement
        a save and restore workflow
        :param ResourceCommandContext context: the context object containing resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str mode: Snapshot save mode, can be one of two values 'shallow' (default) or 'deep'
        :param str custom_params: Set of custom parameters for the save operation
        :return: SavedResults serialized as JSON
        :rtype: OrchestrationSaveResult
        """

        # See below an example implementation, here we use jsonpickle for serialization,
        # to use this sample, you'll need to add jsonpickle to your requirements.txt file
        # The JSON schema is defined at: https://github.com/QualiSystems/sandbox_orchestration_standard/blob/master/save%20%26%20restore/saved_artifact_info.schema.json
        # You can find more information and examples examples in the spec document at https://github.com/QualiSystems/sandbox_orchestration_standard/blob/master/save%20%26%20restore/save%20%26%20restore%20standard.md
        '''
        # By convention, all dates should be UTC
        created_date = datetime.datetime.utcnow()

        # This can be any unique identifier which can later be used to retrieve the artifact
        # such as filepath etc.

        # By convention, all dates should be UTC
        created_date = datetime.datetime.utcnow()

        # This can be any unique identifier which can later be used to retrieve the artifact
        # such as filepath etc.
        identifier = created_date.strftime('%y_%m_%d %H_%M_%S_%f')

        orchestration_saved_artifact = OrchestrationSavedArtifact('REPLACE_WITH_ARTIFACT_TYPE', identifier)

        saved_artifacts_info = OrchestrationSavedArtifactInfo(
            resource_name="some_resource",
            created_date=created_date,
            restore_rules=OrchestrationRestoreRules(requires_same_resource=True),
            saved_artifact=orchestration_saved_artifact)

        return OrchestrationSaveResult(saved_artifacts_info)
        '''
        pass

    def orchestration_restore(self, context, cancellation_context, saved_artifact_info, custom_params):
        """
        Restores a saved artifact previously saved by this Shell driver using the orchestration_save function
        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param CancellationContext cancellation_context: Object to signal a request for cancellation. Must be enabled in drivermetadata.xml as well
        :param str saved_artifact_info: A JSON string representing the state to restore including saved artifacts and info
        :param str custom_params: Set of custom parameters for the restore operation
        :return: None
        """
        '''
        # The saved_details JSON will be defined according to the JSON Schema and is the same object returned via the
        # orchestration save function.
        # Example input:
        # {
        #     "saved_artifact": {
        #      "artifact_type": "REPLACE_WITH_ARTIFACT_TYPE",
        #      "identifier": "16_08_09 11_21_35_657000"
        #     },
        #     "resource_name": "some_resource",
        #     "restore_rules": {
        #      "requires_same_resource": true
        #     },
        #     "created_date": "2016-08-09T11:21:35.657000"
        #    }

        # The example code below just parses and prints the saved artifact identifier
        saved_details_object = json.loads(saved_details)
        return saved_details_object[u'saved_artifact'][u'identifier']
        '''
        pass

    # </editor-fold>

    # <editor-fold desc="Connectivity Provider Interface (Optional)">

    '''
    # The ApplyConnectivityChanges function is intended to be used for using switches as connectivity providers
    # for other devices. If the Switch shell is intended to be used a DUT only there is no need to implement it

    def ApplyConnectivityChanges(self, context, request):
        """
        Configures VLANs on multiple ports or port-channels
        :param ResourceCommandContext context: The context object for the command with resource and reservation info
        :param str request: A JSON object with the list of requested connectivity changes
        :return: a json object with the list of connectivity changes which were carried out by the switch
        :rtype: str
        """

        return apply_connectivity_changes(request=request,
                                          add_vlan_action=lambda x: ConnectivitySuccessResponse(x,'Success'),
                                          remove_vlan_action=lambda x: ConnectivitySuccessResponse(x,'Success'))



    '''

    # </editor-fold>

    # <editor-fold desc="Discovery">

    @GlobalLock.lock
    def get_inventory(self, context):
        """Discovers the resource structure and attributes.

        :param AutoLoadCommandContext context: the context the command runs on
        :return Attribute and sub-resource information for the Shell resource
        :rtype: AutoLoadDetails
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        resource_config = create_resource_from_context(self.SHELL_NAME, self.SUPPORTED_OS, context)
        snmp_handler = SnmpHandler(resource_config, logger, api, None)  # fixme cli_handler

        autoload_operations = AutoloadRunner(resource_config, logger, snmp_handler)
        logger.info('Autoload started')
        response = autoload_operations.discover()
        logger.info('Autoload completed')
        return response

    # </editor-fold>

    def health_check(self, context):
        """Checks if the device is up and connectable

        :param ResourceCommandContext context: ResourceCommandContext object with all Resource
            Attributes inside
        :return: Success or fail message
        :rtype: str
        """

        logger = get_logger_with_thread_id(context)
        api = get_api(context)

        resource_config = create_resource_from_context(self.SHELL_NAME, self.SUPPORTED_OS, context)
        cli_handler = CliHandler(self._cli, resource_config, logger, api)

        state_operations = StateRunner(logger, api, resource_config, cli_handler)
        return state_operations.health_check()

    def cleanup(self):
        """
        Destroy the driver session, this function is called everytime a driver instance is destroyed
        This is a good place to close any open sessions, finish writing to log files
        """
        pass
