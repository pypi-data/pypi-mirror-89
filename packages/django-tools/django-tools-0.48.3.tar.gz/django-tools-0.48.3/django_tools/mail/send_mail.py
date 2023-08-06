"""
    mail util
    ~~~~~~~~~

    :copyleft: 2017-2018 by the django-tools team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import logging

from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string


log = logging.getLogger(__name__)


class SendMail:
    fail_silently = False

    def __init__(
        self,
        template_base,
        mail_context,
        subject,
        recipient_list,
        from_email=None,
        bcc=None,
        connection=None,
        attachments=None,
        headers=None,
        alternatives=None,
        cc=None,
        reply_to=None
    ):
        """
        Send a mail in txt and html format

        :param template_base: e.g.: /foo/bar.{ext}
        :param mail_context: django template context used to render the mail
        :param subject: email subject
        :param recipient_list: email recipient
        :param from_email: optional
        """
        self.template_base = template_base
        self.mail_context = mail_context
        self.subject = subject

        assert recipient_list, f"No recipient given: {recipient_list!r}"
        if isinstance(recipient_list, str):
            self.recipient_list = [recipient_list]
        else:
            self.recipient_list = recipient_list

        if from_email is None:
            self.from_email = settings.DEFAULT_FROM_EMAIL
        else:
            self.from_email = from_email

        self.bcc = bcc
        self.connection = connection
        self.attachments = attachments
        self.headers = headers
        self.alternatives = alternatives
        self.cc = cc
        self.reply_to = reply_to

    def send(self):
        html_message, text_message = self.render_mail()
        msg = self.create_text_and_html_mail(html_message, text_message)
        return self.send_mail(msg)

    def send_mail(self, msg):
        """
        Send created email.
        """
        return msg.send(fail_silently=self.fail_silently)

    def render_mail(self):
        if isinstance(self.template_base, (list, tuple)):
            template_base_list = self.template_base
            html_template = []
            text_template = []
            for template_base in template_base_list:
                html_template.append(template_base.format(ext='html'))
                text_template.append(template_base.format(ext='txt'))
        else:
            html_template = self.template_base.format(ext='html')
            text_template = self.template_base.format(ext='txt')

        html = render_to_string(html_template, self.mail_context)
        text = render_to_string(text_template, self.mail_context)
        return html, text

    def create_text_and_html_mail(self, html_message, text_message):
        msg = EmailMultiAlternatives(
            subject=self.subject,
            body=text_message,
            from_email=self.from_email,
            to=self.recipient_list,
            bcc=self.bcc,
            connection=self.connection,
            attachments=self.attachments,
            headers=self.headers,
            alternatives=self.alternatives,
            cc=self.cc,
            reply_to=self.reply_to
        )
        msg.attach_alternative(html_message, 'text/html')
        return msg
