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


SERVICE_CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "debug": {"type": "boolean"},
        "dry_run": {"type": "boolean"},
        "fas_user": {"type": "string"},
        "keytab_path": {"type": "string"},
        "pagure_user_token": {"type": "string"},
        "pagure_fork_token": {"type": "string"},
        "deployment": {"type": "string"},
        "github_app_id": {"type": "string"},
        "github_app_cert_path": {"type": "string"},
        "webhook_secret": {"type": "string"},
        "testing_farm_secret": {"type": "string"},
        "validate_webhooks": {"type": "boolean"},
    },
    "required": ["deployment", "github_app_id", "github_app_cert_path"],
}
