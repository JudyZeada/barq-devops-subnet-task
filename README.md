# Subnet Analysis and Visualization Tool

## Features
- **IP Subnet Analysis**: Calculates CIDR notation, network addresses, broadcast addresses, and usable hosts
- **Data Processing**: Reads IP data from Excel files and processes subnet information
- **Report Generation**: Exports detailed CSV reports and summaries
- **Visualization**: Creates bar charts showing host distribution across subnets
- **Dockerized**: Fully containerized solution for easy deployment

## Prerequisites
### Local Development
- Python 3.8+
- pip package manager

### Docker Deployment
- Docker Engine

## Installation & Usage

### Option 1: Local Development

1. **Clone the repository:**
   ```bash
   git clone <https://github.com/JudyZeada/barq-devops-subnet-task.git>
   cd barq-devops-subnet-task
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare input data:**
   - Place your Excel file as `ip_data.xlsx` in the project root
   - Ensure the Excel file has IP addresses in column A and subnet masks in column B

4. **Run the analysis:**
   ```bash
   python subnet_analyzer.py
   ```

### Option 2: Docker Deployment

1. **Build the Docker image:**
   ```bash
   docker build -t subnet-analyzer .
   ```

2. **Run the container:**
   ```bash
   docker run subnet-analyzer
   ```

   Or on Windows:
   ```bash
   docker run subnet-analyzer
   ```
