from __future__ import print_function
from swimlane_platform.environment_updater.environment_updater_base import EnvironmentUpdaterBase
from swimlane_platform.lib import Configuration, names, info_function_start_finish, VersionValidator, \
    ContainingDirectoryExistsValidator


class EnvironmentUpdaterAudit(EnvironmentUpdaterBase):

    @info_function_start_finish('Swimlane audit.')
    def run(self):
        # type: () -> None
        """
        Main method.
        """
        self.docker_helper.containers_exists_validate(names.SW_API, names.SW_MONGO)
        local, remote = self.parse_file_location(self.config.args.report_file)
        command = ['audit', '-f', remote]
        if self.config.args.version:
            command.extend(['-v', self.config.args.version])
        volumes = {local: {'bind': self.REPORT_FOLDER, 'mode': 'Z'}}
        # Not pulled up to parent, because in the future EU needs to be fixed.
        self.get_admin_connection()
        self.run_image_command(command, volumes)


def run(config):
    # type: (Configuration) -> None
    questions = [
        {
            'type': 'input',
            'name': 'report_file',
            'message': 'Specify the path to the output audit report file.',
            'validate': ContainingDirectoryExistsValidator
        },
        {
            'type': 'input',
            'name': 'version',
            'message': 'Specify the version to audit.',
            'validate': VersionValidator
        }
    ]
    config.collect(questions)
    audit = EnvironmentUpdaterAudit(config)
    audit.run()
