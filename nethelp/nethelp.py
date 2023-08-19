import tkinter as tk
from tkinter import Entry, Label, Button, Text, Scrollbar, StringVar


def is_valid_ip(ip):
    try:
        octets = ip.split('.')
        if len(octets) != 4:
            return False
        for octet in octets:
            if not 0 <= int(octet) <= 255:
                return False
        return True
    except:
        return False
    
def ip_to_binary(ip):
    return ''.join([bin(int(x)).replace("0b", "").rjust(8, '0') for x in ip.split(".")])

def binary_to_ip(binary_str):
    return '.'.join([str(int(binary_str[i:i+8], 2)) for i in range(0, 32, 8)])

def calculate_network_address(ip, mask):
    ip_bin = ip_to_binary(ip)
    net_bits = ip_bin[:mask] + "0" * (32 - mask)
    return binary_to_ip(net_bits), net_bits

def calculate_broadcast_address(ip, mask):
    ip_bin = ip_to_binary(ip)
    broadcast_bits = ip_bin[:mask] + "1" * (32 - mask)
    return binary_to_ip(broadcast_bits), broadcast_bits

def first_last_address(net_bits, broadcast_bits):
    first_address_bin = net_bits[:-1] + "1"
    first_address = binary_to_ip(first_address_bin)
    last_address_bin = broadcast_bits[:-1] + "0"
    last_address = binary_to_ip(last_address_bin)
    return first_address, first_address_bin, last_address, last_address_bin

def number_of_hosts(mask):
    return 2 ** (32 - mask) - 2

def calculate():
    try:
        ip, cidr = input_var.get().split("/")
        
        if not is_valid_ip(ip):
            raise ValueError("Ungültige IP-Adresse!")

        mask = int(cidr)
        if not (0 <= mask <= 32):
            raise ValueError("Ungültige CIDR-Notation!")

        network_address, net_bits = calculate_network_address(ip, mask)
        broadcast_address, broadcast_bits = calculate_broadcast_address(ip, mask)
        first_address, first_address_bin, last_address, last_address_bin = first_last_address(net_bits, broadcast_bits)
        num_addresses = number_of_hosts(mask)

        output = "\nBinäre Darstellung und ihre dezimalen Äquivalente:\n"
        output += "----------------------------------\n"
        output += "128 | 64 | 32 | 16 | 8 | 4 | 2 | 1\n\n"
        output += f"Eingegebene IP (binär): {ip_to_binary(ip)}\n\n"

        output += "Rechnungsweg:\n"
        output += "----------------------------------\n"
        output += f"Netzwerkadresse:\n"
        output += f"Eingegebene IP (binär): {ip_to_binary(ip)}\n"
        output += f"Setze die letzten {32-mask} Bits (Host-Bits) auf '0': {net_bits}\n"
        output += f"Ergebnis: {network_address}\n\n"

        output += f"Broadcast-Adresse:\n"
        output += f"Eingegebene IP (binär): {ip_to_binary(ip)}\n"
        output += f"Setze die letzten {32-mask} Bits (Host-Bits) auf '1': {broadcast_bits}\n"
        output += f"Ergebnis: {broadcast_address}\n\n"
        
        output += f"Erste nutzbare Adresse:\n"
        output += f"Netzwerkadresse (binär): {net_bits}\n"
        output += f"Erhöhe den letzten Bit um 1: {first_address_bin}\n"
        output += f"Ergebnis: {first_address}\n\n"
        
        output += f"Letzte nutzbare Adresse:\n"
        output += f"Broadcast-Adresse (binär): {broadcast_bits}\n"
        output += f"Verringere den letzten Bit um 1: {last_address_bin}\n"
        output += f"Ergebnis: {last_address}\n\n"
        
        output += f"Anzahl der verfügbaren Adressen: {num_addresses}\n"

        result_text.delete(1.0, tk.END)  
        result_text.insert(tk.END, output)

    except ValueError as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, str(e))
    except Exception as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Ein unerwarteter Fehler ist aufgetreten: {str(e)}")

root = tk.Tk()
root.title("Subnetzrechner")

Label(root, text="Geben Sie das Netzwerk ein (z.B. 192.168.0.0/24)").pack(pady=10)
input_var = StringVar()
Entry(root, textvariable=input_var, width=25).pack(pady=10)
Button(root, text="Berechnen", command=calculate).pack(pady=10)

scrollbar = Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text = Text(root, wrap=tk.WORD, yscrollcommand=scrollbar.set, height=20, width=50)
result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
scrollbar.config(command=result_text.yview)

root.mainloop()
