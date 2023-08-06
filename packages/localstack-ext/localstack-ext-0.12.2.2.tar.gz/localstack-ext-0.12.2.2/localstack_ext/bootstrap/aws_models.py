from localstack.utils.aws import aws_models
HJpaY=super
HJpaL=None
HJpaq=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  HJpaY(LambdaLayer,self).__init__(arn)
  self.cwd=HJpaL
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.HJpaq.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,HJpaq,env=HJpaL):
  HJpaY(RDSDatabase,self).__init__(HJpaq,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,HJpaq,env=HJpaL):
  HJpaY(RDSCluster,self).__init__(HJpaq,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,HJpaq,env=HJpaL):
  HJpaY(AppSyncAPI,self).__init__(HJpaq,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,HJpaq,env=HJpaL):
  HJpaY(AmplifyApp,self).__init__(HJpaq,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,HJpaq,env=HJpaL):
  HJpaY(ElastiCacheCluster,self).__init__(HJpaq,env=env)
class TransferServer(BaseComponent):
 def __init__(self,HJpaq,env=HJpaL):
  HJpaY(TransferServer,self).__init__(HJpaq,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,HJpaq,env=HJpaL):
  HJpaY(CloudFrontDistribution,self).__init__(HJpaq,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,HJpaq,env=HJpaL):
  HJpaY(CodeCommitRepository,self).__init__(HJpaq,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
