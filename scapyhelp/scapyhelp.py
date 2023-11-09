from scapy.all import *

def analyze_pcap(pcap_file):
    packets = rdpcap(pcap_file)
    handshakes = []

    # Analyze TCP handshakes
    for i, pkt in enumerate(packets[:20]):
        if pkt.haslayer(TCP):
            tcp_layer = pkt[TCP]
            # Check for SYN, not ACK flags which indicate handshake initiation
            if 'S' in tcp_layer.flags and 'A' not in tcp_layer.flags:
                syn_frame = i + 1
                # SYN Packet found, now look for corresponding SYN-ACK
                for j in range(i+1, len(packets)):
                    if packets[j].haslayer(TCP):
                        tcp_resp = packets[j][TCP]
                        # Check for SYN-ACK which indicates a handshake response
                        if 'S' in tcp_resp.flags and 'A' in tcp_resp.flags and tcp_resp.ack == tcp_layer.seq + 1:
                            syn_ack_frame = j + 1
                            # SYN-ACK Packet found, now look for corresponding ACK
                            for k in range(j+1, len(packets)):
                                if packets[k].haslayer(TCP):
                                    tcp_ack = packets[k][TCP]
                                    # Check for ACK which completes the handshake
                                    if 'A' in tcp_ack.flags and 'S' not in tcp_ack.flags and tcp_ack.ack == tcp_resp.seq + 1:
                                        ack_frame = k + 1
                                        handshakes.append((syn_frame, syn_ack_frame, ack_frame))
                                        break
                            break

    # Output the handshakes
    for hs in handshakes:
        print(f"Handshake packets: Client SYN: {hs[0]} -> Server SYN / ACK: {hs[1]} -> Client ACK: {hs[2]}")

    # Output the total number of handshakes
    print(f"Total number of handshakes: {len(handshakes)}")

    # Your existing code for requests and User-Agent extraction can remain unchanged here...

# Replace 'path_to_pcap.pcap' with your actual PCAP file path
pcap_path = 'c6-traffic.pcap'
analyze_pcap(pcap_path)

