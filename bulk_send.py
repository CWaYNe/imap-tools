#!/usr/bin/env python

import argparse
import os
import re
import random
import time

from faker import Faker


class SendEmail():

    smtp_send_template = """helo 0
mail from:{sender_email}
{receiver_list}data
Subject:{subject}
{header_list}
{email_body}
.
quit
"""

    def __init__(self, body_max_chars=500, randomSender=True):
        self.use_random_sender = randomSender
        self.body_max_chars = body_max_chars
        self.fake = Faker('zh_TW')

    def bulk_send(self, to, cc=[], bcc=[], count=1):
        sender = self.fake.email()
        for _ in range(count):
            if self.use_random_sender:
                sender = self.fake.email()

            subject = self.fake.sentence()
            body = self.fake.text(max_nb_chars=self.body_max_chars)

            self.send(sender, to, subject, body, cc, bcc)

    def send(self, sender_email, to, subject='', body='', cc=[], bcc=[]):
        rcpt = []
        header = []
        header.append('From: %s' % sender_email)
        if isinstance(to, (str,)):
            rcpt.append(to)
            header.append('To: %s' % to)
        elif isinstance(to, (list,)):
            rcpt.extend(to)
            header.append('To: %s' % (",".join(to)))
            to = ",".join(to)
        else:
            raise ValueError('Error parameter to, expect list of str or str')

        if cc:
            if isinstance(cc, (str,)):
                header.append('Cc: %s' % cc)
                rcpt.append(cc)
            elif isinstance(cc, (list,)):
                header.append('Cc: %s' % (",".join(cc)))
                rcpt.extend(cc)

        if bcc:
            if isinstance(bcc, (str,)):
                header.append('Bcc: %s' % bcc)
                rcpt.append(bcc)
            elif isinstance(bcc, (list,)):
                header.append('Bcc: %s' % (",".join(bcc)))
                rcpt.extend(bcc)

        cmd = ( SendEmail.smtp_send_template.format(
            sender_email=sender_email, receiver_list='rcpt to:'.join([rcpt_to + '\n' for rcpt_to in rcpt]),
            subject=subject, email_body= body, header_list='\n'.join(header)
            )
        )

        os.system('echo "%s" | nc 0 25' % cmd)
        # print( cmd )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bulk email sending tool')
    parser.add_argument('-t', '--to', nargs='+', required=True, help='<required> email receiver')
    parser.add_argument('-c', '--cc', nargs='+', default=[])
    parser.add_argument('-b', '--bcc', nargs='+', default=[])
    parser.add_argument('-n', '--number', type=int, default=1, help='To send email count')
    parser.add_argument('-m', '--body_max_chars', type=int, default=500, help='size of each email body')
    parser.add_argument('-u', '--use_same_sender', action='store_true', help='use same sender for each email')

    args = parser.parse_args()

    s = SendEmail(body_max_chars=args.body_max_chars, randomSender=not args.use_same_sender)
    s.bulk_send(to=args.to, cc=args.cc, bcc=args.bcc, count=args.number)
