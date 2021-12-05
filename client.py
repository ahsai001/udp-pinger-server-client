from socket import *
import time
import sys


address = sys.argv[1]
port = int(sys.argv[2])
ping_count = int(sys.argv[3])
hb_ttl = int(sys.argv[4])

socketClient = socket(AF_INET, SOCK_DGRAM)
server_addr = (address, port)
socketClient.settimeout(1)

try:
    rtt_list = []
    timeout_count = 0
    for i in range(1, ping_count+1):
        start = time.time()
        message = 'Ping ' + str(i) + " " + time.ctime(start)
        try:
            sent = socketClient.sendto(message.encode(), server_addr)
            # socketClient.setsockopt(SOL_IP, IP_TTL, hb_ttl)
            socketClient.setsockopt(SOL_IP, IP_MULTICAST_TTL, hb_ttl)

            print("Sent message : " + message)
            data, server = socketClient.recvfrom(4096)
            print("Received message : " + data.decode())
            end = time.time()
            elapsed = (end - start)*1000
            rtt_list.append(elapsed)
            # print("RTT: " + str(elapsed) + " milliseconds\n")
            str_elapsed = "{:.2f}".format(elapsed)
            print(f"SEQ {i}: Reply from {address} bytes {len(data)} time= {str_elapsed} ms, TTL: {hb_ttl}")
        except timeout:
            # print("Ping " + str(i) + " Requested Time out\n")
            print(f"SEQ {i}: Requested Time out, TTL: {hb_ttl}")
            timeout_count += 1

    # print(rtt_list)
    # print("packet loss : "+"{:.2f}".format(timeout_count*100/ping_count)+" %")
    print("")
    loss_info = "{:.2f}".format(timeout_count*100/ping_count)
    print(f"Sent= {ping_count}, Receive= {ping_count-timeout_count}, Lost= {timeout_count} ({loss_info}% loss)")
    print("avg RTT= "+"{:.2f}".format(sum(rtt_list)/len(rtt_list)))
    print("max RTT= "+"{:.2f}".format(max(rtt_list)))
    print("min RTT= "+"{:.2f}".format(min(rtt_list)))
finally:
    print("closing socket")
    socketClient.close()
