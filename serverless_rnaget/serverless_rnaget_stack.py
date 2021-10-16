from aws_cdk import core as cdk

from serverless_rnaget.gateway.api import API


class RnagetStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.api = API(scope, 'RNAgetAPI')
