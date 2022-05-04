# namecheap-domain-updater
Update the IP records for your namecheap domain. Use either a specified IP address, or let the script automatically fetch your public IP. 

Run periodically with crontab to keep your DNS records up to date. Useful if you have a server running behind a dynamic IP address. 

## Useage
```
$ python3.9 update-domain.py --help

usage: update-domain.py [-h] [--ip-url IP_URL] [--ip IP] domain password hosts [hosts ...]

positional arguments:
  domain           The domain name you want to update records for.
  password         The "Dynamic DNS Password" for your namecheap domain.
  hosts            A list of "hosts" to update for your domain.

optional arguments:
  -h, --help       show this help message and exit
  --ip-url IP_URL  URL that returns your public IP in raw text.
  --ip IP          Specify the IP adress to set records to
 
```