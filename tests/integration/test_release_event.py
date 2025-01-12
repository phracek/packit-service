import json

import pytest
from flexmock import flexmock
from github import Github

from ogr.services.github import GithubProject

from packit.api import PackitAPI
from packit.config import JobTriggerType
from packit.local_project import LocalProject

from packit_service.config import Config
from packit_service.constants import SANDCASTLE_WORK_DIR
from tests.spellbook import DATA_DIR
from packit_service.worker.jobs import SteveJobs
from packit_service.worker.whitelist import Whitelist


@pytest.fixture()
def release_event():
    return json.loads((DATA_DIR / "webhooks" / "github_release_event.json").read_text())


def test_dist_git_push_release_handle(release_event):
    packit_yaml = (
        "{'specfile_path': '', 'synced_files': []"
        ", jobs: [{trigger: release, job: propose_downstream, metadata: {targets:[]}}]}"
    )
    flexmock(Github, get_repo=lambda full_name_or_id: None)
    flexmock(
        GithubProject,
        get_file_content=lambda path, ref: packit_yaml,
        full_repo_name="packit-service/hello-world",
    )
    flexmock(LocalProject, refresh_the_arguments=lambda: None)
    flexmock(Whitelist, check_and_report=True)
    steve = SteveJobs()
    flexmock(SteveJobs, _is_private=False)
    config = Config()
    config.command_handler_work_dir = SANDCASTLE_WORK_DIR
    flexmock(Config).should_receive("get_service_config").and_return(config)
    # it would make sense to make LocalProject offline
    flexmock(PackitAPI).should_receive("sync_release").with_args(
        dist_git_branch="master", version="0.3.0", create_pr=False
    ).once()

    results = steve.process_message(release_event)
    assert "propose_downstream" in results.get("jobs", {})
    assert results.get("jobs", {}).get("propose_downstream", {}).get("success")
    assert results["trigger"] == str(JobTriggerType.release)
