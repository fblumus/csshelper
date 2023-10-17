import re
import email
import networkx as nx
import matplotlib.pyplot as plt
import extract_msg
from email.utils import getaddresses, parseaddr
from matplotlib.lines import Line2D


def get_msg_from_file(filename):
    if filename.endswith(".eml"):
        with open(filename, "r", encoding="utf-8") as f:
            return email.message_from_string(f.read())
    elif filename.endswith(".msg"):
        msg_file = extract_msg.Message(filename)
        header_str = '\n'.join(f"{key}: {value}" for key, value in msg_file.header.items())
        return email.message_from_string(header_str + '\n\n' + msg_file.body)
    else:
        raise ValueError("Nicht unterstütztes Dateiformat.")


def visualize_hops(msg):
    received_headers = msg.get_all('Received')
    if not received_headers:
        print("Keine 'Received'-Header gefunden.")
        return

    received_headers.reverse()

    # Graph
    G = nx.DiGraph()

    # Vorbereiten des Plots
    plt.figure(figsize=(10, 6))
    plt.title('Email Hops Visualization')

    hops = []
    for header in received_headers:
        match = re.search(r'from\s(.*?)\sby', header)
        if match:
            hops.append(match.group(1))

    for i in range(len(hops) - 1):
        G.add_edge(hops[i], hops[i + 1])

    pos = nx.spring_layout(G, seed=227)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", node_shape="s", alpha=0.5, linewidths=40)
    plt.show()


def eml_graph(msg):
    G = nx.MultiDiGraph()  # create empty graph
    (source_name, source_addr) = parseaddr(msg["From"])  # sender

    # get all recipients
    tos = msg.get_all("to", [])
    ccs = msg.get_all("cc", [])
    resent_tos = msg.get_all("resent-to", [])
    resent_ccs = msg.get_all("resent-cc", [])
    redirected_from = msg.get_all("X-Sieve-Redirected-From", [])
    original_to = msg.get_all("X-Original-To", [])
    
    all_recipients = getaddresses(tos + ccs + resent_tos + resent_ccs)

    # Add edges for this mail message
    for target_name, target_addr in all_recipients:
        G.add_edge(source_addr, target_addr, message=msg)

    # If there's a redirection, add an edge
    if redirected_from:
        redirected_addr = getaddresses(redirected_from)[0][1]
        original_addr = getaddresses(original_to)[0][1]
        G.add_edge(redirected_addr, original_addr, message=msg, label='redirect')

    return G, source_addr, original_to


def draw_colored_graph(G, source_addr, original_to):
    node_colors = []

    for node in G.nodes():
        if node == source_addr:  # Farbe für Absender
            node_colors.append('green')
        elif node == getaddresses(original_to)[0][1]:  # Farbe für endgültigen Empfänger
            node_colors.append('blue')
        else:
            node_colors.append('red')  # Farbe für andere Knoten

    pos = nx.spring_layout(G, iterations=10, seed=227)
    nx.draw(G, pos, node_size=300, alpha=0.6, edge_color="black", font_size=16, with_labels=True, node_color=node_colors)
    ax = plt.gca()
    ax.margins(0.08)
    
    # Legende hinzufügen
    legend_elements = [Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Absender'),
                       Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Endgültiger Empfänger'),
                       Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Andere')]
    ax.legend(handles=legend_elements, loc='best')

    plt.show()


if __name__ == "__main__":
    filename = "mail.eml"  # oder "mail.eml"
    msg = get_msg_from_file(filename)

    # Visualisierung der Hops
    visualize_hops(msg)

    # Visualisierung von Absender, Empfänger und CCs
    G, source_addr, original_to = eml_graph(msg)
    for u, v, d in G.edges(data=True):
        print(f"From: {u} To: {v} Subject: {d['message']['Subject']}")
    draw_colored_graph(G, source_addr, original_to)
