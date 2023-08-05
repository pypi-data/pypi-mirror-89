from os import path, makedirs
from uuid import uuid4
from docker.errors import ContainerError
from typing import Union, List, Dict, Tuple
from swimlane_platform.lib.db_configuration import DbConfiguration
from swimlane_platform.lib import names, DockerManager, DockerImage, \
    debug_function_args, debug_function_return, BaseWithLog,  parse_env_variables_to_dict
from swimlane_platform.lib.args_config_questions import Configuration


class EnvironmentUpdaterBase(BaseWithLog):
    APP_NAME = 'EnvironmentUpdater'

    @debug_function_args
    def __init__(self, config):
        # type: (Configuration) -> None
        super(EnvironmentUpdaterBase, self).__init__(config)
        assert config.args.version
        self.REPORT_FOLDER = '/report'
        self.docker_helper = DockerManager(self.logger)
        self.docker_image = DockerImage(image_name='swimlane/swimlane-environmentupdater',
                                        version=self.config.args.version,
                                        is_dev=self.config.args.dev)

    @staticmethod
    def make_tuple(equal_delimited_env):
        # type: (object) -> Tuple[str, str]
        """
        Makes a two value tuple from = delimited environment variable
        :param equal_delimited_env: environment variable
        :return: key, value tuple
        """
        spl = str(equal_delimited_env).split('=')
        return spl[0], '='.join(spl[1:])

    def get_image(self):
        # type: () -> None
        """
        Helper method to acquire image.
        """
        self.docker_helper.extract_or_pull_image(self.docker_image,
                                                 self.config.args.dev,
                                                 self.config.args.installer_is_offline,
                                                 self.config.args.extracted_files_folder)

    @debug_function_args
    def run_image_command(self, special_command, volumes):
        # type: (Union[str, List[str]], Dict) -> None
        """
        Runs docker run on image with some defaults. Network and Environment from API.
        :param special_command: Command
        :param volumes: Volumes to map to container
        """
        name = str(uuid4().hex)
        # noinspection PyBroadException
        try:
            # Override environment variables from API container with command line submitted.
            env_list = self.docker_helper.container_get_dotnet_env(names.SW_API)
            env = dict([self.make_tuple(e) for e in env_list])
            if self.config.args.environment:
                for arg_env in self.config.args.environment:
                    key, value = self.make_tuple(arg_env)
                    env[key] = value
            command = ['dotnet', 'EnvironmentUpdater.dll']
            command.extend(special_command)
            network = self.docker_helper.container_get_network_name(names.SW_API)
            logs = self.docker_helper.image_run_command(self.docker_image.full_name, command=command, name=name,
                                                        volumes=volumes, network=network, env=env)
            for log in logs:
                self.logger.info(log)
        except ContainerError as ex:
            self.logger.error('container.logs(): ' + str(ex.container.logs()))
            if not ex.stderr:
                ex.stderr = ex.container.logs()
            raise
        finally:
            self.docker_helper.container_remove(name)

    @debug_function_return
    @debug_function_args
    def parse_file_location(self, file_path):
        # type: (str) -> (str, str)
        """
        Parses local file path to remote container path and local folder path for mapping.
        :param file_path: File path of indicated local report file.
        :return: Local folder, remote file path
        """
        assert file_path
        local, name = path.split(file_path)
        remote = '/'.join([self.REPORT_FOLDER, name])
        if not path.exists(local):
            makedirs(local)
        return local, remote

    @debug_function_args
    def add_admin_to_env(self, uri):
        # type: (str) -> None
        """
        Adds submitted mongo admin connection string to configuration environment property.
        :param uri: Admin connection.
        """
        uri_env_var = '{key}={value}'.format(key=names.DOT_NET_ADMIN_CONN_KEY, value=uri)
        if 'environment' in self.config:
            self.config['environment'].append(uri_env_var)
        else:
            self.config['environment'] = [uri_env_var]
        self.logger.debug('Result - the environment = {value}'.format(value=self.config.args.environment))

    def get_admin_connection(self):
        # type: () -> None
        """
        Verifies existence of admin connection. If lacking asks appropriate questions.
        :return: None, admin connection added to self.config.args.environment
        """
        self.docker_helper.containers_exists_validate(names.SW_API)
        db_configuration = DbConfiguration(self.config)
        api_config = parse_env_variables_to_dict(self.docker_helper.container_get_dotnet_env(names.SW_API))
        if names.DOT_NET_ADMIN_CONN_KEY in api_config:
            return
        swimlane_connection_string = self.get_swimlane_connection_string(api_config)
        if not swimlane_connection_string:
            questions = [{
                'type': 'input',
                'name': 'mongo_admin_uri',
                'message': 'Please enter full MongoDB admin database connection URI. Example '
                           'mongodb://<user>:<password>@sw_mongo:27017/admin'
                           '?ssl=true&sslVerifyCertificate=false'.format(conf=names.DOT_NET_SWIMLANE_CONN_KEY)
            }]
            self.config.collect(questions)
            self.add_admin_to_env(self.config.args.mongo_admin_uri)
        else:
            questions = [
                {
                    'type': 'input',
                    'name': 'mongo_admin_user',
                    'message': 'What is the username for the MongoDB admin database?'
                },
                {
                    'type': 'password',
                    'name': 'mongo_admin_password',
                    'message': 'What is the password for the MongoDB admin database?'
                }]
            self.config.collect(questions)
            admin_uri = db_configuration.parse_mongo_uri(swimlane_connection_string)
            admin_uri['database'] = 'admin'
            admin_uri['username'] = self.config['mongo_admin_user']
            admin_uri['password'] = self.config['mongo_admin_password']
            self.add_admin_to_env(db_configuration.get_mongo_uri(admin_uri))

    @debug_function_return
    @debug_function_args
    def get_swimlane_connection_string(self, config):
        # type: (Dict[str, str]) -> Union[str, None]
        """
        Returns Swimlane connection either with SWIMLANE prefix or without
        :param config: DotNet environment variables.
        :return: Connection string or None, if not found
        """
        assert config
        result = config.get(names.DOT_NET_SWIMLANE_CONN_KEY)
        return result if result else config.get(names.DOT_NET_SWIMLANE_CONN_KEY.replace(names.SWIMLANE_PREFIX, ''))
