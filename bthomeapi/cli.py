import click
import logging

import json
from .client import ApiClient

from pprint import pprint

from .config import Config
from .utils import setup_logging

logger = logging.getLogger(__name__)

WAPIP="192.168.0.27"

@click.group()
@click.option("-d", "--debug", default=False, is_flag=True)
@click.pass_context
def main(ctx, debug):
    setup_logging(False, debug)
    ctx.ensure_object(dict)
    ctx.obj['config'] = Config()
    

@main.command()
def test():
    client = ApiClient(WAPIP, "admin", "gcn7pne6ce")
    client.login()
    actions =  [
        {
            'id': 0,
            'method': 'getValue',
            'options': {
                'capability-flags': {
                    'interface': True
                }
            },
            'xpath': "Device/UserAccounts/Users/User[Login='admin']/Role"
        }
    ]
    result = client.action(actions)
    pprint(result)

  



@main.command()
def decode():
    input = "{\"request\":{\"id\":1,\"session-id\":272131570,\"priority\":false,\"actions\":[{\"id\":0,\"method\":\"getValue\",\"xpath\":\"Device/UserAccounts/Users/User[Login='admin']/Role\",\"options\":{\"capability-flags\":{\"interface\":true}}}],\"cnonce\":3375479880,\"auth-key\":\"b5ba08133fe052f4ec5aa168fb5d0d28\"}}"
    # input = "{\"request\":{\"id\":0,\"session-id\":\"0\",\"priority\":true,\"actions\":[{\"id\":0,\"method\":\"logIn\",\"parameters\":{\"user\":\"guest\",\"persistent\":\"true\",\"session-options\":{\"nss\":[{\"name\":\"gtw\",\"uri\":\"http://sagemcom.com/gateway-data\"}],\"language\":\"ident\",\"context-flags\":{\"get-content-name\":true,\"local-time\":true},\"capability-depth\":2,\"capability-flags\":{\"name\":true,\"default-value\":false,\"restriction\":true,\"description\":false},\"time-format\":\"ISO_8601\"}}}],\"cnonce\":2818586228,\"auth-key\":\"de0ec9c448f13ddd6a07ef0270b98b7d\"}}"
    #input="{\"request\":{\"id\":1,\"session-id\":1186893318,\"priority\":false,\"actions\":[{\"id\":0,\"method\":\"getValue\",\"xpath\":\"Device/IP/Interfaces/Interface[Alias=\\\"IP_BR_LAN\\\"]/IPv6Addresses/IPv6Address/IPAddress\",\"options\":{\"capability-flags\":{\"interface\":true}}},{\"id\":1,\"method\":\"getValue\",\"xpath\":\"Device/DNS/Client/HostName\",\"options\":{\"capability-flags\":{\"interface\":true}}},{\"id\":2,\"method\":\"getValue\",\"xpath\":\"Device/DeviceInfo/ProductClass\",\"options\":{\"capability-flags\":{\"interface\":true}}},{\"id\":3,\"method\":\"getValue\",\"xpath\":\"Device/DNS/Client/LocalDomains\",\"options\":{\"capability-flags\":{\"interface\":true}}},{\"id\":4,\"method\":\"getValue\",\"xpath\":\"Device/Managers/NetworkData/IpLan\",\"options\":{\"capability-flags\":{\"interface\":true}}},{\"id\":5,\"method\":\"getValue\",\"xpath\":\"Device/IP/Interfaces/Interface[Alias='IP_DATA']/Status\",\"options\":{\"capability-flags\":{\"interface\":true}}},{\"id\":6,\"method\":\"getValue\",\"xpath\":\"Device/Services/DeviceConfig/ConnectionHURLPageEnable\",\"options\":{\"capability-flags\":{\"interface\":true}}},{\"id\":7,\"method\":\"getValue\",\"xpath\":\"Device/Services/DeviceConfig/EnableBridgedMode\",\"options\":{\"capability-flags\":{\"interface\":true}}}],\"cnonce\":1626878869,\"auth-key\":\"fd09ab3b17a6300f3002f5df01a7a6ce\"}}"
    pprint(json.loads(input))