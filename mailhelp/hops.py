import re
import email
import extract_msg
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.patches as patches


filename = "mail2.msg"  # Oder "mail.msg"

if filename.endswith(".eml"):
    with open(filename, "r", encoding="utf-8") as f:
        msg = email.message_from_string(f.read())
elif filename.endswith(".msg"):
    msg_file = extract_msg.Message(filename)
    header_str = '\n'.join(f"{key}: {value}" for key, value in msg_file.header.items())
    msg_string = header_str + '\n\n' + msg_file.body
    msg = email.message_from_string(msg_string)
else:
    raise ValueError("Nicht unterstütztes Dateiformat.")

received_headers = msg.get_all('Received')
received_headers.reverse()

submitting_hosts = []
receiving_hosts = []
submitting_ips = []
receiving_ips = []
transfer_types = []

for header in received_headers:
    # Übertragungsart
    transfer_type_match = re.search(r'with\s+(\S+)', header)
    transfer_type = transfer_type_match.group(1) if transfer_type_match else "Unknown"
    transfer_types.append(transfer_type)

    # Für den sendenden Host und seine IP
    submitting_host_match = re.search(r'from\s+([\w\.-]+)', header)
    ip_match_from = re.search(r'from.*?\[([\d\.]+)\]', header)
    submitting_host = submitting_host_match.group(1) if submitting_host_match else "Unknown"
    submitting_ip = ip_match_from.group(1) if ip_match_from else ""
    submitting_hosts.append(submitting_host)
    submitting_ips.append(submitting_ip)

    # Für den empfangenden Host und seine IP
    receiving_host_match = re.search(r'by\s+([\w\.-]+)', header)
    ip_match_by = re.search(r'by.*?\[([\d\.]+)\]', header)
    receiving_host = receiving_host_match.group(1) if receiving_host_match else "Unknown"
    receiving_ip = ip_match_by.group(1) if ip_match_by else ""
    receiving_hosts.append(receiving_host)
    receiving_ips.append(receiving_ip)

hops_with_data = list(zip(submitting_hosts, submitting_ips, transfer_types, receiving_hosts, receiving_ips))

print("\nHops:")
for i, (submitting, submit_ip, transfer_type, receiving, receive_ip) in enumerate(hops_with_data):
    print(f"Hop {i + 1}: FROM: {submitting} ({submit_ip}) -> BY: {receiving} ({receive_ip}) WITH: {transfer_type}")

redirected_from = msg.get('X-Sieve-Redirected-From')
if redirected_from:
    print(f"\nMail wurde von {redirected_from} weitergeleitet.")

G = nx.DiGraph()

node_positions = {}
label_positions = {}

for i, (submit_host, submit_ip, transfer_type, receive_host, receive_ip) in enumerate(hops_with_data):
    from_node = f"FROM: {submit_host}\n{submit_ip}"
    by_node = f"BY: {receive_host}\n{receive_ip}"

    G.add_edge(from_node, by_node, label=f"HOP {i+1}\nWITH: {transfer_type}")

    # Positioniere die Knoten vertikal
    node_positions[from_node] = (0, -i*2)
    node_positions[by_node] = (1, -i*2)

    # Einstellungen für die Labelpositionen
    label_positions[from_node] = (0, -i*2 + 0.5)
    label_positions[by_node] = (1, -i*2 + 0.5)

fig, ax = plt.subplots(figsize=(15, 10))
edges = G.edges(data=True)

# Einstellung für eine feste Knotengröße
node_sizes = [5000 for _ in G.nodes()]

# Einstellung für die Beschriftungsposition (leicht nach oben verschoben, damit sie zentraler erscheinen)
label_pos = {k: (v[0], v[1] - 0.5) for k, v in node_positions.items()}

# Knoten und Kanten zeichnen
nx.draw(G, pos=node_positions, node_size=node_sizes, node_shape='s', node_color="lightgreen", edge_color="green", ax=ax, width=2, font_size=8, alpha=0.8, arrowstyle="-", arrowsize=15)

# Beschriftungen für Knoten und Kanten hinzufügen
nx.draw_networkx_labels(G, label_pos, labels={node: node.split(": ")[1] for node in G.nodes()}, font_size=8, horizontalalignment='center', verticalalignment='center')
nx.draw_networkx_labels(G, label_positions, labels={node: node.split(": ")[0] + ":" for node in G.nodes()}, font_size=12)
nx.draw_networkx_edge_labels(G, pos=node_positions, edge_labels={(u, v): data['label'] for u, v, data in edges}, font_size=12)

# Manuell Pfeile zwischen den Hops zeichnen
for i in range(len(hops_with_data) - 1):
    x = 0.5  # Zwischen FROM und BY Knoten
    y_start = -i*2 - 0.5  # Ein wenig unterhalb des aktuellen Hops
    y_end = -i*2 - 1.5  # Ein wenig oberhalb des nächsten Hops
    ax.arrow(x, y_start, 0, y_end - y_start, head_width=0.01, head_length=0.15, fc='green', ec='green')

plt.title("Mail Transfer Visualization")
plt.axis('off')
plt.tight_layout()
plt.show()