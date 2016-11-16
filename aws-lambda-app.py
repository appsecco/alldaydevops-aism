# Author : Madhu Akula (madhu@appsecco.com)
# Date : 7th Nov 2016
from chalice import Chalice
import boto.vpc

app = Chalice(app_name='infrmonitor')
# app.debug = True

allowed_ip = 'xxx.xxx.xxx.xxx'
aws_access_key_id = 'xxxxxxx'
aws_secret_access_key = 'xxxxxxxxxxxxx'

@app.route('/')
def index():
	return {'error': 'Not Authorised'}

# Random Token generation using "openssl rand -hex 24"
# Reference https://twitter.com/lincmdfu/status/755369085626556416

@app.route('/9ec5be0ba3773d4f6556e4/ip/inframonitor/{ipadd}')
def ip_address(ipadd):
	network_acl_id = 'acl-xxxxxx' # Subsititue your AWS VPC Network ACL ID
	acl_action = 'deny'
	protocol_num = 6 # TCP protocol (http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml)
	acl_rule_num = 99 # Any rule above 1 and below 100 is acceptable 
	port_num = 22 # Default SSH port

	if app.current_request.context["source-ip"] == allowed_ip: # To ensure only whitelisted IP can make API call
		vpc2conn = boto.vpc.VPCConnection(aws_access_key_id, aws_secret_access_key, is_secure=True, host=None, port=None, proxy=None, proxy_port=None, proxy_user=None, proxy_pass=None, debug=0, https_connection_factory=None, region=None, path='/', api_version=None, security_token=None, validate_certs=True, profile_name=None)
		network_acl_entry = vpc2conn.create_network_acl_entry(network_acl_id, acl_rule_num, protocol_num, acl_action, ipadd + '/32', egress=False, icmp_code=-1, icmp_type=-1, port_range_from=port_num, port_range_to=port_num)
		return {'ip address': ipadd }
	else:
		return {'error': 'Not Authorised'}


# Generated endpoint from chalice "https://xxxxxx.amazonaws.com/dev/"

# Security Implementations
# 1. Using the sufficient random generated token for the request when posting the IP address
# 2. Whitelist the IP address of the source making request