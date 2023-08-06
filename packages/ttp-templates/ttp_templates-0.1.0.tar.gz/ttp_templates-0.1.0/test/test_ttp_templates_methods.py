import sys
import pprint
sys.path.insert(0,'..')

from ttp_templates import get_template
from ttp_templates import parse_output


def test_get_template():
    template = get_template(path="yang/ietf-interfaces_cisco_ios.txt")
    # print(template)
    assert isinstance(template, str)

# test_get_template()

def test_parse_output_platform():
    data = """
interface GigabitEthernet1/3.251
 description Customer #32148
 encapsulation dot1q 251
 ip address 172.16.33.10 255.255.255.128
 shutdown
!
interface GigabitEthernet1/3.251
 description Customer #32148
 encapsulation dot1q 251
 ip address 172.16.33.10 255.255.255.128
 shutdown
    """
    result = parse_output(
        data=data,
        platform="Test Platform",
        command="show run | sec interface"
    )
    # pprint.pprint(result)
    assert result == [[[{'description': 'Customer #32148',
                         'disabled': True,
                         'dot1q': '251',
                         'interface': 'GigabitEthernet1/3.251',
                         'ip': '172.16.33.10',
                         'mask': '255.255.255.128'},
                        {'description': 'Customer #32148',
                         'disabled': True,
                         'dot1q': '251',
                         'interface': 'GigabitEthernet1/3.251',
                         'ip': '172.16.33.10',
                         'mask': '255.255.255.128'}]]]
    
# test_parse_output()

def test_parse_output_misc():
    data = """
r1# show run | sec interfaces
interface GigabitEthernet1
 vrf forwarding MGMT
 ip address 10.223.89.55 255.255.255.0
 negotiation auto
 no mop enabled
interface GigabitEthernet1
 vrf forwarding MGMT
 ip address 10.223.89.56 255.255.255.0
 negotiation auto
 no mop enabled
 no mop sysid
    """
    result = parse_output(
        data=data,
        misc="ttp_templates_tests/cisco_ios_interfaces_cfg_per_ip.txt"
    )
    # pprint.pprint(result)
    assert result == [[{'description': 'description',
                        'hostname': 'r1',
                        'interface': 'GigabitEthernet1',
                        'ip': '10.223.89.55',
                        'mask': '255.255.255.0',
                        'vrf': 'MGMT'},
                       {'description': 'description',
                        'hostname': 'r1',
                        'interface': 'GigabitEthernet1',
                        'ip': '10.223.89.56',
                        'mask': '255.255.255.0',
                        'vrf': 'MGMT'}]]
   
   
# test_parse_output_misc()