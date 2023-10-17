import re
from email import policy
from email.parser import BytesParser
from datetime import datetime

def analyse_eml_datei(dateipfad):
    with open(dateipfad, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    received_headers = list(msg.get_all('Received'))
    hops = len(received_headers)
    unique_nodes = set()

    for header in received_headers:
        # Extrahieren von Werten mit RegEx
        submitting_host_match = re.search(r'from\s+([\w\.-]+)', header)
        receiving_host_match = re.search(r'by\s+([\w\.-]+)', header)

        if submitting_host_match and submitting_host_match.group(1) != '-':
            unique_nodes.add(submitting_host_match.group(1))
        if receiving_host_match and receiving_host_match.group(1) != '-':
            unique_nodes.add(receiving_host_match.group(1))

    print(f'Anzahl der Hops: {hops}')
    print(f'Anzahl der eindeutigen Nodes: {len(unique_nodes)}')
    print('-' * 150)

    print(f'{"Hop":<5}{"Submitting Host":<30}{"Receiving Host":<30}{"Time":<30}{"Delay":<10}{"Type":<10}{"ID":<15}{"For":<30}')
    print('-' * 150)

    prev_time = None
    for idx, header in enumerate(reversed(received_headers)):
        # Extrahieren von Werten mit RegEx
        submitting_host_match = re.search(r'from\s+([\w\.-]+)', header)
        receiving_host_match = re.search(r'by\s+([\w\.-]+)', header)
        time_match = re.search(r';\s+(.+)$', header)
        type_match = re.search(r'with\s+([\w\.-]+)', header)
        id_match = re.search(r'id\s+([\w\.-]+)', header)
        for_match = re.search(r'for\s+<(.+?)>', header)

        submitting_host = submitting_host_match.group(1) if submitting_host_match else '-'
        receiving_host = receiving_host_match.group(1) if receiving_host_match else '-'
        time_str = time_match.group(1).strip() if time_match else '-'
        
        try:
            time_obj = datetime.strptime(time_str, '%a, %d %b %Y %H:%M:%S %z')
        except ValueError:
            time_obj = None
        
        delay = '-'
        if prev_time and time_obj:
            delay = str(prev_time - time_obj)
        prev_time = time_obj
        type_ = type_match.group(1) if type_match else '-'
        id_ = id_match.group(1) if id_match else '-'
        for_ = for_match.group(1) if for_match else '-'

        print(f'{idx+1:<5}{submitting_host:<30}{receiving_host:<30}{time_str:<30}{delay:<10}{type_:<10}{id_:<15}{for_:<30}')


# Test
dateipfad = 'mail.eml'
analyse_eml_datei(dateipfad)
