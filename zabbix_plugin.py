 # All Rights Reserved. 
 # 
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
 
 
 import json 
 import requests 
 import time 
 
 
 import copy 
 from oslo_log import log as logging 
 from tacker.vnfm.monitor_drivers import abstract_driver 
 from tacker.vnfm.monitor_drivers.zabbix import zabbix_api as zapi 
 
 
 

 LOG = logging.getLogger(__name__) 


 
 class VNFMonitorZabbix(abstract_driver.VNFMonitorAbstractDriver): 
     params = ['application', 'OS'] 
 
 
     def __init__(self): 
         self.kwargs = None 
         self.vnf = None 
         self.vduname = [] 
         self.URL = None 
         self.hostinfo = {} 
         self.tenant_id = None 
     def get_type(self): 
         """Return one of predefined type of the hosting vnf drivers.""" 
         plugin_type = 'zabbix' 
         return plugin_type 
 
      def get_name(self): 
         """Return a symbolic name for the VNF Monitor plugin.""" 
         plugin_name = 'zabbix' 
         return plugin_name 

     def get_description(self): 
         """Return description of VNF Monitor plugin.""" 
         plugin_descript = 'Tacker VNFMonitor Zabbix Driver' 
         return plugin_descript 
     def monitor_get_config(self, plugin, context, vnf): 
 
 
         """Return dict of monitor configuration data. 
  
         :param plugin: 
         :param context: 
         :param vnf: 
         :returns: dict 
         :returns: dict of monitor configuration data 
         """ 
         return {} 

     def monitor_url(self, plugin, context, vnf): 
         """Return the url of vnf to monitor. 
  
         :param plugin: 
         :param context: 
         :param vnf: 
         :returns: string 
         :returns: url of vnf to monitor 
         """ 
         pass 
     def send_post(self, query): 
         response = requests.post(self.URL, headers=zapi.HEADERS, 
                                  data=json.dumps(query)) 
         return dict(response.json()) 
  
     @staticmethod 
     def check_error(response): 
         try: 
             if 'result' not in response: 
                 raise ValueError 
         except ValueError: 
             LOG.error('Cannot request error : %s', response['error']['data']) 

     def create_graph(self, itemid, name, nodename): 
             temp_graph_api = copy.deepcopy(zapi.dGRAPH_CREATE_API) 
             gitems = [{'itemid': itemid, 'color': '00AA00'}] 
             temp_graph_api['auth'] = \ 
                 self.hostinfo[nodename]['zbx_info']['zabbix_token'] 
             temp_graph_api['params']['gitems'] = gitems 
             temp_graph_api['params']['name'] = name 
             response = self.send_post(temp_graph_api) 
             VNFMonitorZabbix.check_error(response) 
     def create_action(self): 
         for vdu in self.vduname: 
             temp_action_api = copy.deepcopy(zapi.dACTION_CREATE_API) 
             temp_action_api['auth'] = \ 
                 self.hostinfo[vdu]['zbx_info']['zabbix_token'] 
             tempname_api = temp_action_api['params']['operations'][0] 
             temp_filter = temp_action_api['params']['filter'] 
             for info in (self.hostinfo[vdu]['actioninfo']): 
                 tempname_api['opcommand_hst'][0]['hostid'] = \ 
                     self.hostinfo[vdu]['hostid'] 
                 now = time.localtime() 
                 rtime = str(now.tm_hour) + str(now.tm_min) + str(now.tm_sec) 
                 temp_name = "Trigger Action " + \ 
                             str( 
                                 vdu + rtime + " " + 
                                 info['item'] + " " + info['action'] 
                             ) 
                 temp_action_api['params']['name'] = temp_name 
                 if (info['action'] == 'cmd') and \ 
                         (info['item'] != 'os_agent_info'): 
 
 
                     tempname_api['opcommand']['command'] = info['cmd-action'] 
  
                 elif (info['item'] == 'os_agent_info') \ 
                         and (info['action'] == 'cmd'): 
 
 
                     tempname_api['opcommand']['authtype'] = 0 
                     tempname_api['opcommand']['username'] = \ 
                         self.hostinfo[vdu]['appinfo']['ssh_username'] 
                     tempname_api['opcommand']['password'] = \ 
                         self.hostinfo[vdu]['appinfo']['ssh_password'] 
                     tempname_api['opcommand']['type'] = 2 
                     tempname_api['opcommand']['command'] = info['cmd-action'] 
                     tempname_api['opcommand']['port'] = 22 
                     temp_filter['conditions'][0]['value'] = info['trigger_id'] 
                     response = self.send_post(temp_action_api) 
                     VNFMonitorZabbix.check_error(response) 
                     continue 

                 temp_filter['conditions'][0]['value'] = info['trigger_id'] 
                 response = self.send_post(temp_action_api) 
                 VNFMonitorZabbix.check_error(response) 
  
     def create_vdu_host(self): 
         for vdu in self.vduname: 
             temp_host_api = zapi.dHOST_CREATE_API 
             temp_group_api = zapi.dGROUP_GET_API 
             temp_host_api['auth'] = \ 
                 self.hostinfo[vdu]['zbx_info']['zabbix_token'] 
             temp_group_api['auth'] = \ 
                 self.hostinfo[vdu]['zbx_info']['zabbix_token'] 
             response = self.send_post(temp_group_api) 
             gid = response['result'][0]['groupid'] 
             temp_host_api['params']['host'] = str(vdu) 
             if type(self.hostinfo[vdu]['mgmt_ip']) is list: 
                 for vduip in (self.hostinfo[vdu]['mgmt_ip']): 
                     temp_host_api['params']['interfaces'][0]['ip'] = vduip 
                     temp_host_api['params']['templates'][0]['templateid'] = \ 
                         self.hostinfo[vdu]['template_id'][0] 
                     temp_host_api['params']['groups'][0]['groupid'] = gid 
                     response = self.send_post(temp_host_api) 
             else: 
                 temp_host_api['params']['interfaces'][0]['ip'] = \ 
                     self.hostinfo[vdu]['mgmt_ip'] 
                 temp_host_api['params']['templates'][0]['templateid'] = \ 
                     self.hostinfo[vdu]['template_id'][0] 
                 temp_host_api['params']['groups'][0]['groupid'] = gid 
                 response = self.send_post(temp_host_api) 
             if 'error' in response: 
                 now = time.localtime() 
                 rtime = str(now.tm_hour) + str(now.tm_min) + str(now.tm_sec) 
                 temp_host_api['params']['host'] = str(vdu) + rtime 
                 response = self.send_post(temp_host_api) 
             self.hostinfo[vdu]['hostid'] = response['result']['hostids'][0] 

     def create_trigger(self, trigger_params, vduname): 
         temp_trigger_api = copy.deepcopy(zapi.dTRIGGER_CREATE_API) 
         temp_trigger_api['auth'] = \ 
            self.hostinfo[vduname]['zbx_info']['zabbix_token'] 
         temp_trigger_api['params'] = trigger_params 
         temp_trigger_api['templateid'] = \ 
             str( 
                 self.hostinfo[vduname]['template_id'][0]) 
         response = self.send_post(temp_trigger_api) 
         VNFMonitorZabbix.check_error(response) 
         return response['result'] 
     def _create_trigger(self): 
 
         trigger_params = [] 
         trig_act_pa = [] 


         for vdu in self.vduname: 
             temp_trigger_list = copy.deepcopy(zapi.dTRIGGER_LIST) 

             temp_vdu_name = self.hostinfo[vdu]['appinfo']['app_name'] 
             temp_vdu_port = self.hostinfo[vdu]['appinfo']['app_port'] 
             for para in VNFMonitorZabbix.params: 
                 for item in self.hostinfo[vdu]['parameters'][para].keys(): 
                     action_list = copy.deepcopy(zapi.dACTION_LIST) 
                     temp_item = self.hostinfo[vdu]['parameters'][para][item] 

                     if ('app_name' != item)\ 
                             and ('app_port' != item) \ 
                             and ('ssh_username' != item) \ 
                             and ('ssh_password' != item): 
                         if 'condition' \ 
                                 in temp_item.keys(): 
                             temp_con = temp_item['condition'] 
  
                         if len(temp_con) == 2: 
                             temp_comparrision = temp_con[0] 
                             temp_comparrision_value = temp_con[1] 
                             temp_trigger_list[item][0]['expression'] += \ 
                                 self.hostinfo[vdu]['template_name'] + ':'\ 
                                 + str( 
                                     zapi.dITEM_KEY_COMP[item].replace( 
                                         '*', str(temp_vdu_name))) \ 
                                 + str( 
                                     zapi.COMP_VALUE[temp_comparrision]) \ 
                                 + str( 
                                     temp_comparrision_value) 
                         else: 
                             temp_comparrision = temp_con[0] 
                             if 'os_agent_info' == item: 
                                 temp_trigger_list[item][0]['expression'] += \ 
                                     self.hostinfo[vdu]['template_name'] + ':' \ 
                                     + str(zapi.dITEM_KEY_COMP[item]) 

                             else: 
                                 temp_trigger_list[item][0]['expression'] += \ 
                                     self.hostinfo[vdu]['template_name'] + ':' \ 
                                     + str( 
                                         zapi.dITEM_KEY_COMP[item].replace( 
                                             '*', str(temp_vdu_port))) \ 
                                     + str( 
                                         zapi.COMP_VALUE[temp_comparrision]) 
                         if 'actionname' in \ 
                                 temp_item.keys(): 
                             trig_act_pa.append(temp_trigger_list[item][0]) 
                             response = self.create_trigger(trig_act_pa, vdu) 
                             del trig_act_pa[:] 
                             action_list['action'] = \ 
                                 temp_item['actionname'] 
                             action_list['trigger_id'] = \ 
                                 response['triggerids'][0] 
                             action_list['item'] = item 
                             if 'cmd' == \ 
                                     temp_item['actionname']: 
  

