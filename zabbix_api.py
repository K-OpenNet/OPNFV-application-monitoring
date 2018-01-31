 # 
 #    Licensed under the Apache License, Version 2.0 (the "License"); you may 
 #    not use this file except in compliance with the License. You may obtain 
 #    a copy of the License at 
 # 
 #         http://www.apache.org/licenses/LICENSE-2.0 
 # 
 #    Unless required by applicable law or agreed to in writing, software 
 #    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT 
 #    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the 
 #    License for the specific language governing permissions and limitations 
 #    under the License. 
 # 
 URL_ = "/zabbix/api_jsonrpc.php" 
 
 
 HEADERS = {'Content-Type': 'application/json-rpc'} 
 dAUTH_API = {'jsonrpc': "2.0", 
              'method': 'user.login', 
              'params': {'user': None, 
                         'password': None}, 
              'id': 1, 
              'auth': None} 
 COMP_VALUE = {'greater': '>', 
               'less': '<', 
               'and greater': '>=', 
               'and less': '<=', 
               'down': '=0'} 
 
 
