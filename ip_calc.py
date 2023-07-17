def better(var):
    return var[:len(var)-1]


def bin_ip(ip):
    ip_bin = ""

    ips = ip.split(".")

    for z in ips:
        z = int(z)

        bny = bin(z)

        if len(bny[2:]) != 8:
            bny = bny.replace("0b",f"{'0'* (8-len(bny[2:]))}")
        else:
            bny = bny[2:]
        

        ip_bin += f"{bny}."

    return better(ip_bin)


def subnet_mask(ip):
    mask = int(ip.split("/")[1])
    sb_mask = ""

    if mask % 8 == 0:
        n = round(mask / 8)

        for _ in range(n):
            sb_mask += "255."
        
        rem = 4 - n

        for _ in range(rem):
            sb_mask += "0."
    
    else:
        finish = False
        n = 0
        av = 0

        while(finish == False):
            n+= 8

            if n > mask:
                bit = mask - (n - 8)
                finish = True
            else:
                av+= 1

        for x in range(av+1):
            if x == av:
                block = "1"*bit

                for _ in range(8 - len(block)):
                    block+= "0"
                
                sb_mask += f"{str(int(block,2))}."
            else:
                sb_mask+= "255."

        for x in range(5 - len(sb_mask.split("."))):
            sb_mask += "0."

    return better(sb_mask)


def logic(ip1,ip2,t):
    net_brd_id = ""

    ip1 = ip1.split(".")
    ip2 = ip2.split(".")

    for x in range(len(ip1)):
        if t == "AND":
            res = int(ip1[x],2) & int(ip2[x],2)
        elif t == "OR":
            res = int(ip1[x],2) | int(ip2[x],2)
        
        net_brd_id+= f"{res}."

    return better(net_brd_id)



def hosts_calc(ip1,ip2):
    hosts = 1

    ip1 = ip1.split(".")
    ip2 = ip2.split(".")

    for x in range(len(ip1)):
        if ip1[x] != ip2[x]:
            hosts *= int(ip2[x]) - int(ip1[x]) + 1

    return hosts



#CIDR NOTATION => 192.168.0.0/24 | ip/subnetmask
#ip_mask = str(input("IP ADDRESS => "))

ip_mask = "192.168.0.0/24"

mask = ip_mask.split("/")[1]
ip = ip_mask.replace(f"/{mask}","")

if (int(mask) < 32):
    binary_ip = bin_ip(ip)
    submask = subnet_mask(ip_mask)
    binary_submask = bin_ip(submask)

    neg_binary_submask = ""
    for x in binary_submask:
        if x == "0":
            x = "1"
        elif x == "1":
            x = "0"
        else:
            x = "."
        
        neg_binary_submask+= x



    network_id = logic(binary_ip,binary_submask,"AND")
    broadcast_id = logic(binary_ip,neg_binary_submask,"OR")

    hosts = hosts_calc(network_id,broadcast_id)
    potential_hosts = hosts - 2

    print(f"\nRESULTS FOR => `{ip_mask}`\n\nIP => {ip}\nBINARY_IP => {binary_ip}\n\nSUBNETMASK => {submask}\nBINARY_SUBNETMASK => {binary_submask}\nNEG_BINARY_SUBNETMASK => {neg_binary_submask}\n\nNETWORK_ID => {network_id} | {bin_ip(network_id)}\nBROADCAST_ID => {broadcast_id} | {bin_ip(broadcast_id)}\n\nHOSTS => {hosts}\nPOTENTIAL HOSTS => {potential_hosts}\n")

else:
    print("\nERROR: SubNet Mask must be equal or less than 32")