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

