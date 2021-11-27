from socket import *
import time
import sys

socketClient = socket(AF_INET, SOCK_DGRAM)
server_addr = ('localhost', 12000)
socketClient.settimeout(1)

ping_count = int(sys.argv[1])
try:
    rtt_list = []
    timeout_count = 0
    for i in range(1, ping_count+1):
        start = time.time()
        message = 'Ping ' + str(i) + " " + time.ctime(start)
        try:
            sent = socketClient.sendto(message.encode(), server_addr)
            print("Sent message : " + message)
            data, server = socketClient.recvfrom(4096)
            print("Received message : " + data.decode())
            end = time.time()
            elapsed = (end - start)*1000
            rtt_list.append(elapsed)
            print("RTT: " + str(elapsed) + " milliseconds\n")
        except timeout:
            print("Ping " + str(i) + " Requested Time out\n")
            timeout_count += 1

    print(rtt_list)
    print("max : "+"{:.2f}".format(max(rtt_list)))
    print("min : "+"{:.2f}".format(min(rtt_list)))
    print("avg : "+"{:.2f}".format(sum(rtt_list)/len(rtt_list)))
    print(f"packet loss : "+"{:.2f}".format(timeout_count*100/ping_count)+" %")
finally:
    print("closing socket")
    socketClient.close()
