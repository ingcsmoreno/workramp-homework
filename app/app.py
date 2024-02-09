#!/usr/bin/env python3
# import os

import aws_cdk as cdk

from app.vpc_stack import VPCStack

# deployment-env=cdk.Environment(
#    account=os.environ.get("CDK_DEPLOY_ACCOUNT", os.environ["CDK_DEFAULT_ACCOUNT"]),
#    region=os.environ.get("CDK_DEPLOY_REGION", os.environ["CDK_DEFAULT_REGION"])
# )

app = cdk.App()
VPCStack(
    app,
    "WorkRamp-VPC-Stack",
    # env=deployment-env
)

app.synth()
