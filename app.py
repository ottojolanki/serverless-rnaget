#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

from serverless_rnaget.serverless_rnaget_stack import RnagetStack


app = cdk.App()

RnagetStack(
    app,
    'RnagetStack',
    env=cdk.Environment(account='618537831167', region='us-west-2'),
)

app.synth()
