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
 
 dTEMPLATE_CREATE_API = {'jsonrpc': "2.0", 'method': "template.create", 
                         'params': {'host': "", 'groups': {'groupid': 1}, 
                                    'hosts': []}, 
                         'id': 1004, 'auth': None} 
  
 dITEM_KEY_VALUE = {'os_agent_info': 'agent.ping', 
                    'os_cpu_usage': 'system.cpu.util[,iowait]', 
                    'os_cpu_load': 'system.cpu.load[percpu,avg1]', 
                    'os_proc_value': 'proc.num[,,run]', 
                    'app_status': 'net.tcp.port[ ,*]', 
                    'app_memory': 'proc.mem[*,root]'} 
 





