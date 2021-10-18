from aws_cdk import core as cdk
from aws_cdk import aws_ec2
from aws_cdk import aws_elasticsearch


VPC_ID = 'vpc-ea3b6581'

SECURITY_GROUP_ID = 'sg-022ea667'

ELASTICSEARCH = 'https://vpc-rna-expression-dro56qntagtgmls6suff2m7nza.us-west-2.es.amazonaws.com'


class InternalNetwork(cdk.Construct):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.vpc = aws_ec2.Vpc.from_lookup(self, 'VPC', vpc_id=VPC_ID)
        self.security_group = aws_ec2.SecurityGroup.from_security_group_id(
            self,
            'SG',
            SECURITY_GROUP_ID,
            mutable=False
        )


class ExistingResources(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.internal_network = InternalNetwork(self, 'VPCSecurity')
        self.elasticsearch = aws_elasticsearch.Domain.from_domain_endpoint(
            self,
            'RNAGetExpressions',
            ELASTICSEARCH
        )
