from aws_cdk import CfnOutput, Stack, aws_ec2 as ec2
from constructs import Construct


class BastionStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bastionSG = ec2.SecurityGroup(
            self,
            "BastionSecurityGroup",
            vpc=vpc,
            description="Allow SSH access",
            allow_all_outbound=True,
            disable_inline_rules=True,
        )
        bastionSG.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "allow SSH access from the world"
        )

        self.bastion = ec2.BastionHostLinux(
            self,
            "bastionServer",
            vpc=vpc,
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=bastionSG,
            instance_type=ec2.InstanceType(instance_type_identifier="t2.micro"),
        )

        CfnOutput(self, "BastionPublicIP", value=self.bastion.instance_public_ip)
