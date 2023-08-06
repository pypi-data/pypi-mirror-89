# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkehpc.endpoint import endpoint_data

class EditJobTemplateRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'EHPC', '2018-04-12', 'EditJobTemplate')
		self.set_method('GET')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_StderrRedirectPath(self):
		return self.get_query_params().get('StderrRedirectPath')

	def set_StderrRedirectPath(self,StderrRedirectPath):
		self.add_query_param('StderrRedirectPath',StderrRedirectPath)

	def get_CommandLine(self):
		return self.get_query_params().get('CommandLine')

	def set_CommandLine(self,CommandLine):
		self.add_query_param('CommandLine',CommandLine)

	def get_ArrayRequest(self):
		return self.get_query_params().get('ArrayRequest')

	def set_ArrayRequest(self,ArrayRequest):
		self.add_query_param('ArrayRequest',ArrayRequest)

	def get_PackagePath(self):
		return self.get_query_params().get('PackagePath')

	def set_PackagePath(self,PackagePath):
		self.add_query_param('PackagePath',PackagePath)

	def get_StdoutRedirectPath(self):
		return self.get_query_params().get('StdoutRedirectPath')

	def set_StdoutRedirectPath(self,StdoutRedirectPath):
		self.add_query_param('StdoutRedirectPath',StdoutRedirectPath)

	def get_Variables(self):
		return self.get_query_params().get('Variables')

	def set_Variables(self,Variables):
		self.add_query_param('Variables',Variables)

	def get_RunasUser(self):
		return self.get_query_params().get('RunasUser')

	def set_RunasUser(self,RunasUser):
		self.add_query_param('RunasUser',RunasUser)

	def get_ReRunable(self):
		return self.get_query_params().get('ReRunable')

	def set_ReRunable(self,ReRunable):
		self.add_query_param('ReRunable',ReRunable)

	def get_TemplateId(self):
		return self.get_query_params().get('TemplateId')

	def set_TemplateId(self,TemplateId):
		self.add_query_param('TemplateId',TemplateId)

	def get_Priority(self):
		return self.get_query_params().get('Priority')

	def set_Priority(self,Priority):
		self.add_query_param('Priority',Priority)

	def get_Name(self):
		return self.get_query_params().get('Name')

	def set_Name(self,Name):
		self.add_query_param('Name',Name)