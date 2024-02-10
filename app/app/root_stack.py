from aws_cdk import Stack, CfnOutput
from constructs import Construct

from app.vpc_stack import VPCStack
from app.bastion_stack import BastionStack
from app.service_stack import ServiceStack


class RootStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        network = VPCStack(
            self,
            "VPC",
        )
        bastion = BastionStack(self, "Bastion", network.vpc, network.frontSG)

        service = ServiceStack(self, "Service", network.vpc, network.backSG)

        # Outputs

        CfnOutput(self, "VPCId", value=network.vpc.vpc_id)
        CfnOutput(self, "FrontSGId", value=network.frontSG.security_group_id)
        CfnOutput(self, "BackSGId", value=network.backSG.security_group_id)

        CfnOutput(self, "BastionPublicIP", value=bastion.bastion.instance_public_ip)
        CfnOutput(
            self, "BastionPrivateKey", value=bastion.key_pair.private_key.parameter_name
        )

        CfnOutput(self, "ServicePrivateIP", value=service.instance.instance_private_ip)
