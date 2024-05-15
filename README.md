# IP Scanner
Enables a simple search of IPs with the intent of rediscovering a dynamic IP within a known range. This script will search a range of IP addresses, attempting to connect, and then update the local SSH config upon success.

## Application

1. Rename "example.env" to ".env" and replace the "abc123" with the host username and password, respectively.
2. Update the path to your SSH config file, if needed. Current setup should detect the standard setup config file for a Windows computer.
3. Update the block describing the config file formatting. For context, the example formatting matches the following:
```
  Host Host_Server_Name
    HostName xxx.xxx.xxx.xxx
    User host_username
    ServerAliveInterval 60
```
4. If receiving SSH protocol errors, reduce worker number.
