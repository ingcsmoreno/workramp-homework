#!/usr/bin/env python3
# import os

import aws_cdk as cdk

# from app.vpc_stack import VPCStack
# from app.bastion_stack import BastionStack
from app.root_stack import RootStack

# deployment-env=cdk.Environment(
#    account=os.environ.get("CDK_DEPLOY_ACCOUNT", os.environ["CDK_DEFAULT_ACCOUNT"]),
#    region=os.environ.get("CDK_DEPLOY_REGION", os.environ["CDK_DEFAULT_REGION"])
# )

app = cdk.App()
RootStack(
    app,
    "WorkRamp-Stack",
    # env=deployment-env
)
# NETWORK = VPCStack(
#    app,
#    "WorkRamp-VPC-Stack",
#    # env=deployment-env
# )
# BASTION = BastionStack(
#    app,
#    "WorkRamp-Bastion-Stack",
#    NETWORK.vpc,
#    # env=deployment-env
# )

app.synth()
