import time
import logging
import importlib
import redis

from runners_manager.vm_creation.github_actions_api import GithubManager
from runners_manager.vm_creation.openstack import OpenstackManager
from runners_manager.runner.Manager import Manager
from runners_manager.runner.RedisManager import RedisManager
from settings.yaml_config import EnvSettings

logger = logging.getLogger("runner_manager")


def maintain_number_of_runner(runner_m: Manager, github_manager: GithubManager):
    while True:
        runners = github_manager.get_runners()
        logger.info(f"nb runners: {len(runners['runners'])}")
        logger.info(
            f"offline: {len([e for e in runners['runners'] if e['status'] == 'offline'])}"
        )

        logger.debug(runners)
        runner_m.update_all_runners(runners['runners'])

        time.sleep(10)


def init(settings: dict, args: EnvSettings):
    logger.info('Initialisation')
    importlib.import_module(settings['python_config'])
    openstack_manager = OpenstackManager(project_name=settings['cloud_nine_tenant'],
                                         region=settings['cloud_nine_region'],
                                         token=args.cloud_nine_token,
                                         username=args.cloud_nine_user,
                                         password=args.cloud_nine_password,
                                         redhat_username=args.redhat_username,
                                         redhat_password=args.redhat_password,
                                         ssh_keys=settings['allowed_ssh_keys'])
    github_manager = GithubManager(organization=settings['github_organization'],
                                   token=args.github_token)
    r = redis.Redis(host=settings['redis']['host'],
                    port=settings['redis']['port'],
                    password=args.redis_password)
    redis_database = RedisManager(r)
    runner_m = Manager(settings, openstack_manager, github_manager, redis_database)
    return runner_m, redis_database, github_manager, openstack_manager


def main(settings: dict, args: EnvSettings):
    runner_m, redis_database, github_manager, openstack_manager = init(settings, args)
    maintain_number_of_runner(runner_m, github_manager)
