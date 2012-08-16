"""
sentry_redflash.plugin
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 by David Szotten.
:license: MIT, see LICENSE for more details.
"""

import logging

from django import forms
from sentry.plugins import Plugin

import sentry_redflash
from sentry_redflash.client import RedFlashClient


logger = logging.getLogger('sentry.plugins.redflash')
MAX_LENGTH = 159


class RedflashOptionsForm(forms.Form):
    url = forms.CharField(help_text="Redflash server url.")
    key = forms.CharField(help_text="API key")
    group = forms.CharField(help_text="Redflash contact group to notify")


class RedflashPlugin(Plugin):
    author = 'David Szotten'
    author_url = 'https://github.com/davidszotten/sentry-redflash'
    title = 'Redflash'
    slug = 'redflash'
    conf_key = 'redflash'
    description = 'Send error notifications to Redflash.'
    version = sentry_redflash.VERSION
    project_conf_form = RedflashOptionsForm

    def post_process(self, group, event, is_new, is_sample, **kwargs):
        # only notify about new events
        if not is_new:
            return

        # only notify errors and higher. TODO: make this configurable?
        if event.level < logging.ERROR:
            return

        redflash_url = self.get_option('url', event.project)
        redflash_key = self.get_option('key', event.project)
        redflash_group = self.get_option('group', event.project)

        # make sure we are properly configured
        if not (redflash_url and redflash_key and redflash_group):
            return  # TODO: log error?

        # message title/description
        # from sentry:///templates/sentry/partial/_group.html
        if getattr(group, 'view', None):
            title = group.view
            message = group.message
        elif group.culprit:
            title = group.culprit
            message = group.message
        else:
            title = group.message
            message = ""

        notification = "%s\n%s" % (title, message)
        notification = notification.strip()
        if len(notification) > MAX_LENGTH:
            notification = notification[:(MAX_LENGTH - 3)] + "..."

        redflash_client = RedFlashClient(redflash_url, redflash_key)
        redflash_client.notify_group(redflash_group, notification)
