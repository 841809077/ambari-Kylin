from resource_management import *
from resource_management.libraries.script.script import Script
import os

# server configurations
config = Script.get_config()
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]
tmp_dir = Script.get_tmp_dir()

ambari_server_hostname = config['clusterHostInfo']['ambari_server_host'][0]
kylin_download = os.path.join('http://', ambari_server_hostname, 'kylin/kylin-2.5.1.tar.gz')

kylin_user = config['configurations']['kylin']['kylin_user']
kylin_group = config['configurations']['kylin']['kylin_group']
kylin_install_dir = config['configurations']['kylin']['kylin_install_dir']
kylin_log_dir = config['configurations']['kylin']['kylin_log_dir']
kylin_pid_dir = config['configurations']['kylin']['kylin_pid_dir']
kylin_pid_file = format("{kylin_pid_dir}/kylin.pid")

kylin_web_port = config['configurations']['kylin']['kylin_web_port']

kylin_properties = config['configurations']['kylin']['kylin_properties']

# kylin web timezone
kylin_web_timezone = config['configurations']['kylin']['kylin_web_timezone']
# kylin_web_cross_domain_enabled
kylin_web_cross_domain_enabled = config['configurations']['kylin']['kylin_web_cross_domain_enabled']
if (kylin_web_cross_domain_enabled):
    kylin_web_cross_domain_enabled = 'true'
else:
    kylin_web_cross_domain_enabled = 'false'

current_host_name = config['hostname']
server_mode = "query"
server_masters = config['clusterHostInfo']['kylin_all_hosts'][0]
server_clusters_arr = config['clusterHostInfo']['kylin_all_hosts'] + (
    config['clusterHostInfo'].has_key('kylin_query_hosts') and config['clusterHostInfo']['kylin_query_hosts'] or [])

server_clusters = ','.join(i + ":" + kylin_web_port for i in server_clusters_arr)
kylin_servers = ';'.join("server " + i + ":" + kylin_web_port for i in server_clusters_arr) + ";"
hadoop_conf_dir = kylin_install_dir + "/conf/hadoop_conf"

# ngnix
nginx_download = os.path.join('http://', ambari_server_hostname, 'kylin/nginx-1.8.1.tar.gz')
nginx_install_dir = config['configurations']['nginx']['nginx_install_dir']
nginx_conf = config['configurations']['nginx']['nginx_conf']
nginx_port = config['configurations']['nginx']['nginx_port']
nginx_log_dir = config['configurations']['nginx']['nginx_log_dir']
nginx_pid_dir = config['configurations']['nginx']['nginx_pid_dir']
nginx_pid_file = format("{nginx_pid_dir}/nginx.pid")
