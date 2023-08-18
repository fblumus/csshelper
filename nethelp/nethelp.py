import tkinter as tk
from tkinter import Entry, Label, Button, Text, Scrollbar, StringVar


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

def first_last_address(ip, mask):
    network_address, net_bits = calculate_network_address(ip, mask)
    broadcast_address, broadcast_bits = calculate_broadcast_address(ip, mask)
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
        mask = int(cidr)

        network_address, net_bits = calculate_network_address(ip, mask)
        broadcast_address, broadcast_bits = calculate_broadcast_address(ip, mask)
        first_address, first_address_bin, last_address, last_address_bin = first_last_address(ip, mask)
        num_addresses = number_of_hosts(mask)

        output = f"Eingegebene IP (binär): {ip_to_binary(ip)}\n\n"
        
        output += f"Netzwerkadresse: {network_address}\n"
        output += f"Setze die letzten {32-mask} Bits (Host-Bits) auf '0'.\n"
        output += f"Ergebnis (binär): {net_bits}\n\n"
        
        output += f"Broadcast-Adresse: {broadcast_address}\n"
        output += f"Setze die letzten {32-mask} Bits (Host-Bits) auf '1'.\n"
        output += f"Ergebnis (binär): {broadcast_bits}\n\n"
        
        output += f"Erste nutzbare Adresse: {first_address}\n"
        output += f"Netzwerkadresse + 1.\n"
        output += f"Ergebnis (binär): {first_address_bin}\n\n"
        
        output += f"Letzte nutzbare Adresse: {last_address}\n"
        output += f"Broadcast-Adresse - 1.\n"
        output += f"Ergebnis (binär): {last_address_bin}\n\n"
        
        output += f"Anzahl der verfügbaren Adressen: {num_addresses}\n"

        result_text.delete(1.0, tk.END)  
        result_text.insert(tk.END, output)

    except ValueError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Ungültige Eingabe!")
    except Exception as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, str(e))

root = tk.Tk()
root.title("Subnetzrechner")

Label(root, text="Geben Sie das Netzwerk ein (z.B. 192.168.0.0/24)").pack(pady=10)
input_var = StringVar()
Entry(root, textvariable=input_var).pack(pady=10)
Button(root, text="Berechnen", command=calculate).pack(pady=10)

scrollbar = Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text = Text(root, wrap=tk.WORD, yscrollcommand=scrollbar.set)
result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
scrollbar.config(command=result_text.yview)

root.mainloop()
