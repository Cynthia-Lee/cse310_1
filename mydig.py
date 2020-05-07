import dns.query
import dns.message
import sys
import datetime

# DNS resolver
# resolver takes in input domain name
# resolves query by first contacting the root server, the top-level domain,
# all the way until the authoritative name server

# using dnspython library that can resolve a single iterative DNS query

# Access the IP address of the root servers from https://www.iana.org/domains/root/servers

# Build a "dig" -like tool called "mydig"
# takes as input the name of the domain you want to resolve
# should resolve the "A" record for the query
# -------------------------------

def resolver(domain, ip): # recursion
    query = dns.message.make_query(domain, dns.rdatatype.A) # query
    response = dns.query.udp(query, ip, 2) # send query over UDP
    # check that there is no answer
    # check that there are no additionals

    if (len(response.answer) != 0): # answer was found
        arr = (str(response.answer[0])).split(" ")
        check = arr[3]
        if (check == "CNAME"): # resolve the CNAME
            domain = (arr[4])
            # need to find domain name's ip
            return resolver(domain, '198.41.0.4')
        else:
            return response.answer[0]

    if (len(response.additional) == 0):
        # check response.authority, recursive call
        # authority is a list of RRsets
        authDomain = str(response.authority[0][0]) # domain name
        # need to find domain name's ip
        authIp = resolver(authDomain, '198.41.0.4')
        authIp = (str(authIp)).split(" ")[4]
        return resolver(domain, authIp)
    else:
        # check one response.additional, only the A records
        ip = ((response.find_rrset(response.additional, response.additional[0].name, 1, dns.rdatatype.A)).items[0])
        ip = str(ip)
        return resolver(domain, ip)

class mydig:
    # take in input
    domain = sys.argv[1]
    # make query
    query = dns.message.make_query(domain, dns.rdatatype.A)
    print("QUESTION SECTION:")
    print(query.question[0])
    print("\nANSWER SECTION:")
    # start time
    start_time = datetime.datetime.now()
    # resolve
    print(resolver(domain, '198.41.0.4'))
    # end time
    end_time = datetime.datetime.now()
    elapsed = end_time - start_time
    elapsed = elapsed.total_seconds() * 1000
    print("\nQUERY TIME:", end = ' ') # how much time it took to resolve the query
    print(elapsed, end = ' ')
    print("msec")
    print("WHEN:", end = ' ') # date and time of the request
    print(start_time)
    print()
