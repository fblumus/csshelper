from email import message_from_file
from email.utils import getaddresses, parseaddr
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def eml_graph(filename):
    with open(filename, 'r') as f:
        msg = message_from_file(f)

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

G, source_addr, original_to = eml_graph("mail.eml")

# print edges with message subject
for u, v, d in G.edges(data=True):
    print(f"From: {u} To: {v} Subject: {d['message']['Subject']}")

draw_colored_graph(G, source_addr, original_to)
