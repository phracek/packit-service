# MIT License
#
# Copyright (c) 2018-2019 Red Hat, Inc.

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

import json

import pytest
from flexmock import flexmock

from tests.spellbook import DATA_DIR
from packit.api import PackitAPI
from packit_service.worker.jobs import SteveJobs
from packit_service.worker.handler import HandlerResults


@pytest.fixture()
def issue_comment_propose_update_event():
    return json.loads(
        (DATA_DIR / "webhooks" / "github_issue_propose_update.json").read_text()
    )


@pytest.fixture()
def issue_empty_comment_event():
    return json.loads(
        (DATA_DIR / "webhooks" / "github_issue_empty_comment.json").read_text()
    )


def test_issue_comment_propose_update_handler(
    mock_issue_comment_functionality, issue_comment_propose_update_event
):
    flexmock(PackitAPI).should_receive("sync_release").and_return(
        HandlerResults(success=True, details={})
    )
    steve = SteveJobs()
    flexmock(SteveJobs, _is_private=False)
    results = steve.process_message(issue_comment_propose_update_event)
    assert results.get("jobs", {})
    assert "pull_request_action" in results.get("jobs", {})
    assert "created" in results.get("event", {}).get("action", None)
    assert results.get("event", {}).get("issue_id", None) == 512
    assert "comment" in results.get("trigger", None)
    assert results.get("event", {}).get("comment", None) == "/packit propose-update"
    assert results.get("jobs", {}).get("pull_request_action", {}).get("success")
