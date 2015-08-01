# do-dydns
DigitalOcean DyDns (Dynamic DNS)

I created this as a quick and dirty means to tracking the ip addresses of relatives whom I provide computer support to. Signing up for Dynamic DNS providers isn't as simple/free as it used to be, so I figured if I already had a domain hosted on my DigitalOcean account, why not roll my own DyDns using the API. I stick this as a cron job on people's boxes, and now I have `mom.example.com` and `bro1.example.com`.

## Running

The domain you choose must have it's nameservers already pointed at DigitalOcean, and the basic domain setup must be done as well. You don't have to create the record itself, that will be taken care of with this script.

The python script takes three command line arguments:

```
$ python do-dydns.py --help
usage: do-dydns.py [-h] -a API_KEY -d DOMAIN_NAME -r RECORD_NAME

DigitalOcean Dynamic DNS

optional arguments:
  -h, --help            show this help message and exit
  -a API_KEY, --api_key API_KEY
                        DigitalOcean v2 api key
  -d DOMAIN_NAME, --domain-name DOMAIN_NAME
                        Domain name managed by DigitalOcean (eg: example.com)
  -r RECORD_NAME, --record-name RECORD_NAME
                        Short form DNS name, either subdomain or @ for the
                        domain itself (eg: @ or home)
```

## Example

If you own `example.com`, and want `example.com` to point at your ip address:

```
python do-dydns.py -a 'DIGITAL_OCEAN_API_V2_KEY_HERE' -d 'example.com' -r '@'
```

If you would prefer to use the subdomain `home.example.com`:

```
python do-dydns.py -a 'DIGITAL_OCEAN_API_V2_KEY_HERE' -d 'example.com' -r 'home'
```
