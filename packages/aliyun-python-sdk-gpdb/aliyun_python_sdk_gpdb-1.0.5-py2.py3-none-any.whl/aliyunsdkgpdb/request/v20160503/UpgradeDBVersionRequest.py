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
from aliyunsdkgpdb.endpoint import endpoint_data

class UpgradeDBVersionRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'gpdb', '2016-05-03', 'UpgradeDBVersion','gpdb')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_SwitchTimeMode(self):
		return self.get_query_params().get('SwitchTimeMode')

	def set_SwitchTimeMode(self,SwitchTimeMode):
		self.add_query_param('SwitchTimeMode',SwitchTimeMode)

	def get_DBInstanceId(self):
		return self.get_query_params().get('DBInstanceId')

	def set_DBInstanceId(self,DBInstanceId):
		self.add_query_param('DBInstanceId',DBInstanceId)

	def get_SwitchTime(self):
		return self.get_query_params().get('SwitchTime')

	def set_SwitchTime(self,SwitchTime):
		self.add_query_param('SwitchTime',SwitchTime)

	def get_MajorVersion(self):
		return self.get_query_params().get('MajorVersion')

	def set_MajorVersion(self,MajorVersion):
		self.add_query_param('MajorVersion',MajorVersion)

	def get_MinorVersion(self):
		return self.get_query_params().get('MinorVersion')

	def set_MinorVersion(self,MinorVersion):
		self.add_query_param('MinorVersion',MinorVersion)

	def get_OwnerId(self):
		return self.get_query_params().get('OwnerId')

	def set_OwnerId(self,OwnerId):
		self.add_query_param('OwnerId',OwnerId)