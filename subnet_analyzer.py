import pandas as pd
import os
import matplotlib.pyplot as plt
import json
import numpy as np
from visualize import plot_hosts_per_subnet

def read_ip_data(filename):
    """
    Reads IP addresses and subnet masks from an Excel file.
    """
    try:
        ip_addresses = []
        subnet_masks = []
        file = pd.read_excel(filename)
        
        # Process each row in the Excel file
        for index, row in file.iterrows(): 
            ip_address = str(row.iloc[0]).strip()
            subnet_mask = str(row.iloc[1]).strip()

            # Skip rows with invalid data
            if ip_address != 'nan' and subnet_mask != 'nan':
                ip_addresses.append(ip_address)
                subnet_masks.append(subnet_mask)  
            else:
                print(f"Row {index + 1}: Skipped invalid data")
        return ip_addresses, subnet_masks
    
    except PermissionError:
        print(f"Error: Permission denied for file '{filename}'. Close it or check permissions.")
        return [], []
    except Exception as e:
        print(f"Error reading file: {e}")
        return [], []

def process_ip_data(ip_addresses, subnet_masks):
    """
    Process IP data from Excel file and return a DataFrame with calculated network information
    and grouped data by subnet.
    """
    try:
        # Initialize lists for calculated values
        results = {
            'ip_address': [],
            'subnet_mask': [],
            'cidr': [],
            'network_address': [],
            'broadcast_address': [],
            'usable_hosts': []
        }
        
        # Process each row
        for ip_string, subnet_string in zip(ip_addresses, subnet_masks):
            ip_string = str(ip_string).strip()
            subnet_string = str(subnet_string).strip()
            
            # Skip invalid entries
            if ip_string == 'nan' or subnet_string == 'nan':
                print(f"Skipped invalid data")
                continue
            
            try:
                # Calculate network information
                subnet_octets = subnet_string.split('.')
                subnet_binary = ''.join([f'{int(octet):08b}' for octet in subnet_octets])
                ip_octets = ip_string.split('.')
                ip_binary = ''.join([f'{int(octet):08b}' for octet in ip_octets])
                
                # Calculate host bits and CIDR
                host_bits = subnet_binary.count('0')
                cidr = 32 - host_bits
                
                # Calculate network and broadcast addresses
                network_binary = ip_binary[:-host_bits] + '0' * host_bits
                broadcast_binary = ip_binary[:-host_bits] + '1' * host_bits
                
                def binary_to_ip(binary_str):
                    return '.'.join([str(int(binary_str[i:i+8], 2)) for i in range(0, 32, 8)])
                
                network_address = binary_to_ip(network_binary)
                broadcast_address = binary_to_ip(broadcast_binary)
                usable_hosts = (2 ** host_bits) - 2
                
                # Store results
                results['ip_address'].append(ip_string)
                results['subnet_mask'].append(subnet_string)
                results['cidr'].append(cidr)
                results['network_address'].append(network_address)
                results['broadcast_address'].append(broadcast_address)
                results['usable_hosts'].append(usable_hosts)
                
            except ValueError as e:
                print(f"Error processing {ip_string}/{subnet_string}: {e}")
                continue
                
        # Create DataFrame from results
        result_file = pd.DataFrame(results)
        
        # Group by subnet (CIDR + network address)
        grouped = result_file.groupby(['cidr', 'network_address']).agg({
            'subnet_mask': 'first',
            'broadcast_address': 'first',
            'usable_hosts': 'first',
            'ip_address': list
        }).reset_index()
        
        return result_file, grouped
    
    except Exception as e:
        print(f"Error processing IP data: {e}")
        return pd.DataFrame(), pd.DataFrame()

def export_reports(result_df, grouped_df,output_dir='output'):
    """
    Export reports in CSV and JSON formats.
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Export detailed results
        network_details_path = os.path.join(output_dir, 'ip_network_details.csv')
        result_df.to_csv(network_details_path, index=False)
        print("Detailed report saved as '{network_details_path}'")
        
        # Export grouped results
        summary_csv_path = os.path.join(output_dir,'subnet_summarry.csv')
        grouped_df.to_csv(summary_csv_path, index=False)
        print("Subnet summary saved as '{summary_csv_path}'")
        
    except Exception as e:
        print(f"Error exporting reports: {e}")
        

def main():
    """
    Main function to execute the IP data processing workflow.
    """
    filename = "ip_data.xlsx"
    
    # Check if file exists
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found!")
        return
    
    # Read IP data from file
    ip_addresses, subnet_masks = read_ip_data(filename)

    # Process the IP data
    result_df, grouped_df = process_ip_data(ip_addresses, subnet_masks)
    
    if result_df is None or grouped_df is None:
        print()
        return(f"Error: File empty")
    
    # Print summary information
    print("\nSubnet Summary:")
    print(grouped_df[['cidr', 'subnet_mask', 'network_address', 
                     'broadcast_address', 'usable_hosts']].to_string(index=False))
    
    # Export reports
    export_reports(result_df, grouped_df)
    
    # Create visualization
    plot_hosts_per_subnet(grouped_df)

if __name__ == "__main__":
    main()