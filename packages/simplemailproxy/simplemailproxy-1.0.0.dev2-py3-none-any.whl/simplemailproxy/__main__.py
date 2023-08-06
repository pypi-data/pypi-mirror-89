#!/usr/bin/env python
#
# Simple Mail Proxy
# Author: Ondrej Sika <ondrej@ondrejsika.com>
#

import smtpd
import smtplib
import argparse
import asyncore


parser = argparse.ArgumentParser(
    prog="python -m simplemailproxy",
    description="Simple mail proxy",
)
parser.add_argument(
    "--host",
    default="0.0.0.0",
    type=str,
    help="Listening host",
)
parser.add_argument(
    "--port",
    default=25,
    type=int,
    help="Listening port",
)
parser.add_argument(
    "domain_host_port",
    metavar="domain:host:port",
    type=str,
    nargs="+",
    help="Forward rule, example: foo.com:mx1.foo.com:25",
)


args = parser.parse_args()


CONFIG = {}
for domain_host_port in args.domain_host_port:
    domain, host, port = domain_host_port.split(":")
    CONFIG[domain] = (host, int(port))


def send(host, port, mailfrom, rcpttos, data):
    server = smtplib.SMTP(host, port)
    try:
        server.sendmail(mailfrom, rcpttos, data)
    finally:
        server.quit()


class SMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, *args, **kwargs):
        for rcptto in rcpttos:
            _, domain = rcptto.split("@")
            if not domain in CONFIG:
                continue
            host, port = CONFIG[domain]
            send(host, port, mailfrom, (rcptto,), data)


server = SMTPServer((args.host, args.port), None)
asyncore.loop()
