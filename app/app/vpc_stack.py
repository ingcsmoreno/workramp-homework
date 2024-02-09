from aws_cdk import CfnOutput, Stack, aws_ec2 as ec2
from constructs import Construct


class VPCStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(
            self,
            "VPC",
            availability_zones=["us-east-1a", "us-east-1b", "us-east-1c"],
            restrict_default_security_group=True,
            cidr="10.0.0.0/16",
            # Will create 2 groups in 3 AZs (6 subnets).
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC, name="Public", cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    name="Private",
                    cidr_mask=24,
                ),
            ],
            nat_gateways=1,
        )

        self.private_nacl = ec2.NetworkAcl(
            self,
            "PrivateNAcl",
            vpc=self.vpc,
            subnet_selection=ec2.SubnetSelection(subnets=self.vpc.private_subnets),
        )

        for id, subnet in enumerate(self.vpc.public_subnets, start=1):
            self.private_nacl.add_entry(
                "PrivateNACLIngress{}".format(id * 100),
                rule_number=id * 100,
                cidr=ec2.AclCidr.ipv4(subnet.node.default_child.cidr_block),
                traffic=ec2.AclTraffic.tcp_port_range(0, 65535),
                direction=ec2.TrafficDirection.INGRESS,
                rule_action=ec2.Action.ALLOW,
            )

        self.private_nacl.add_entry(
            "PrivateNACLEgressALL",
            rule_number=100,
            cidr=ec2.AclCidr.ipv4("0.0.0.0/0"),
            traffic=ec2.AclTraffic.tcp_port_range(0, 65535),
            direction=ec2.TrafficDirection.EGRESS,
            rule_action=ec2.Action.ALLOW,
        )

        self.frontSG = ec2.SecurityGroup(
            self,
            "BackendSecurityGroup",
            vpc=self.vpc,
            description="Allow web access",
            allow_all_outbound=True,
            disable_inline_rules=True,
        )
        # This will add the rule as an external cloud formation construct
        self.frontSG.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "allow HTTP access from the world"
        )
        self.frontSG.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(433), "allow HTTPS access from the world"
        )

        self.backSG = ec2.SecurityGroup(
            self,
            "FrontendSecurityGroup",
            vpc=self.vpc,
            description="Allow web access",
            allow_all_outbound=True,
            disable_inline_rules=True,
        )

        CfnOutput(self, "VPCId", value=self.vpc.vpc_id)
        CfnOutput(self, "FrontSGId", value=self.frontSG.security_group_id)
        CfnOutput(self, "BackSGId", value=self.backSG.security_group_id)
