# BCI (Brain-Computer Interface) Project

A comprehensive brain-computer interface system for real-time EEG data acquisition, processing, and visualization. This project includes hardware integration, signal processing pipelines, and Kubernetes-based deployment infrastructure.

## 🧠 Overview

This BCI system is designed to:
- Acquire EEG signals from hardware devices (Arduino UNO R4)
- Stream data using Lab Streaming Layer (LSL) protocol
- Process and analyze neural signals in real-time
- Detect specific patterns like blinks and other features
- Visualize data through dashboards and live plots
- Deploy components in a containerized Kubernetes environment

## 🏗️ Architecture

The project consists of several key components:

### Data Acquisition
- **Arduino UNO R4 Integration**: Serial communication for EEG data capture
- **LSL Streaming**: Real-time data streaming using Lab Streaming Layer
- **Signal Simulation**: EEG simulation capabilities for testing

### Signal Processing
- **Blink Detection**: Real-time blink pattern recognition
- **Feature Extraction**: Advanced signal feature analysis
- **Data Pipeline**: Configurable signal processing workflows

### Visualization & Analysis
- **Live Plotting**: Real-time EEG signal visualization
- **Dashboard**: Web-based monitoring interface
- **Memory Analysis**: Performance and memory usage tools

### Deployment Infrastructure
- **Kubernetes Deployments**: Container orchestration for scalable deployment
- **Custom Resource Definitions (CRDs)**: Domain-specific Kubernetes resources
- **Data Policies**: Governance and compliance configurations

## 📁 Project Structure

```
BCI/
├── bci-deployments/          # Kubernetes deployment configurations
│   ├── core-deployment.yaml  # Main BCI application deployment
│   ├── blink-detector.yaml   # Blink detection service
│   ├── signal-pipeline.yaml  # Signal processing pipeline
│   ├── alpha-dashboard*.yaml # Dashboard deployments
│   ├── lsl-*.yaml            # LSL streaming services
│   ├── lsl_live_plot.py      # Real-time EEG visualization
│   └── uno_r4_serial_to_lsl.py # Arduino serial to LSL bridge
├── memory-analyzer/          # Performance analysis tools
│   ├── SizeOfMemory.c        # Memory usage analyzer
│   └── SizeOfMemory          # Compiled analyzer
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Kubernetes cluster
- Arduino UNO R4 (for hardware integration)
- Required Python packages:
  ```bash
  pip install pylsl numpy matplotlib serial
  ```

### Hardware Setup
1. Connect your EEG acquisition hardware to Arduino UNO R4
2. Upload the appropriate firmware for EEG data collection
3. Connect Arduino to your computer via USB

### Data Streaming
1. **Start LSL Stream from Arduino:**
   ```bash
   python bci-deployments/uno_r4_serial_to_lsl.py
   ```

2. **Launch Live Visualization:**
   ```bash
   python bci-deployments/lsl_live_plot.py
   ```

### Kubernetes Deployment
1. **Deploy Core Infrastructure:**
   ```bash
   kubectl apply -f bci-deployments/crds.yaml
   kubectl apply -f bci-deployments/core-deployment.yaml
   ```

2. **Deploy Signal Processing Pipeline:**
   ```bash
   kubectl apply -f bci-deployments/signal-pipeline.yaml
   kubectl apply -f bci-deployments/blink-detector.yaml
   ```

3. **Launch Dashboard:**
   ```bash
   kubectl apply -f bci-deployments/alpha-dashboard.yaml
   ```

## 🔧 Configuration

### EEG Stream Parameters
- **Stream Name**: `EEG_SIM` (configurable in Python scripts)
- **Channels**: 6 channels by default
- **Sample Rate**: 500 Hz
- **Data Format**: 16-bit signed integers

### Hardware Configuration
- **Serial Port**: `/dev/ttyACM0` (adjust for your system)
- **Baud Rate**: 230400
- **Packet Format**: Custom protocol with sync bytes

### Visualization Settings
- **Window Duration**: 5 seconds (configurable)
- **Plot Channels**: [0, 1, 2] (first 3 channels)
- **Real-time Updates**: Using matplotlib animation

## 🧪 Features

### Real-time Processing
- **Live EEG Streaming**: Continuous data acquisition from hardware
- **Blink Detection**: Automated detection of eye blinks in EEG signals
- **Alpha Wave Analysis**: Detection and analysis of alpha brain waves
- **Feature Extraction**: Advanced signal processing for pattern recognition

### Monitoring & Analysis
- **Performance Monitoring**: Memory usage and system performance analysis
- **Data Quality Assessment**: Signal quality metrics and validation
- **Session Management**: Organized data collection sessions

### Deployment & Scaling
- **Container Orchestration**: Kubernetes-based deployment for scalability
- **Real-time Priority**: High-priority scheduling for time-sensitive processing
- **Multi-node Support**: Distributed processing capabilities

## 🛠️ Development

### Adding New Features
1. Create feature detection algorithms in the signal processing pipeline
2. Add corresponding Kubernetes deployments in `bci-deployments/`
3. Update dashboard configurations for new visualizations

### Memory Optimization
Use the memory analyzer to profile your applications:
```bash
cd memory-analyzer
./SizeOfMemory
```

### Testing with Simulation
For development without hardware:
1. Use the LSL simulator configurations
2. Modify stream names from hardware streams to `EEG_SIM`
3. Test with synthetic EEG data

## 📊 Performance

- **Real-time Processing**: Sub-millisecond latency for critical features
- **Scalability**: Kubernetes-based horizontal scaling
- **Memory Efficiency**: Optimized for continuous data streaming
- **High Throughput**: Supports multiple concurrent EEG streams

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes with appropriate tests
4. Update documentation as needed
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Related Technologies

- **Lab Streaming Layer (LSL)**: Real-time data streaming protocol
- **Kubernetes**: Container orchestration platform
- **NumPy & Matplotlib**: Scientific computing and visualization
- **Arduino**: Hardware integration platform

## 📞 Support

For questions, issues, or contributions, please open an issue in the GitHub repository or contact the development team.

---

*Last updated: January 2026*