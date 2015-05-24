from paypalrestsdk.resource import List, Find, Create, Delete, Update, Replace, Resource, Post
from paypalrestsdk.api import default as default_api
import paypalrestsdk.util as util
import binascii
from base64 import b64decode
import requests


class Webhook(Create, Find, List, Delete, Replace):
    """Exposes REST endpoints for creating and managing webhooks

    Usage::

        >>> web_profile = WebProfile.find("XP-3NWU-L5YK-X5EC-6KJM")
    """
    path = "/v1/notifications/webhooks/"

    def get_event_types(self, api=None):
        """Get the list of events types that are subscribed to a webhook
        """
        api = api or default_api()
        url = util.join_url(self.path, str(self['id']), 'event-types')
        return Resource(self.api.get(url), api=api)


class WebhookEvent(Find, List, Post):
    """Exposes REST endpoints for working with subscribed webhooks events
    """
    path = "/v1/notifications/webhooks-events/"

    def resend(self):
        """Specify a received webhook event-id to resend the event notification
        """
        return self.post('resend', {}, self)

    def get_resource(self):
        """Get the resource sent via the webhook event, e.g. Authorization, conveniently
         wrapped in the corresponding paypalrestsdk class
        """
        webhook_resource_type = self.resource_type
        klass = util.get_member(webhook_resource_type)
        resource = klass(self.resource.__dict__)
        return resource

    @staticmethod
    def _get_expected_sig(transmission_id, timestamp, webhook_id, event_body):
        """Get the input string to generate the HMAC signature
        """
        expected_sig = transmission_id + "|" + timestamp + "|" + webhook_id + "|" + str(binascii.crc32(event_body.encode('utf-8')) & 0xffffffff)
        return expected_sig

    @staticmethod
    def _get_cert(cert_url):
        """Fetches the paypal certificate used to sign the webhook event payload
        """
        from OpenSSL import crypto
        try:
            r = requests.get(cert_url)
            cert = crypto.load_certificate(crypto.FILETYPE_PEM, str(r.text))
            return cert
        except requests.exceptions.RequestException as e:
            print("Error retrieving PayPal certificate with url " + cert_url)
            print(e)

    @classmethod
    def verify(cls, transmission_id, timestamp, webhook_id, event_body, cert_url, actual_sig, auth_algo='sha1'):
        """Verify that the webhook payload received is from PayPal,
        unaltered and targeted towards correct recipient
        """
        from OpenSSL import crypto
        expected_sig = WebhookEvent._get_expected_sig(transmission_id, timestamp, webhook_id, event_body)
        cert = WebhookEvent._get_cert(cert_url)
        try:
            crypto.verify(cert, b64decode(actual_sig), expected_sig.encode('utf-8'), auth_algo)
            return True
        except Exception as e:
            print(e)
            return False


class WebhookEventType(List):
    """Exposes REST endpoint for listing available event types for webhooks
    """
    path = "/v1/notifications/webhooks-event-types/"
