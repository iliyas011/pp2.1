import json

with open("sample-data.json") as f:
    data = json.load(f)


interfaces =  data["imdata"]
print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<10} {'MTU'}")
print("-" * 80)


for item in interfaces:
    
    dn = item["l1PhysIf"]["attributes"]["dn"]
    description = item["l1PhysIf"]["attributes"]["descr"] 
    speed = item["l1PhysIf"]["attributes"]["speed"]
    mtu = item["l1PhysIf"]["attributes"]["mtu"]

    print(f"{dn:<50}                  {description}   {speed}    {mtu}  ")
