from localstack.utils.aws import aws_models
EMiyb=super
EMiyv=None
EMiyH=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  EMiyb(LambdaLayer,self).__init__(arn)
  self.cwd=EMiyv
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.EMiyH.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,EMiyH,env=EMiyv):
  EMiyb(RDSDatabase,self).__init__(EMiyH,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,EMiyH,env=EMiyv):
  EMiyb(RDSCluster,self).__init__(EMiyH,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,EMiyH,env=EMiyv):
  EMiyb(AppSyncAPI,self).__init__(EMiyH,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,EMiyH,env=EMiyv):
  EMiyb(AmplifyApp,self).__init__(EMiyH,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,EMiyH,env=EMiyv):
  EMiyb(ElastiCacheCluster,self).__init__(EMiyH,env=env)
class TransferServer(BaseComponent):
 def __init__(self,EMiyH,env=EMiyv):
  EMiyb(TransferServer,self).__init__(EMiyH,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,EMiyH,env=EMiyv):
  EMiyb(CloudFrontDistribution,self).__init__(EMiyH,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,EMiyH,env=EMiyv):
  EMiyb(CodeCommitRepository,self).__init__(EMiyH,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
