#!/bin/bash
#
# vol2help.sh
#
# Copyright (c) 2023 fblumus
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
#
# This script is a helper script for volatility. It is a menu driven script to make it easier to use volatility.
# It is inspired on the volatility cheat sheet from https://book.hacktricks.xyz/generic-methodologies-and-resources/basic-forensic-methodology/memory-dump-analysis/volatility-cheatsheet
# It is not a complete script. It is a work in progress. Feel free to contribute.
#
# Author: fblumus
# Created: 2023-07-13
# Last modified: 2021-25-07
#
# Example:  ./vol2help.sh
#
# Requirements: volatility 2, jq, curl, xdg-open


# About
autor="fblumus"
version="0.2 Beta"

# Initialize variables
API_KEY="Your_API_KEY"
Cheat_Sheet="https://book.hacktricks.xyz/generic-methodologies-and-resources/basic-forensic-methodology/memory-dump-analysis/volatility-cheatsheet"
profile=""
selected_file=""
last_cmd=""
last_output=""


# ASCII-Art Logo
declare -a ascii=(
"                                                                               "
" █████   █████       ████   ████████  █████   █████         ████               "
"░░███   ░░███       ░░███  ███░░░░███░░███   ░░███         ░░███               "
" ░███    ░███ ██████ ░███ ░░░    ░███ ░███    ░███   ██████ ░███ ████████      "
" ░███    ░██████░░███░███    ███████  ░███████████  ███░░███░███░░███░░███     "
" ░░███   ███░███ ░███░███   ███░░░░   ░███░░░░░███ ░███████ ░███ ░███ ░███     "
"  ░░░█████░ ░███ ░███░███  ███      █ ░███    ░███ ░███░░░  ░███ ░███ ░███     "
"    ░░███   ░░██████ █████░██████████ █████   █████░░██████ █████░███████      "
"     ░░░     ░░░░░░ ░░░░░ ░░░░░░░░░░ ░░░░░   ░░░░░  ░░░░░░ ░░░░░ ░███░░░       "
"                                                                 ░███          "
"                                                                 █████         "
"                                                                ░░░░░          "
"                                                                               "   
)

# Main menu
declare -a menu=(
"Select File and Profile (\033[1mRequired\033[0m)"
"Hashes/Passwords"
"List processes"
"Dump proc"
"Command line"
"Environment"
"Token privileges"
"SIDs"
"Handles"
"DLLs"
"Strings per processes (not implemented yet)"
"UserAssist"
"Services"
"Network"
"Registry hive"
"Filesystem"
"SSL Keys/Certs"
"Malware"
"Scanning with yara"
"Open Volatility Cheat-Sheet"
"Quit"
)

# Submenus select file
declare -a select_file=(
"Auto-Profile (\033[1mRecommended\033[0m)"
"Manual Profile & File Selection"
"Declare VirusTotal Api-Key"
"Return"
)

# Submenus hashes
declare -a hashes=(
"hashdump  | Grab common windows hashes (SAM+SYSTEM)"
"cachedump | Grab domain cache hashes inside the registry"
"lsadump   | Get LSA secrets"
"Return"
)

# Submenus list processes
declare -a list_processes=(
"pslist  | Get process list (EPROCESS)"
"pstree  | Get process tree (not hidden)"
"psxview | Get hidden process list"
"psscan  | Get hidden process list(malware)"
"Return"
)

# Submenus dump proc
declare -a dump_proc=(
"procdump | Dump a process"
"VirusTotal | Scan a process with virustotal"
"Return"
)

# Submenus command line
declare -a command_line=(
"cmdline | Display process command-line arguments"
"consoles | command history by scanning for _CONSOLE_INFORMATION"
"Return"
)

# Submenus environment
declare -a environment=(
"envars | Display process environment variables"
"linux_psenv | Display process environment variables (Linux)"
"Return"
)

# Submenus token privileges
declare -a token_privileges=(
"privs | Display process token privileges"
"Return"
)

# Submenus sids
declare -a sids=(
"getsids | Display process token SIDs"
"getserviceids | Display process token service SIDs"
"Return"
)

# Submenus handles
declare -a handles=(
"handles | Display process handles"
"Return"
)

# Submenus dlls
declare -a dlls=(
"dlllist | List DLLs loaded by process"
"dlldump | Dump DLLs from process address space"
"Return"
)

# Submenus strings per processes
declare -a strings_per_processes=(
"string per process | Get strings per process"
"yarascan | Scan for yara signatures (not working atm)"
"Return"
)

# Submenus user_assist
declare -a user_assist=(
"userassist | Get userassist information"
"Return"
)

# Submenus services
declare -a services=(
"svcscan | Get services and binary path"
"getservicesids | Get name of the services and SID (slow)"
"Return"
)

# Submenus network
declare -a network=(
"netscan | Get network connections"
"connections | XP and 2003 only"
"connscan | TCP connections"
"sockscan | Open sockets"
"sockets | #Scanner for tcp socket objects"
"linux_ifconfig | Get network interfaces (Linux)" 
"linux_netstat | Get network connections (Linux)"
"linux_netfilter | Get netfilter connections (Linux)"
"linux_arp | Get ARP table (Linux)"
"linux_list_raw | Get raw sockets (Linux)"
"linux_route_cache | Get route cache (Linux)"
"Return"
)

# Submenus registry
declare -a registry=(
"hivelist | List roots"
"printkey | List roots and get initial subkeys"
"search for a key | Search for a key"
"dumpregistry | Dump registry hive"
"Return"
)

# Submenus filesystem
declare -a filesystem=(
"filescan | Scan for files"
"mftparser | Parse the MFT"
"dumpfiles | Dump all files"
"Return"
)

# Submenus SSL Keys/Certs
declare -a ssl_keys_certs=(
"dumpcerts | Dump certificates"
"Return"
)

# Submenus malware3
declare -a malware=(
"malfind | Find hidden and injected code [dump each suspicious section]"
"apihooks | Detect API hooks in process and kernel memory (Not Working atm)"
"driverirp | Driver IRP hook detection"
"ssdt | Check system call address from unexpected addresses (Not Working atm)"
"linux_check_afinfo | Check for hidden network sockets (Linux)"
"linux_check_creds | Check for hidden credentials (Linux)"
"linux_check_fop | Check for hidden file operations (Linux)"
"linux_check_idt | Check for hidden IDT entries (Linux)"
"linux_check_syscall | Check for hidden system calls (Linux)"
"linux_check_modules | Check for hidden modules (Linux)"
"linux_check_tty | Check for hidden TTY devices (Linux)"
"linux_keyboard_notifiers | Check for hidden keyloggers (Linux)"
)

# Submenus yara
declare -a yara=(
"yarascan | Scan for yara signatures"
"Return"
)

# Submenus cheat_sheet
declare -a cheat_sheet=(
"open cheat sheet | Open volatility cheat sheet"
"Return"
)

open_editor() { # Open the file in the editor
    ${EDITOR:-mousepad} "$1" &
}

run_and_display() { # Run volatility command and display the output
    local cmd="volatility $profile -f /data/$selected_file $1"
    [ -n "$2" ] && cmd="$cmd $2"
    [ -n "$3" ] && cmd="$cmd $3"
    cmd="$cmd "
    last_cmd="$cmd"
    
    last_output=$(eval $cmd)
    local output=$last_output
    local tempfile=$(mktemp -t $1.XXXXXX)

    echo "Command: $cmd" > "$tempfile"
    echo "Output: " >> "$tempfile"
    echo "$output" >> "$tempfile"

    open_editor "$tempfile" &

}

show_menu() { # Funktion, um das Menü anzuzeigen
    clear
    printf '%.s-' {1..80}; echo
    echo "Welcome to the Volatility Helper Script $version by $autor"
    printf '%.s-' {1..80}; echo
    for line in "${ascii[@]}"; do 
        echo -e "\e[32m$line\e[0m"
    done
    if [ ! -z "$profile" ]; then
        echo -e "Profile: \e[32m$profile\e[0m"
    fi
    if [ ! -z "$selected_file" ]; then
        echo -e "File: \e[32m$selected_file\e[0m"
    fi
    if [ ! -z "$last_cmd" ]; then
        echo -e "Last command: \e[32m$last_cmd\e[0m"
    fi
    printf '%.s-' {1..80}; echo
    for i in "${!menu[@]}"; do
        echo -e "$i) ${menu[$i]}"
    done
    printf '%.s-' {1..80}; echo

}

show_submenu() { # Funktion, um das Untermenü anzuzeigen
    clear
    submenu=("${!1}")
    printf '%.s-' {1..80}; echo
    echo "Select a command from the submenu:"
    printf '%.s-' {1..80}; echo
    for i in "${!submenu[@]}"; do
        echo -e "$i) ${submenu[$i]}"
    done
    printf '%.s-' {1..80}; echo

}

# Main function
main() {
    show_menu
    read -p "-> " choice
    case $choice in
        0) # Select File and get Auto-Profile
            show_submenu select_file[@]
            read -p "-> " subchoice_select_file
            case $subchoice_select_file in
                0)
                    clear
                    echo "Select a file:"
                    file_info=$(ls -lh | grep -v /)
                    readarray -t files <<<"$file_info"

                    # show each file with a number
                    for i in "${!files[@]}"; do 
                    echo "$i) ${files[$i]}"
                    done

                    # ask the user to select a file
                    read -p "-> " file_number

                    # get the selected file
                    selected_file_info=${files[$file_number]}
                    selected_file=$(echo $selected_file_info | awk '{print $9}')

                    # show the selected file
                    run_and_display "imageinfo"
                    profile=$(echo "$last_output" | grep 'Suggested Profile(s)' | awk -F ': ' '{print $2}' | awk -F ', ' '{print $1}')
                    profile="--profile=${profile}"
                    ;;
                1)
                    read -p "Enter profile " profile
                    profile="--profile=${profile}"
                    read -p "Enter file " selected_file
                    ;;
                2)
                    ;;
                *)  
                    echo "Invalid option."
                    ;;
            esac
            ;;
        1) # Hashes/Passwords
            show_submenu hashes[@]
            read -p "-> " subchoice_hash
            case $subchoice_hash in
                0)
                    run_and_display "hashdump"
                    ;;
                1)
                    run_and_display "cachedump"
                    ;;
                2)
                    run_and_display "lsadump"
                    ;;
                3)
                    ;;
                *)
                    echo "Invalid option."
                    ;;
            esac
            ;;
        2) # List processes
            show_submenu list_processes[@]
            read -p "-> " subchoice_list_processes
            case $subchoice_list_processes in
                0)
                    run_and_display "pslist"
                    ;;
                1)
                    run_and_display "pstree"
                    ;;
                2)
                    run_and_display "psxview"
                    ;;
                3)
                    run_and_display "psscan"
                    ;;
                4)
                    ;;
                *)
                    echo "Invalid option."
                    ;;
            esac
            ;;
        3) # Dump proc
            show_submenu dump_proc[@]
            read -p "-> "subchoice_dump_proc
            case $subchoice_dump_proc in

                0)
                    mkdir -p ./procdump 
                    run_and_display "procdump" "-D ./procdump"
                    ;;
                1)
                    echo "Ever 15 seconds a dump file will be checked by VirusTotal"
                    for file in ./procdump/*.exe; do
                        sha1=$(sha1sum $file | awk '{ print $1 }')
                        echo "Checking file $file with SHA1 $sha1"
                        response=$(curl --request GET \
                        --url https://www.virustotal.com/api/v3/files/$sha1 \
                        --header "x-apikey: $API_KEY" | jq '.data.attributes.last_analysis_stats')

                        positives=$(echo $response | jq '.malicious + .suspicious')
                        undetected=$(echo $response | jq '.undetected')

                        if [ $positives -gt 0 ]; then
                            printf '%.s-' {1..80}; echo
                            echo "file $file - $sha1 is potentially infected. Positives: $positives"
                            printf '%.s-' {1..80}; echo
                        else
                            printf '%.s-' {1..80}; echo
                            echo "file $file - $sha1 is clean. Undetected: $undetected"
                            printf '%.s-' {1..80}; echo
                        fi

                        filename=$(basename $file)
                        echo "$response" > "./procdump/$filename.$sha1.json"
                        sleep 15
                    done
                    echo "Press Enter to continue"
                    read -s -n 1 -p ""
                    ;;
                2)
                    ;;
                *)
                    echo "Invalid option."
                    ;;
            esac
            ;;


        4) # Command line
            show_submenu command_line[@]
            read -p "-> " subchoice_command_line
            case $subchoice_command_line in
                0)
                    run_and_display "cmdline"
                    ;;
                1)
                    run_and_display "consoles"
                    ;;
                2)
                    ;;
                *)
                    echo "Invalid option."
                    ;;
            esac
            ;;
        5) # Environment
            show_submenu environment[@]
            read -p "-> " subchoice_environment
            case $subchoice_environment in
                0)
                    run_and_display "envars"
                    ;;
                1)
                    run_and_display "linux_psenv"
                    ;;
                2)
                    ;;
                *)
                    echo "Invalid option."
                    ;;
            esac
            ;;
        6) # Token privileges
            show_submenu token_privileges[@]
            read -p "-> " subchoice_token_privileges
            case $subchoice_token_privileges in
                0)
                    run_and_display "privs"
                    ;;
                1)
                    ;;
                *)
                    echo "Invalid option."
                    ;;
            esac
            ;;
        7) # SIDs
            show_submenu sids[@]
            read -p "-> " subchoice_sids
            case $subchoice_sids in
                0)
                    run_and_display "getsids"
                    ;;
                1)
                    run_and_display "getserviceids"
                    ;;
                2)
                    ;;
                *)
                    echo "Invalid option."
                    ;;
            esac
            ;;
        8) # Handles
            show_submenu handles[@]
            read -p "-> " subchoice_handles
            case $subchoice_handles in
                0)
                    run_and_display "handles"
                    ;;
                1)
                    ;;
                *)
                    echo "Invalid option."
                    ;;
            esac
            ;;
        9) # DLLs
            show_submenu dlls[@]
            read -p "-> " subchoice_dlls
            case $subchoice_dlls in
                0)
                    echo "Enter PID"
                    read pid
                    run_and_display "dlllist" "-p $pid"
                    ;;
                1)
                    mkdir -p ./dlldump
                    echo "Enter PID"
                    read pid
                    run_and_display "dlldump" "-D ./dlldump" "-p $pid"
                    ;;
                2)
                    ;;
                *)
                    echo "Invalid option."
                    ;;
            esac
            ;;
        10) # Strings per processes
            show_submenu strings_per_processes[@]
            read -p "-> " subchoice_strings_per_processes
            case $subchoice_strings_per_processes in
                0)
                    ;;
                1)
                    run_and_display "yarascan"
                    ;;
                2)
                    ;;
                *)
                    echo "Invalid option."
                    ;;
            esac
            ;;
        11) # user_assist
            show_submenu user_assist[@]
            read -p "-> " subchoice_user_assist
            case $subchoice_user_assist in
                0)
                    run_and_display "userassist"
                    ;;
                1)
                    ;;
                *)
                    echo "Invalid option."
                    ;;
            esac
            ;;
        12) # services
            show_submenu services[@]
            read -p "-> " subchoice_services
            case $subchoice_services in
                0)
                    run_and_display "svcscan"
                    ;;
                1)
                    run_and_display "getservicesids"
                    ;;
                2)
                    ;;
                *)
                    echo "Invalid option."
                    ;;
            esac
            ;;
        13) # network
            show_submenu network[@]
            read -p "-> " subchoice_network
            case $subchoice_network in
                0)
                    run_and_display "netscan"
                    ;;
                1)
                    run_and_display "connections"
                    ;;
                2)
                    run_and_display "connscan"
                    ;;
                3)
                    run_and_display "sockscan"
                    ;;
                4)
                    run_and_display "sockets"
                    ;;
                5)
                    run_and_display "linux_ifconfig"
                    ;;
                6)
                    run_and_display "linux_netstat"
                    ;;
                7)
                    run_and_display "linux_netfilter"
                    ;;
                8)
                    run_and_display "linux_arp"
                    ;;
                9)
                    run_and_display "linux_list_raw"
                    ;;
                10)
                    run_and_display "linux_route_cache"
                    ;;
                11)
                    ;;
                *)
                    echo "Invalid option."
                    ;;
            esac
            ;;
        14) # registry
            show_submenu registry[@]
            read -p "-> " subchoice_registry
            case $subchoice_registry in
                0)
                    run_and_display "hivelist"
                    ;;
                1)
                    run_and_display "printkey"
                    ;;
                2)
                    echo "Enter search term"
                    read search_term
                    run_and_display "printkey" "-K $search_term"
                    ;;
                3)
                    mkdir -p ./registry
                    echo "Enter hive offset"
                    read hive_offset
                    run_and_display "dumpregistry" "-H $hive_offset" "-D ./registry"
                    ;;
                4)
                    ;;
                *)
                    echo "Invalid option."
                    ;;
            esac
            ;;
        15) # filesystem
            show_submenu filesystem[@]
            read -p "-> " subchoice_filesystem
            case $subchoice_filesystem in
                0)
                    run_and_display "filescan"
                    ;;
                1)
                    run_and_display "mftparser"
                    ;;
                2)
                    mkdir -p ./dumpfiles
                    run_and_display "dumpfiles" "-D ./dumpfiles"
                    ;;
                3)
                    ;;
                *)
                    echo "Invalid option."
                    ;;
            esac
            ;;
        16) # SSL Keys/Certs
            show_submenu ssl_keys_certs[@]
            read -p "-> " subchoice_ssl_keys_certs
            case $subchoice_ssl_keys_certs in
                0)
                    run_and_display "dumpcerts"
                    ;;
                1)
                    ;;
                *)
                    echo "Invalid option."
                    ;;
            esac
            ;;
        17) # Malware
            show_submenu malware[@]
            read -p "-> " subchoice_malware
            case $subchoice_malware in
                0)
                    run_and_display "malfind"
                    ;;
                1)
                    run_and_display "apihooks"
                    ;;
                2)
                    run_and_display "driverirp"
                    ;;
                3)
                    run_and_display "ssdt"
                    ;;
                4)
                    run_and_display "linux_check_afinfo"
                    ;;
                5)
                    run_and_display "linux_check_creds"
                    ;;
                6)
                    run_and_display "linux_check_fop"
                    ;;
                7)
                    run_and_display "linux_check_idt"
                    ;;
                8)
                    run_and_display "linux_check_syscall"
                    ;;
                9)
                    run_and_display "linux_check_modules"
                    ;;
                10)
                    run_and_display "linux_check_tty"
                    ;;
                11)
                    run_and_display "linux_keyboard_notifiers"
                    ;;
                12)
                    ;;
                *)
                    echo "Invalid option."
                    ;;
            esac
            ;;
        18) # Scanning with yara
            show_submenu yara[@]
            read -p "-> " subchoice_yara
            case $subchoice_yara in
                0)
                    run_and_display "yarascan"
                    ;;
                1)
                    ;;
                *)
                    echo "Invalid option."
                    ;;
            esac
            ;;
        19) # Open Volatility Cheat-Sheet
            show_submenu cheat_sheet[@]
            read -p "-> " subchoice_cheat_sheet
            case $subchoice_cheat_sheet in
                0)
                    xdg-open $Cheat_Sheet
                    ;;
                1)
                    ;;
                *)
                    echo "Invalid option."
                    ;;
            esac
            ;;
        20) # Beenden
            exit 0
            ;;
    esac
}

# Main loop
while true; do
    main
done
