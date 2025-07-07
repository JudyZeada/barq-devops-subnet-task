# Network Analysis Report

## Analysis Questions and Answers

### 1. Which subnet has the most hosts?
The subnet mask that has the most hosts is the 255.255.252.0 (/22). Each subnet with this mask has 1022 hosts available.
**Aggregated by CIDR**: The /22 subnets collectively provide **8,176 total hosts**, making them the largest subnet group.

### 2. Are there any overlapping subnets? If yes, which ones?

**No overlapping subnets were found.** Each subnet has a unique network address and address range:

- **8 /22 subnets** - All have distinct network addresses
- **7 /23 subnets** - All have distinct network addresses  
- **10 /24 subnets** - All have distinct network addresses

### 3. What is the smallest and largest subnet in terms of address space?

**Largest Subnet:**
- **CIDR: /22** (subnet mask 255.255.252.0)
- **Address space: 1,024 total addresses** (1,022 usable hosts)
- **Host bits: 10 bits**

**Smallest Subnet:**
- **CIDR: /24** (subnet mask 255.255.255.0)
- **Address space: 256 total addresses** (254 usable hosts)
- **Host bits: 8 bits**

### 4. Suggest a subnetting strategy that could reduce wasted IPs in this network.

#### Current IP Allocation Analysis:
- **Total allocated IPs: 16,286 addresses**
- **8 × /22 subnets**: 8,176 addresses (1,022 usable each)
- **7 × /23 subnets**: 3,570 addresses (510 usable each)
- **10 × /24 subnets**: 2,540 addresses (254 usable each)

#### Optimization Strategies
- Start with a network audit to determine actual host counts
- Assess actual host requirements for each subnet
- Consider /25 (126 hosts), /26 (62 hosts), /27 (30 hosts) for smaller segments
- Group subnets by function
-  Use larger subnets for high-density areas
- Use smaller subnets for point-to-point links or small office branches



