import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import tempfile


def create_dropdown_menu(window, text, values, info, detail_info):
    frame = tk.Frame(window)
    frame.pack(fill=tk.X, padx=10, pady=5)
    var = tk.StringVar()
    label = tk.Label(frame, text=text, width=20 ,anchor='w')
    label.pack(side=tk.LEFT)
    dropdown = ttk.Combobox(frame, textvariable=var, values=values, width=30)
    dropdown.pack(side=tk.LEFT)
    button = tk.Button(frame, text="?", command=lambda: show_info(info, detail_info))  # pass detail_info here
    button.pack(side=tk.RIGHT)
    return var


def create_target_entry(window, text, info):
    frame = tk.Frame(window)
    frame.pack(fill=tk.X, padx=10, pady=5)
    label = tk.Label(frame, text=text, width=20 ,anchor='w')
    label.pack(side=tk.LEFT)
    entry = tk.Entry(frame, width=31)
    entry.pack(side=tk.LEFT)
    button = tk.Button(frame, text="?", command=lambda: show_info(info))
    button.pack(side=tk.RIGHT)
    return entry


def run_command():
    command = ["nmap", "--privileged"]
    if scan_var.get():
        command.append(scan_var.get())
    if extra_var.get():
        command.append(extra_var.get())
    if port_var.get():
        command.append(port_var.get())
    if host_discovery_var.get():    
        command.append(host_discovery_var.get())
    if version_detection_var.get():   
        command.append(version_detection_var.get())
    if firewall_proofing_var.get():  
        command.append(firewall_proofing_var.get())
    if target_entry.get():
        command.append(target_entry.get())
    else:   
        tk.messagebox.showerror("Fehler", "Bitte geben Sie ein Ziel an.")
        return
    
    command_str = " ".join(command)

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        temp_file.write("Input:\n" + command_str + "\n\nOutput:\n")
        temp_file.flush()
        subprocess.run(command, stdout=temp_file)

    subprocess.Popen(["xdg-open", temp_file.name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def show_info(message, detail_message):
    info_window = tk.Toplevel(window)
    info_window.geometry('400x600')
    info_window.title("Information")

    scrollbar = tk.Scrollbar(info_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    info_text = tk.Text(info_window, wrap=tk.WORD, yscrollcommand=scrollbar.set)  
    info_text.insert(tk.END, message)
    info_text.pack(anchor='nw', padx=10, pady=10, fill=tk.BOTH, expand=True)
    info_text.configure(state='disabled')

    scrollbar.config(command=info_text.yview)

    button_frame = tk.Frame(info_window)
    button_frame.pack(fill=tk.X, padx=10, pady=10)

    ok_button = tk.Button(button_frame, text="OK", command=info_window.destroy)
    ok_button.pack(side=tk.LEFT)

    detail_button = tk.Button(button_frame, text="?", command=lambda: show_info_detail(detail_message))
    detail_button.pack(side=tk.RIGHT)


def show_info_detail(message):
    info_window = tk.Toplevel(window)
    info_window.geometry('800x600')
    info_window.title(" Detail Information")

    scrollbar = tk.Scrollbar(info_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    info_text = tk.Text(info_window, wrap=tk.WORD, yscrollcommand=scrollbar.set)  
    info_text.insert(tk.END, message)
    info_text.pack(anchor='nw', padx=10, pady=10, fill=tk.BOTH, expand=True)
    info_text.configure(state='disabled')

    scrollbar.config(command=info_text.yview)

    ok_button = tk.Button(info_window, text="Close", command=info_window.destroy)  
    ok_button.pack(pady=10)


window = tk.Tk()
window.title("nmaphelp")
window.geometry('500x400')

scan_types = ["-sT", "-sS", "-sA", "-sW", "-sM", "-sN", "-sF", "-sX", "-sI", "-sY", "-sZ", "-sU", "-sO"] # -sT	TCP Connect scan, -sS	TCP SYN / stealth / half-open scan, -sA	TCP ACK scan, -sW	TCP Window scan, -sM	TCP Maimon scan (FIN/ACK flags), -sN	TCP Null scan (no flags) ,-sF	TCP FIN scan, -sX	TCP Xmass scan (all flags), -sI	TCP Zombie / Idle scan ,-sY	SCTP INIT scan, -sZ	SCTP COOKIE ECHO scan ,-sU	UDP scan, -sO	IP protocol scan
port_types = ["-p", "-F", "-p-"]
host_discovery_types = ["-sn", "-Pn"]
version_detection_types = ["-sV", "-A", "-O"]
firewall_proofing_types = ["-f", "-mtu", "sI", "-source-port", "-data-length", "-randomize-hosts", "-badsum"]
extra_options = ["-v"]


help_scan_types = "Der Scantyp bestimmt, wie die Ports gescannt werden.\n\n-sT: TCP Connect Scan\n-sS: TCP SYN Scan\n-sA: TCP ACK Scan\n-sW: TCP Window Scan\n-sM: TCP Maimon Scan\n-sN: TCP Null Scan\n-sF: TCP FIN Scan\n-sX: TCP Xmass Scan\n-sI: TCP Zombie / Idle Scan\n-sY: SCTP INIT Scan\n-sZ: SCTP COOKIE ECHO Scan\n-sU: UDP Scan\n-sO: IP Protocol Scan"
help_scan_types_detail = """
TCP Connect Scan: 
Dies ist der grundlegendste Typ eines Portscans. Es verwendet den vollständigen Drei-Wege-Handshake von TCP (SYN-SYN/ACK-ACK). Wenn der Port offen ist, wird der vollständige Handshake abgeschlossen und die Verbindung sofort danach geschlossen. Diese Methode ist zuverlässig, aber nicht subtil - sie wird sehr leicht von IDS/IPS-Systemen erkannt.

Angreifer                                   Ziel-Host
--------                                   ---------
   |                                            |
   |    (1) SYN-Paket (Port-Scan-Anfrage)       |
   | --------------------------------------->   |
   |                                            |
   |       (2) SYN/ACK-Paket (Port offen)       |
   | <---------------------------------------   |
   |                                            |
   |        (3) ACK-Paket (Verbindung beenden)  |
   | --------------------------------------->   |
   |                                            |

TCP SYN (Stealth/Half-open) Scan: 
Dieser Scan-Typ wird auch als "halboffener" Scan bezeichnet. Anstatt einen vollständigen TCP-Handshake abzuschließen, sendet der Scanner ein SYN-Paket und wartet auf eine SYN/ACK-Antwort, um zu bestätigen, dass der Port offen ist. Da der Handshake nicht abgeschlossen wird (das abschließende ACK wird nicht gesendet), ist dieser Scan schwieriger für IDS/IPS-Systeme zu erkennen.

Angreifer                                   Ziel-Host
--------                                   ---------
   |                                            |
   |       (1) SYN-Paket (Port-Scan-Anfrage)    |
   | --------------------------------------->   |
   |                                            |
   |        (2) SYN/ACK-Paket (Port offen)      |
   | <---------------------------------------   |
   |                                            |
   |          (3) (Keine ACK-Antwort)           |
   |                                          X |
   |                                            |

TCP ACK Scan: Dieser Scan wird verwendet, um festzustellen, ob ein Port gefiltert ist oder nicht. Er ist nicht in der Lage, offene Ports zu ermitteln, aber er kann Firewall-Regeln und Filterung identifizieren.

Angreifer                                   Ziel-Host
--------                                   ---------
   |                                            |
   |     (1) ACK-Paket (Port-Scan-Anfrage)      |
   | --------------------------------------->   |
   |                                            |
   |        (2) (Keine Antwort)                 |
   |          (Gefilterter Port)              X |
   |                                            |

TCP Window Scan: Dieser Scan ähnelt dem ACK-Scan, nutzt aber eine Eigenschaft von TCP-Window-Größen, um den Status des Ports festzustellen. Er ist weniger verbreitet und funktioniert nicht immer, da er stark von der spezifischen TCP/IP-Implementierung des Zielsystems abhängt.

Angreifer                                   Ziel-Host
--------                                   ---------
   |                                            |
   |     (1) SYN-Paket (Port-Scan-Anfrage)      |
   | --------------------------------------->   |
   |                                            |
   |        (2) (Keine Antwort)                 |
   |          (Gefilterter Port)              X |
   |                                            |

TCP Maimon Scan: Benannt nach seinem Entdecker, Uriel Maimon. Er sendet Pakete mit FIN/ACK-Flags und erwartet, dass geschlossene Ports mit RST/ACK antworten, während offene Ports keine Antwort senden.

Angreifer                                   Ziel-Host
--------                                   ---------
   |                                            |
   |    (1) FIN/ACK-Paket (Port-Scan-Anfrage)   |
   | --------------------------------------->   |
   |                                            |
   |        (2) (Keine Antwort)                 |
   |          (Offener Port)                  X |
   |                                            |

TCP Null Scan (no flags): In diesem Scan werden Pakete ohne gesetzte TCP-Flags gesendet. Da solche Pakete gegen die TCP-Spezifikationen verstoßen, reagieren Systeme unterschiedlich darauf. Im Allgemeinen wird erwartet, dass offene Ports keine Antwort senden und geschlossene Ports mit RST antworten.

Angreifer                                   Ziel-Host
--------                                   ---------
   |                                            |
   |    (1) Paket ohne TCP-Flags                |
   | --------------------------------------->   |
   |                                            |
   |       (2) (Keine Antwort)                  |
   |          (Offener Port)                  X |
   |                                            |

TCP FIN Scan: Ein FIN-Scan sendet ein Paket mit dem FIN-Flag, um einen offenen Port zu erkennen. Geschlossene Ports sollten mit einem RST-Paket antworten, während offene Ports keine Antwort senden.

Angreifer                                   Ziel-Host
--------                                   ---------
   |                                            |
   |        (1) FIN-Paket (Port-Scan-Anfrage)   |
   | --------------------------------------->   |
   |                                            |
   |       (2) (Keine Antwort)                  |
   |          (Offener Port)                  X |
   |                                            |


TCP Xmas Scan (all flags): Ein Xmas-Scan sendet ein Paket mit allen TCP-Flags gesetzt. Wie beim Null- und FIN-Scan wird erwartet, dass offene Ports nicht antworten und geschlossene Ports ein RST-Paket zurücksenden.

Angreifer                                   Ziel-Host
--------                                   ---------
   |                                            |
   |    (1) Paket mit allen TCP-Flags gesetzt (Port-Scan-Anfrage) |
   | --------------------------------------->   |
   |                                            |
   |       (2) (Keine Antwort)                  |
   |          (Offener Port)                  X |
   |                                            |

TCP Zombie/Idle Scan: Ein Idle Scan verwendet ein "Zombie"-Gerät, um Ports zu scannen. Es wird versucht, das Gerät zu scannen, ohne direkten Kontakt mit ihm aufzunehmen. Dies ist nützlich, um die Erkennung durch Netzwerksicherheitssysteme zu vermeiden.\n

Angreifer                                   Zombie                                 Ziel-Host
--------                                   ------                                 ---------
   |                                            |                                       |
   |  (1) SYN-Scan auf Zombie durchführen       |                                       |
   | -------------------------------------->    |                                       |
   |                                            |                                       |
   |       (2) Geeigneten Ziel-Host suchen      |                                       |
   | -------------------------------------->    |                                       |
   |                                            |                                       |
   |      (3) SYN-Paket an Zombie senden        |                                       |
   |            (gefälschte Absender-IP)        |                                       |
   | -------------------------------------->    |                                       |
   |                                            |                                       |
   |                                            |   (4) Verbindungsaufbau zum Ziel-Host |
   |                                            | ------------------------------------> |
   |                                            |                                       |
   |      (5) SYN/ACK oder RST/ACK Antwort      |                                       |
   | <--------------------------------------    |                                       |
   |                                            |                                       |
   |      (6) Ziel-Port offen oder geschlossen  |                                       |
   | -------------------------------------->    |                                       |
   |                                            |                                       |

SCTP INIT Scan und SCTP COOKIE ECHO Scan: Diese sind spezifische Scans für das SCTP-Protokoll (Stream Control Transmission Protocol), das eine Alternative zu TCP und UDP ist. INIT wird verwendet, um neue Verbindungen zu initialisieren, während COOKIE ECHO verwendet wird, um bestehende Verbindungen aufrechtzuerhalten.\n

SCTP INIT Scan:

Angreifer                                   Ziel-Host
--------                                   ---------
   |                                            |
   |       (1) INIT-Chunks (Verbindungsinitiierung) |
   | ---------------------------------------> |
   |                                            |
   |        (2) INIT-ACK-Antwort (Port offen)    |
   | <--------------------------------------  |
   |                                            |
   |        (3) (Keine INIT-ACK-Antwort)         |
   |          (Port geschlossen)              X |
   |                                            |

SCTP COOKIE ECHO Scan:

Angreifer                                   Ziel-Host
--------                                   ---------
   |                                            |
   |   (1) Bestehendes SCTP-Verbindungscookie suchen   |
   | ---------------------------------------> |
   |                                            |
   |   (2) COOKIE ECHO-Chunks (Verbindung aufrechterhalten) |
   |   (mit dem Verbindungscookie)            |
   | ---------------------------------------> |
   |                                            |
   |        (3) COOKIE ECHO-Antwort (Port offen) |
   | <--------------------------------------  |
   |                                            |
   |       (4) (Keine COOKIE ECHO-Antwort)       |
   |         (Port geschlossen oder inaktiv)   X |
   |                                            |


UDP Scan: Ein UDP-Scan sendet ein leeres UDP-Paket an jeden Port. Offene Ports sollten in der Regel mit einem ICMP Port Unreachable Paket antworten, wenn sie nicht in Gebrauch sind.\n

Angreifer                                   Ziel-Host
--------                                   ---------
   |                                            |
   |       (1) Leeres UDP-Paket (Port-Scan-Anfrage)    |
   | ---------------------------------------> |
   |                                            |
   |        (2) ICMP Port Unreachable (Port geschlossen) |
   | <---------------------------------------  |
   |                                            |
   |         (3) (Keine Antwort)                  |
   |          (Offener Port)                  X |
   |                                            |

IP Protocol Scan: Dieser Scan identifiziert, welche IP-Protokolle (wie TCP, UDP, ICMP, etc.) auf einem System verfügbar sind. Es wird durch Senden von IP-Paketen ohne zusätzliche Schicht 4 (TCP/UDP/etc.) durchgeführt. Jedes Protokoll, das nicht mit einem ICMP Protocol Unreachable Nachricht reagiert, wird als verfügbar betrachtet.\n

Angreifer                                   Ziel-Host
--------                                   ---------
   |                                            |
   |       (1) IP-Paket ohne Schicht 4 (Port-Scan-Anfrage) |
   | ---------------------------------------> |
   |                                            |
   |        (2) ICMP Protocol Unreachable (Protokoll nicht verfügbar) |
   | <---------------------------------------  |
   |                                            |
   |        (3) (Keine ICMP-Antwort)             |
   |         (Protokoll verfügbar)            X |
   |                                            |

"""


help_port_types = "Die Auswahl des Portbereichs bestimmt, welche Ports gescannt werden.\n\n-p: Portbereich\n-F: Fast Scan\n-p-: Alle Ports"
help_port_types_detail = ""

help_host_discovery_types = "Die Option Host Discovery bestimmt, wie die Zielhosts gefunden werden.\n\n-sn: Ping Scan\n-Pn: Kein Ping"
help_host_discovery_types_detail = ""

help_version_detection_types = "Die Option Version Detection erlaubt die Erkennung der verwendeten Software und deren Versionen auf dem Zielhost.\n\n-sV: Version Detection\n-A: Aggressive Version Detection\n-O: OS Detection"
help_version_detection_types_detail = ""

help_firewall_proofing_types = "Die Option Firewall Proofing versucht, Firewalls und Intrusion Detection Systems zu umgehen.\n\n-f: Fragmentierung\n-mtu: MTU Discovery\n-sI: Idle Scan\n-source-port: Source Port\n-data-length: Data Length\n-randomize-hosts: Randomize Hosts\n-badsum: Bad Checksum"
help_firewall_proofing_types_detail = ""

help_extra_options = "Die zusätzlichen Optionen erlauben spezielle Einstellungen und Befehle.\n\n-v: Verbose Output"
help_extra_options_detail = ""

help_target = "Das Ziel kann eine IP-Adresse, ein Hostname oder eine IP-Range sein."
help_target_detail = ""


scan_var = create_dropdown_menu(window, "Scantyp:", scan_types, help_scan_types, help_scan_types_detail)
port_var = create_dropdown_menu(window, "Portbereich:", port_types, help_port_types, help_port_types_detail)
host_discovery_var = create_dropdown_menu(window, "Host Discovery:", host_discovery_types, help_host_discovery_types, help_host_discovery_types_detail)
version_detection_var = create_dropdown_menu(window, "Version Detection:", version_detection_types, help_version_detection_types, help_version_detection_types_detail)
firewall_proofing_var = create_dropdown_menu(window, "Firewall Proofing:", firewall_proofing_types, help_firewall_proofing_types, help_firewall_proofing_types_detail)
extra_var = create_dropdown_menu(window, "Zusätzliche Optionen:", extra_options, help_extra_options, help_extra_options_detail)
target_entry = create_target_entry(window, "Target:", help_target)

run_button = tk.Button(window, text="Scan starten", command=run_command)
run_button.pack()

window.mainloop()