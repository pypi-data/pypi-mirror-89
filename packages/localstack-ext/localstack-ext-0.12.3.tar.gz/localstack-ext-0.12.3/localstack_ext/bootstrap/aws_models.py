from localstack.utils.aws import aws_models
qEUdg=super
qEUdf=None
qEUdP=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  qEUdg(LambdaLayer,self).__init__(arn)
  self.cwd=qEUdf
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.qEUdP.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,qEUdP,env=qEUdf):
  qEUdg(RDSDatabase,self).__init__(qEUdP,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,qEUdP,env=qEUdf):
  qEUdg(RDSCluster,self).__init__(qEUdP,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,qEUdP,env=qEUdf):
  qEUdg(AppSyncAPI,self).__init__(qEUdP,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,qEUdP,env=qEUdf):
  qEUdg(AmplifyApp,self).__init__(qEUdP,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,qEUdP,env=qEUdf):
  qEUdg(ElastiCacheCluster,self).__init__(qEUdP,env=env)
class TransferServer(BaseComponent):
 def __init__(self,qEUdP,env=qEUdf):
  qEUdg(TransferServer,self).__init__(qEUdP,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,qEUdP,env=qEUdf):
  qEUdg(CloudFrontDistribution,self).__init__(qEUdP,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,qEUdP,env=qEUdf):
  qEUdg(CodeCommitRepository,self).__init__(qEUdP,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
