#!/usr/bin/env python3
import os

import aws_cdk as cdk

from app.root_stack import RootStack

app = cdk.App()
RootStack(
    app,
    "WorkRamp-Stack-{}".format(os.environ.get("ENVIRONMENT", "dev")),
)

app.synth()
