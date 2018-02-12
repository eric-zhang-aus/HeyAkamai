# HeyAkamai CLI

## Description
HeyAkamai CLI is a command line that can assist the users to do some basic Akamai troubleshootings.

## Credentials
The crendial needs access to Akamai PAPI endpoint, and they are passed from the four environment variables: 
```
AKAMAI_PAPI_CLIENT_TOKEN   
AKAMAI_PAPI_CLIENT_SECRET  
AKAMAI_PAPI_ACCESS_TOKEN  
AKAMAI_PAPI_URL   
```

## Sample 
```bash
NCA1028940:HeyAkamai-CLI chenj1$ python HeyAkamai.py 

Please type the hostname: www.news.com.au

Please choose environment (0 for staging, 1 for production): 0

Searching the property for www.news.com.au ......
Property found: wp.mastheads.prod

You chose to check staging

Checking the active versions of staging ...
staging_propertyVersion : 384
staging_propertyId : prp_228847
staging_groupId : grp_106431
staging_contractId : ctr_M-24P95UF
staging_edgeHostname : wildcardsan.news.com.au.edgekey-staging.net
staging_lastUpdate : 2018-02-07T05:12:55Z by gareth.mcshane@news.com.au for csp exception for /video

Downloading the active version configuration ......
<Response [200]>

Checking origin settings...
hostname : newsatnewscorpau.wordpress.com
originType : CUSTOMER
forwardHostHeader : ORIGIN_HOSTNAME
cacheKeyHostname : REQUEST_HOST_HEADER
compress : True
enableTrueClientIp : True
trueClientIpHeader : True-Client-IP
trueClientIpClientSetting : False
httpPort : 80
verificationMode : CUSTOM
originSni : False
httpsPort : 443
originCertificate : 
ports : 
customValidCnValues : ['{{Origin Hostname}}', '{{Forward Host Header}}']
originCertsToHonor : STANDARD_CERTIFICATE_AUTHORITIES
standardCertificateAuthorities : ['akamai-permissive']

Do you want to read all rules? (y or n) n
Bye!

```# HeyAkamai
