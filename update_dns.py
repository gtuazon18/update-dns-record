import CloudFlare

api_token = input("Enter your Cloudflare API token: ")
domain_name = input("Enter the domain name for which you want to update the DNS record: ")
new_ip = input("Enter the new IP address to set for the DNS record: ")

cf = CloudFlare.CloudFlare(token=api_token)

try:
    zones = cf.zones.get(params={"name": domain_name})
    if len(zones) == 0:
        raise Exception(f"No zone found for {domain_name}")
    zone_id = zones[0]["id"]
except CloudFlare.exceptions.CloudFlareAPIError as e:
    print(f"CloudFlare API error: {e}")
    exit()
except Exception as e:
    print(f"Error: {e}")
    exit()

try:
    records = cf.zones.dns_records.get(zone_id, params={"name": domain_name, "type": "A"})
    if len(records) == 0:
        raise Exception(f"No A record found for {domain_name}")
    record_id = records[0]["id"]
except CloudFlare.exceptions.CloudFlareAPIError as e:
    print(f"CloudFlare API error: {e}")
    exit()
except Exception as e:
    print(f"Error: {e}")
    exit()

try:
    data = {"type": "A", "name": domain_name, "content": new_ip}
    cf.zones.dns_records.put(zone_id, record_id, data=data)
    print(f"Successfully updated the IP address of {domain_name} to {new_ip}")
except CloudFlare.exceptions.CloudFlareAPIError as e:
    print(f"CloudFlare API error: {e}")
    exit()
