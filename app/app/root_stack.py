from aws_cdk import Stack
from constructs import Construct

from app.vpc_stack import VPCStack
from app.bastion_stack import BastionStack


class RootStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        network = VPCStack(
            self,
            "VPC",
        )
        BastionStack(
            self,
            "Bastion",
            network.vpc,
        )
