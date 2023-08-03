# css
This repository contains a collection of diverse scripts dedicated to cybersecurity solutions and tools, designed to enhance network protection and identify vulnerabilities.

# vol2help
In order to use the Dump proc / VirusTotal function, you need an API key. The instructions for this can be found here: https://support.virustotal.com/hc/en-us/articles/115002088769-Please-give-me-an-API-key. Subsequently, the variable API_KEY="Your_API_KEY" can be adjusted.

### Instructions
The script must be executable and ideally located in the same directory as the RAM image. To call the script, use ./vol2help.sh

# nmaphelp

### Running Nmap without root privileges

Nmap can be run without root privileges while still supporting all advanced features and port scanning methods. 
We just need to utilize Linux process capabilities and assign three specific capabilities to the Nmap binary.

* CAP_NET_RAW
* CAP_NET_ADMIN
* CAP_NET_BIND_SERVICE

`sudo setcap cap_net_raw,cap_net_admin,cap_net_bind_service+eip /usr/bin/nmap`

Remember to use the --privileged flag with Nmap. This tells Nmap it has all the required capabilities, even when not run as root.