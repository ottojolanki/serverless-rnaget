#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

from serverless_rnaget.gateway.api import API as RNAGetAPI


app = cdk.App()

RNAGetAPI(
    app,
    'RNAGetAPIStack',
    env=cdk.Environment(account='618537831167', region='us-west-2'),
)

app.synth()
