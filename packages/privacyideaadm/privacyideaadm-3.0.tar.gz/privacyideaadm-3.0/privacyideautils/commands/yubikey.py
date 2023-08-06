# -*- coding: utf-8 -*-
#
#  2020-04-13 Cornelius Kölbel <cornelius.koelbel@netknights.it>
#             migrate to click
#
# This code is free software; you can redistribute it and/or
# modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
# License as published by the Free Software Foundation; either
# version 3 of the License, or any later version.
#
# This code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU AFFERO GENERAL PUBLIC LICENSE for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import click
import datetime
import logging
from privacyideautils.clientutils import (showresult,
                                          dumpresult,
                                          privacyideaclient,
                                          __version__)
from privacyideautils.clientutils import PrivacyIDEAClientError
from ykman.piv import (
    PivController, ALGO, OBJ, SLOT, PIN_POLICY, TOUCH_POLICY,
    DEFAULT_MANAGEMENT_KEY, generate_random_management_key)
from ykman.driver_ccid import APDUError, SW
from ykman.cli.util import UpperCaseChoice, YkmanContextObject


@click.group()
@click.pass_context
def yubikey(ctx):
    """
    Create certificates on yubikeys
    """
    ctx.obj = YkmanContextObject()
    dev = _run_cmd_for_single(ctx, subcmd.name, transports, reader)
    ctx.call_on_close(dev.close)
    ctx.obj.add_resolver('dev', dev)

    try:
        ctx.obj['controller'] = PivController(ctx.obj['dev'].driver)
    except APDUError as e:
        if e.sw == SW.NOT_FOUND:
            ctx.fail("The PIV application can't be found on this YubiKey.")
        raise


from ykman.piv import ALGO
from ykman.cli.util import EnumChoice
from ykman.cli.piv import click_parse_management_key

@yubikey.command()
@click.pass_context
@click.option("--ca", help="Specify the CA where you want to send the CSR to.")
@click.option("--user", help="The user to whom the certificate should be assigned.")
@click.option("--realm", help="The realm of the user to whom the certificate should be assigned.")
@click.option("--slot", help="The slot where to create the private key.",
              default="9a", show_default=True)
@click.option('-a', '--algorithm', help='Algorithm to use in key generation.',
              type=EnumChoice(ALGO), default=ALGO.RSA2048.name, show_default=True)
@click.option('-m', '--management-key',
              help='The management key.', callback=click_parse_management_key)
@click.option('-P', '--pin', help='PIN code.')
def create(ctx, slot, ca, user, realm, algorithm, management_key, pin):
    """
    Create a certificate signing request on the Yubikey and send it to the privacyIDEA server.
    """
    client = ctx.obj["pi_client"]
    param = {"type": "certificate",
             "user": user}

    if ca:
        param["ca"] = ca
    if user:
        param["user"] = user
    if realm:
        param["realm"] = realm



    try:
        resp = client.inittoken(param)
        print("result: {0!s}".format(resp.status))
        showresult(resp.data)
        if resp.status == 200:
            if not param.get("serial"):
                print("serial: {0!s}".format(resp.data.get("detail", {}).get("serial")))
    except PrivacyIDEAClientError as e:
        print(e)

