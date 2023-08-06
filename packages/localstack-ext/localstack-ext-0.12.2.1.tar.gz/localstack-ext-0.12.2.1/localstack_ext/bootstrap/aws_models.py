from localstack.utils.aws import aws_models
RLizl=super
RLizH=None
RLizC=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  RLizl(LambdaLayer,self).__init__(arn)
  self.cwd=RLizH
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.RLizC.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,RLizC,env=RLizH):
  RLizl(RDSDatabase,self).__init__(RLizC,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,RLizC,env=RLizH):
  RLizl(RDSCluster,self).__init__(RLizC,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,RLizC,env=RLizH):
  RLizl(AppSyncAPI,self).__init__(RLizC,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,RLizC,env=RLizH):
  RLizl(AmplifyApp,self).__init__(RLizC,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,RLizC,env=RLizH):
  RLizl(ElastiCacheCluster,self).__init__(RLizC,env=env)
class TransferServer(BaseComponent):
 def __init__(self,RLizC,env=RLizH):
  RLizl(TransferServer,self).__init__(RLizC,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,RLizC,env=RLizH):
  RLizl(CloudFrontDistribution,self).__init__(RLizC,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,RLizC,env=RLizH):
  RLizl(CodeCommitRepository,self).__init__(RLizC,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
