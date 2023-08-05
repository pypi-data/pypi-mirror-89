import json
import logging
from urllib.parse import urlencode
from urllib.request import urlopen

import zope.interface
from certbot import interfaces
from certbot.plugins import dns_common

logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """ISPManager dns-01 authenticator plugin"""

    description = "Obtain a certificate using a DNS TXT record in ISPManager."
    problem = "a"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add, default_propagation_seconds=10) -> None:
        """Adds the ISPManager credentials path to arguments."""
        super().add_parser_arguments(add, default_propagation_seconds)
        add('credentials', type=str, help='The ISPManager credentials INI file.')

    def more_info(self) -> str:
        """Returns description of the class as more info."""
        return self.description

    def _setup_credentials(self) -> None:
        self.credentials = self._configure_credentials(
            'credentials',
            'The ISPManager credentials INI file.',
            {
                'url': 'ISPManager URL.',
                'username': 'ISPManager username.',
                'password': 'ISPManager password.',
                'dns_domain': 'Domain name to do the lookups on host records.',
            }
        )

    def _perform(self, domain, validation_name, validation):
        client = self._get_ispmanager_client()
        client.add_dns_record(
            domain=self.credentials.conf("dns_domain"),
            name=validation_name,
            value=validation,
            rtype='txt',
            ttl=self.conf('propagation-seconds'),
        )

    def _cleanup(self, domain, validation_name, validation):
        client = self._get_ispmanager_client()

        client.delete_dns_record(
            domain=self.credentials.conf("dns_domain"),
            record=f'{validation_name}. TXT  {validation}'
        )

    def _get_ispmanager_client(self) -> '_ISPManagerClient':
        return _ISPManagerClient(
            self.credentials.conf("url"),
            self.credentials.conf("username"),
            self.credentials.conf("password"),
        )


class _ISPManagerClient:
    """
    Doc: https://docs.ispsystem.com/ispmanager-lite/developer-section/ispmanager-api#ISPmanagerAPI-WWW-domains
    https://docs.ispsystem.com/ispmanager-lite/developer-section/guide-to-ispsystem-software-api
    """
    def __init__(self, url: str, username: str, password: str):
        self.url = url
        self.auth_session_id: str = self.authorize(username, password)

    def process_api(self, params: dict) -> dict:
        params.update({
            'auth': self.auth_session_id,
            'out': 'json',
        })

        data = urlopen(f'{self.url}?{urlencode(params)}')
        out = json.load(data)['doc']

        try:
            return out['elem']
        except KeyError:
            return out

    def authorize(self, username, password) -> str:
        params = urlencode({
            'func': 'auth',
            'out': 'json',
            'username': username,
            'password': password,
        })
        data = urlopen(f"{self.url}?{params}")
        out = json.load(data)['doc']

        if 'authfail' in out:
            raise RuntimeError('Authorization error, check your credentials')

        return out['auth']['$id']

    def logout(self):
        params = {
            'func': 'session.delete',
            'elid': self.auth_session_id,
        }

        data = urlopen('%s?%s' % (self.url, params))
        out = json.load(data)

        if out["result"] == "OK":
            return True
        else:
            raise RuntimeError('Logout failed!')

    def add_dns_record(self, domain: str, name: str, value: str, rtype: str, ttl: int = 3600):
        """
        Removes the txt record.

        API func: domain.record.delete
        elid — one or more object's unique identifiers comma-delimited with space ", ".
        The unique identifiers is the rkey element of domain.record function.

        Success resp:

        ```
        {
          "doc": {
            "$lang": "en",
            "$func": "domain.record.delete",
            "$binary": "\\/ispmgr",
            "$host": "https:\\/\\/endpoint.ru",
            "$themename": "orion",
            "$theme": "\\/manimg\\/orion\\/",
            "$css": "main.css",
            "$logo": "logo.png",
            "$logolink": "https:\\/\\/www.smartape.ru",
            "$favicon": "favicon.ico",
            "$localdir": "local_e11575d5f303\\/",
            "$features": "d6060f75828e823f56064652661a22070",
            "$notify": "2",
            "ok": {},
            "saved_filters": {},
            "tips": {
              "tip": {
                "$": "help_links"
              }
            },
            "tparams": {
              "elid": {
                "$": "pop.nev.is. A  185.9.147.250"
              },
              "func": {
                "$": "domain.record.delete"
              },
              "out": {
                "$": "xjson"
              },
              "plid": {
                "$": "nev.is"
              }
            }
          }
        }
        ```
        """
        params = {
            'sok': 'ok',
            'plid': domain,
            'func': 'domain.record.edit',
            'name': f'{name}.',
            'value': value,
            'rtype': rtype,
            'ttl': ttl,

        }

        print(f'Adding DNS record: {params}')

        return self.process_api(params)

    def delete_dns_record(self, domain: str, record: str):
        """
        Removes the txt record.

        API func: domain.record.delete
        elid — one or more object's unique identifiers comma-delimited with space ", ".
        The unique identifiers is the rkey element of domain.record function.

        Success resp:

        ```
        {
          "doc": {
            "$lang": "en",
            "$func": "domain.record.delete",
            "$binary": "\\/ispmgr",
            "$host": "https:\\/\\/endpoint.ru",
            "$themename": "orion",
            "$theme": "\\/manimg\\/orion\\/",
            "$css": "main.css",
            "$logo": "logo.png",
            "$logolink": "https:\\/\\/www.endpoint.ru",
            "$favicon": "favicon.ico",
            "$localdir": "local_e11575d5f303\\/",
            "$features": "d6060f75828e823f56064652661a22070",
            "$notify": "2",
            "ok": {},
            "saved_filters": {},
            "tips": {
              "tip": {
                "$": "help_links"
              }
            },
            "tparams": {
              "elid": {
                "$": "pop.nev.is. A  185.9.147.250"
              },
              "func": {
                "$": "domain.record.delete"
              },
              "out": {
                "$": "xjson"
              },
              "plid": {
                "$": "nev.is"
              }
            }
          }
        }
        ```
        """
        params = {
            'plid': domain,
            'func': 'domain.record.delete',
            'elname': record,
            'elid': record,
        }

        print(f'Deleting DNS record: {params}')

        return self.process_api(params)
