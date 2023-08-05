# -*- coding: utf-8 -*-
'''
Created on 2020-12-6

@author: zhys513(254851907@qq.com)
'''
from opspipe.DevOps.deploy.DockerClient import DockerClient 
from opspipe.DevOps.deploy.SSHClient import SSHClient 


SSH = SSHClient().sshConnection('192.168.54.22','root', 'yirong123',10022)
DOCKER = DockerClient(SSH)
'''
result = DOCKER.stop('ai_special_1.0')
print(result)
result = DOCKER.start('ai_special_1.0')
print(result)
'''
result = DOCKER.logs('ai_special_1.0',10)
print(result)