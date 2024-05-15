import paramiko
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

load_dotenv()
ssh_username = os.getenv('SSH_USERNAME')
ssh_password = os.getenv('SSH_PASSWORD')

def attempt_ssh_connection(ip, username, password):
    """Attempt SSH connection to the given IP and return True if successful."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, username=username, password=password, timeout=1)
        client.close()
        return ip, True
    except Exception as e:
        return ip, False

def update_config_file(new_ip):
    """Update the SSH config file with the new IP address."""
    config_path = os.path.expanduser('~/.ssh/config')  # Update this path if your config is located elsewhere
    with open(config_path, 'r') as file:
        lines = file.readlines()
    
    # Update this block based on the formatting of your SSH config file
    for i, line in enumerate(lines):
        if line.strip().startswith('Host PhD'):
            lines[i+1] = f'    HostName {new_ip}\n'
            break
    
    with open(config_path, 'w') as file:
        file.writelines(lines)
    print(f"Config file updated with new IP: {new_ip}")

def main():
    # Record time at start of scan
    start_time = time.time()

    username = ssh_username
    password = ssh_password
    max_workers = 128   # Number of concurrent threads, reduce if you experience network issues (e.g. reading SSH protocol banner)

    octet1_range = range(10,11) # "10." seems to be the default for AIML, but change if needed
    octet2_range = range(12,14)
    octet3_range = range(256)
    octet4_range = range(256)

    ips_to_check = [f"{h}.{i}.{j}.{k}" for h in octet1_range for i in octet2_range for j in octet3_range for k in octet4_range]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ip = {executor.submit(attempt_ssh_connection, ip, username, password): ip for ip in ips_to_check}
        for future in as_completed(future_to_ip):
            ip, success = future.result()
            if success:
                print(f"Success! Connected to {ip}")
                update_config_file(ip)
                return
            else:
                print(f"Failed to connect to {ip}")

    # Record time at end of scan
    end_time = time.time()
    print("Finished scanning! Time elapsed: " + str(end_time - start_time) + " seconds.")

if __name__ == "__main__":
    main()
