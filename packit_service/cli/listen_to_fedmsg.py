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

"""
Watch for new upstream releases.
"""
import logging

import click

from packit_service.celerizer import celery_app
from packit_service.fed_mes_consume import Consumerino
from packit_service.worker.fedmsg_handlers import do_we_process_fedmsg_topic

logger = logging.getLogger(__name__)


@click.command("listen-to-fedmsg")
@click.argument("message-id", nargs=-1)
def listen_to_fedmsg(message_id):
    """
    Listen to events on fedmsg and process them.

    if MESSAGE-ID is specified, process only the selected messages
    """
    consumerino = Consumerino()

    if message_id:
        for msg_id in message_id:
            fedmsg_dict = consumerino.fetch_fedmsg_dict(msg_id)
            logger.debug(f"Processing {fedmsg_dict}")
            celery_app.send_task(
                name="task.steve_jobs.process_message", kwargs={"event": fedmsg_dict}
            )
    else:
        for topic, msg in consumerino.yield_all_messages():
            if do_we_process_fedmsg_topic(topic):
                logger.debug(f"Processing topic {topic}, msg {msg}")
                celery_app.send_task(
                    name="task.steve_jobs.process_message",
                    kwargs={"event": msg, "topic": topic},
                )
