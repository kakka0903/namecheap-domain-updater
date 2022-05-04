import requests
import argparse

from xml.dom.minidom import parseString


def get_args():
    """ Returns the parsed arguments given to the program. """
    # add commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip-url',
                        type=str,
                        default='https://myexternalip.com/raw',
                        help='URL that returns your public IP in raw text.',
                        required=False)

    parser.add_argument('--ip',
                        type=str,
                        help='Specify the IP adress to set records to',
                        required=False)

    parser.add_argument('domain',
                        action="store",
                        help='The domain name you want to update records for.',
                        type=str)

    parser.add_argument('password',
                        action="store",
                        type=str,
                        help='The "Dynamic DNS Password" for your namecheap domain.')

    parser.add_argument('hosts',
                        nargs='+',
                        help='A list of "hosts" to update for your domain.')

    # retun given args
    return parser.parse_args()


def get_url_ip(ip_url):
    """ Returns the IP given in raw text by the given URL """
    try:
        request = requests.get(ip_url)
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

    if args.ip:
        ip = args.ip
        print(f"using specified IP ({ip})")

    elif args.ip_url:
        ip = get_url_ip(args.ip_url)
        print(f"using IP ({ip}) fetched from {args.ip_url}")

    if not ip:
        print("could not get current ip address. aborting")
        exit()

    print(f"\nsetting {len(args.hosts)} records for {args.domain} to {ip}")
    for host in args.hosts:
        if not update_host(args.domain, host, ip, args.password):
            print(f'    update failed for: {host}')

    print()
    print("done!")
