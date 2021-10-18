from aws_cdk import core as cdk
from aws_cdk import aws_ec2
from aws_cdk import aws_elasticsearch

from serverless_rnaget.config import config

config = config['existing_resources']


class InternalNetwork(cdk.Construct):

    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.vpc = aws_ec2.Vpc.from_lookup(self, 'VPC', vpc_id=config['vpc_id'])
        self.security_group = aws_ec2.SecurityGroup.from_security_group_id(
            self,
            'SG',
            config['security_group_id'],
            mutable=False
        )


class ExistingResources(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.internal_network = InternalNetwork(self, 'VPCSecurity')
        self.elasticsearch = aws_elasticsearch.Domain.from_domain_endpoint(
            self,
            'RNAGetExpressions',
            config['elasticsearch'],
        )
