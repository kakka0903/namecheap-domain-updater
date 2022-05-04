import requests
import argparse

from xml.dom.minidom import parseString


def get_args():
    """ Gets given progam arguments """
    # add commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-ip-url', type=str,
                        default='https://myexternalip.com/raw')
    parser.add_argument('--debug', action="store_true")
    parser.add_argument('--domain', required=True,
                        action="store", type=str)
    parser.add_argument('--password', required=True,
                        action="store", type=str)
    parser.add_argument('--hosts', required=True, nargs='+')

    # retun given args
    return parser.parse_args()


def get_current_ip(ip_check_address):
    """ Gets the current ip_address from a website """
    try:
        request = requests.get(ip_check_address)
    except ConnectionError:
        return False

    if request.ok:
        return request.text
    else:
        return False


def update_host(domain, host, ip, password):
    # format the url
    url = f'https://dynamicdns.park-your-domain.com/update?host={host}&domain={domain}&password={password}&ip={ip}'

    # make the api call
    # and catch connection error
    try:
        result = requests.get(url)
    except ConnectionError:
        return False

    # failed request
    if not result.ok:
        return False

    # check if there are errors
    xml_dom = parseString(result.text)
    error_tags = xml_dom.getElementsByTagName("errors")
    return not error_tags[0].hasChildNodes()


if __name__ == '__main__':
    args = get_args()
    ip = get_current_ip(args.check_ip_url)

    if not ip:
        print("Could not get current ip address. Aborting")
        exit()

    print(f"\nsetting {len(args.domain)} records for {args.domain} to {ip}")
    for host in args.hosts:
        if not update_host(args.domain, host, ip, args.password):
            print(f'  - update failed for: {host}')
    print("done\n")
