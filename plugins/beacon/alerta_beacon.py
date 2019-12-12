import logging
import os
import json
import requests
try:
      from alerta.plugins import app  # alerta >= 5.0
except ImportError:
      from alerta.app import app  # alerta < 5.0

from alerta.plugins import PluginBase

LOG = logging.getLogger('alerta.plugins.beacon')

BEACON_HEADERS = {
    'Content-Type': 'application/json'
}
BEACON_SEND_ON_ACK = os.environ.get('BEACON_SEND_ON_ACK') or app.config.get('BEACON_SEND_ON_ACK', False)
BEACON_SEVERITY_MAP = app.config.get('BEACON_SEVERITY_MAP', {})
BEACON_DEFAULT_SEVERITY_MAP = {'security': '#000000', # black
                              'critical': '#FF0000', # red
                              'major': '#FFA500', # orange
                              'minor': '#FFFF00', # yellow
                              'warning': '#1E90FF', #blue
                              'informational': '#808080', #gray
                              'debug': '#808080', # gray
                              'trace': '#808080', # gray
                              'ok': '#00CC00'} # green

class ServiceIntegration(PluginBase):

    def __init__(self, name=None):
        # override user-defined severities
        self._severities = BEACON_DEFAULT_SEVERITY_MAP
        self._severities.update(BEACON_SEVERITY_MAP)

        super(ServiceIntegration, self).__init__(name)

    def pre_receive(self, alert):
        return alert

    def post_receive(self, alert):
        return

    def status_change(self, alert, status, text, **kwargs):
        BEACON_WEBHOOK_URL = self.get_config('BEACON_WEBHOOK_URL', type=str, **kwargs)

        #if BEACON_SEND_ON_ACK == False or status not in ['ack', 'assign']:
            #return

        LOG.debug('Beacon alert: %s', alert)
        LOG.debug('Beacon status: %s', status)
        LOG.debug('Beacon text: %s', text)
        try:
            #payload = self._beacon_prepare_payload(alert, status, text, **kwargs)
            payload = alert

            LOG.debug('Beacon payload: %s', payload)
        except Exception as e:
            LOG.error('Exception formatting payload: %s\n%s' % (e, traceback.format_exc()))
            return

        try:
            r = requests.post(BEACON_WEBHOOK_URL,
                              data=json.dumps(payload), headers=BEACON_HEADERS, timeout=2)
        except Exception as e:
            raise RuntimeError("Beacon connection error: %s", e)

        LOG.debug('Beacon response: %s\n%s' % (r.status_code, r.text))
