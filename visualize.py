import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
def plot_individual_subnets(grouped_df, output_dir = 'output'):
    """Create bar chart showing hosts for each individual subnet"""
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Create figure
        plt.figure(figsize=(14, 8))
        
        # Create labels for each subnet (network address + CIDR)
        subnet_labels = [f"{row['network_address']} /{row['cidr']}" 
                        for _, row in grouped_df.iterrows()]
        
        # Get unique CIDR values and assign a color to each
        unique_cidrs = grouped_df['cidr'].unique()

        # Create color gradient
        colours = plt.cm.viridis(np.linspace(0, 0.5, len(unique_cidrs)))

        # Create a color dictionary mapping CIDR to color
        cidr_colour_map = {cidr: colours[i] for i, cidr in enumerate(unique_cidrs)}
        
        # Create bars with assigned colors
        bar_colours = [cidr_colour_map[cidr] for cidr in grouped_df['cidr']]
        
        # Create bars with custom style
        bars = plt.bar(subnet_labels, grouped_df['usable_hosts'],
                      color=bar_colours, width=0.8, edgecolor='black', linewidth=0.8)
        
        # Chart title and labels
        plt.title('Hosts per Individual Subnet\n', fontsize=14, pad=20)
        plt.xlabel('\nSubnet (Network Address/CIDR)', fontsize=12, labelpad=10)
        plt.ylabel('Number of Hosts', fontsize=12, labelpad=10)
        
        # Customize ticks
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        
        # Add grid and remove borders
        plt.grid(axis='y', alpha=0.2)
        for spine in ['top', 'right']:
            plt.gca().spines[spine].set_visible(False)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=9)
        
        # Add legend for CIDR colors
        legend_elements = [plt.Rectangle((0,0), 1, 1, color=cidr_colour_map[cidr], label=f'/{cidr}')
                         for cidr in unique_cidrs]
        plt.legend(handles=legend_elements, title='CIDR Notation', 
                  bbox_to_anchor=(1.1, 1), loc='upper left')
        
        plt.tight_layout()
        output_path = os.path.join(output_dir, 'individual_subnets.png')
        plt.savefig(output_path, dpi=120, bbox_inches='tight')
        print("\nIndividual subnets chart saved as 'individual_subnets.png'")
        plt.show()
        
    except Exception as e:
        print(f"Error creating individual subnets chart: {e}")

def plot_aggregated_cidr(grouped_df, output_dir = 'output'):
    """Create bar chart showing total hosts aggregated by CIDR"""
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Create figure
        plt.figure(figsize=(8, 6))
        
        # Group data by CIDR
        cidr_groups = grouped_df.groupby('cidr')['usable_hosts'].sum().reset_index()
        cidr_labels = [f"/{cidr}" for cidr in cidr_groups['cidr']]
        
        # Create color gradient
        colours = plt.cm.viridis(np.linspace(0, 0.5, len(cidr_labels)))
        
        # Create bars
        bars = plt.bar(cidr_labels, cidr_groups['usable_hosts'],
                      width=0.6, color=colours, edgecolor='black', linewidth=0.8)
        
        # Chart title and labels
        plt.title('Total Hosts by Subnet Mask (CIDR)\n', fontsize=14, pad=20)
        plt.xlabel('\nSubnet Mask', fontsize=12, labelpad=10)
        plt.ylabel('Total Hosts', fontsize=12, labelpad=10)
        
        # Customize ticks
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        
        # Add grid and remove borders
        plt.grid(axis='y', alpha=0.2)
        for spine in ['top', 'right']:
            plt.gca().spines[spine].set_visible(False)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        output_path = os.path.join(output_dir, 'aggregated_cidr.png')
        plt.savefig(output_path, dpi=120, bbox_inches='tight')
        print("\nAggregated CIDR chart saved as 'aggregated_cidr.png'")
        plt.show()
        
    except Exception as e:
        print(f"Error creating aggregated CIDR chart: {e}")

def plot_hosts_per_subnet(grouped_df, output_dir ='output'):
    """Wrapper function to create both charts"""
    plot_individual_subnets(grouped_df, output_dir)
    plot_aggregated_cidr(grouped_df, output_dir)