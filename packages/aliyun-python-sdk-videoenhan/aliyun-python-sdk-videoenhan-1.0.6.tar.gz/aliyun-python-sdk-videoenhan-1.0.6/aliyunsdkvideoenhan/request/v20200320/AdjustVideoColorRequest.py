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
from aliyunsdkvideoenhan.endpoint import endpoint_data

class AdjustVideoColorRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'videoenhan', '2020-03-20', 'AdjustVideoColor','videoenhan')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_Mode(self):
		return self.get_body_params().get('Mode')

	def set_Mode(self,Mode):
		self.add_body_params('Mode', Mode)

	def get_VideoUrl(self):
		return self.get_body_params().get('VideoUrl')

	def set_VideoUrl(self,VideoUrl):
		self.add_body_params('VideoUrl', VideoUrl)

	def get_VideoBitrate(self):
		return self.get_body_params().get('VideoBitrate')

	def set_VideoBitrate(self,VideoBitrate):
		self.add_body_params('VideoBitrate', VideoBitrate)

	def get_VideoCodec(self):
		return self.get_body_params().get('VideoCodec')

	def set_VideoCodec(self,VideoCodec):
		self.add_body_params('VideoCodec', VideoCodec)

	def get_VideoFormat(self):
		return self.get_body_params().get('VideoFormat')

	def set_VideoFormat(self,VideoFormat):
		self.add_body_params('VideoFormat', VideoFormat)