import xml.etree.ElementTree as ET
import re
import yaml
import base64
import os

MAPPING = {
    "xrv": "cisco_xrv",
    "xrv9k": "cisco_xrv9k",
    "csr1000v": "cisco_csr1000v",
    "csr1000vng": "cisco_csr1000v",
    "cat8000v": "cisco_c8000v",
    "vios": "linux",
}

REGISTRY = "ghcr.io/kaelemc"
CFG_DIR = "./configs"

# file_path = "./Ping Factory - CCNP CCIE SP mock lab.unl"
file_path = "CCIE SP bootcamp ch02.unl"

tree = ET.parse(file_path)
root = tree.getroot()

name = "".join([ c if c.isalnum() else "-" for c in root.get("name") ]).lower()

clab_topo = {
    'name': name,
    'topology': {},
}

raw_nodes = {}
links = {}
kinds = {}

for node in root.find("topology").find("nodes").findall("node"):
    
    node_id = node.get("id")
    node_name = node.get("name")
    node_kind = MAPPING[node.get("template")]
    
    node_image_raw = node.get("image")
    node_image_version = re.search("(?<=-).*$", node_image_raw).group()
    node_image = f"{REGISTRY}/{node_kind}:{node_image_version}"
    
    if node_kind not in kinds:
        kinds[node_kind] = {'image': node_image}
    
    raw_nodes[node_id] = {'name': node_name, 'kind': node_kind}

    for interface in node.findall('interface'):
        intf_id = interface.get("id")
        intf_name = interface.get("name")
        intf_net = interface.get("network_id")
        intf_obj = {'node': node_name, 'interface': intf_name, 'intf_idx': intf_id}

        if intf_net not in links:
            links[intf_net] = {}
            
        links[intf_net][node_name] = intf_obj

for config in root.find("objects").find("configs").findall("config"):
    cfg_id = config.get("id")
    raw_nodes[cfg_id]['config'] = config.text

link_list = []
nodes = {}

try:
    os.makedirs(f"./configs")
except:
    pass

for x in raw_nodes:
    node_name = raw_nodes[x]['name']
    node_kind = raw_nodes[x]['kind']
    
    if 'config' in raw_nodes[x]:
        cfg_path = f"{CFG_DIR}/{node_name}.cfg"
        
        print(f"\x1B[0;32mFound\x1B[0m configuration for {node_name}\tAttempting to write to {cfg_path}", end='')
        
        try:
            with open(cfg_path, "w") as cfg:
                cfg.write(base64.b64decode(raw_nodes[x]['config']).decode())
            print(f" \t\x1B[0;32mSUCCESS\x1B[0m")
        except:
            print(f" \t\x1B[0;31mFAIL\x1B[0m")
        nodes[node_name] = {'kind': node_kind, 'startup-config': cfg_path}
    else:
        nodes[node_name] = {'kind': node_kind}

for x in links:
    keys = list(links[x].keys())
    intf0 = f"{keys[0]}:{links[x][keys[0]]['interface']}"
    intf1 = f"{keys[1]}:{links[x][keys[1]]['interface']}"
    
    link_list.append({'endpoints': [intf0, intf1]})

clab_topo['topology']['kinds'] = kinds
clab_topo['topology']['nodes'] = nodes
clab_topo['topology']['links'] = link_list


print("Exporting to 'topo.clab.yml'")

with open('topo.clab.yml', 'w') as yaml_file:
    yaml.dump(clab_topo, yaml_file, default_flow_style=False, sort_keys=False)

print(f"Done {name}")
