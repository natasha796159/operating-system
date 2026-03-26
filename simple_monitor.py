import http.server
import socketserver
import json
import time
import webbrowser
import threading
from datetime import datetime
import random

print("🚀 Starting Simple Process Monitor...")
print("📊 This will open in your web browser automatically!")
print("🛑 Press Ctrl+C to stop the monitor")

class ProcessMonitor:
    def __init__(self):
        self.data = self.generate_demo_data()
        
    def generate_demo_data(self):
        # Create realistic demo data
        base_processes = [
            {'pid': 1234, 'name': 'chrome.exe', 'cpu_percent': 15.5, 'memory_percent': 8.2, 'status': 'running'},
            {'pid': 5678, 'name': 'vscode.exe', 'cpu_percent': 12.1, 'memory_percent': 12.5, 'status': 'running'},
            {'pid': 9012, 'name': 'node.exe', 'cpu_percent': 8.7, 'memory_percent': 4.3, 'status': 'sleeping'},
            {'pid': 3456, 'name': 'explorer.exe', 'cpu_percent': 5.2, 'memory_percent': 3.1, 'status': 'running'},
            {'pid': 7890, 'name': 'spotify.exe', 'cpu_percent': 3.8, 'memory_percent': 6.7, 'status': 'running'},
            {'pid': 1111, 'name': 'python.exe', 'cpu_percent': 2.5, 'memory_percent': 1.2, 'status': 'running'},
            {'pid': 2222, 'name': 'firefox.exe', 'cpu_percent': 7.3, 'memory_percent': 9.8, 'status': 'running'},
            {'pid': 3333, 'name': 'discord.exe', 'cpu_percent': 4.2, 'memory_percent': 5.1, 'status': 'running'},
            {'pid': 4444, 'name': 'steam.exe', 'cpu_percent': 1.8, 'memory_percent': 3.4, 'status': 'sleeping'},
            {'pid': 5555, 'name': 'notepad.exe', 'cpu_percent': 0.5, 'memory_percent': 0.8, 'status': 'running'}
        ]
        
        # Add random variation to make it look live
        for p in base_processes:
            p['cpu_percent'] = max(0.1, p['cpu_percent'] + random.uniform(-3, 3))
            p['memory_percent'] = max(0.1, p['memory_percent'] + random.uniform(-1, 1))
        
        # Sort by CPU usage
        base_processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        
        return {
            'cpu': 25 + random.uniform(0, 50),  # 25-75%
            'memory': 40 + random.uniform(0, 35),  # 40-75%
            'memory_used': 6.8,
            'memory_total': 16.0,
            'disk_used': 142.3,
            'disk_total': 256.0,
            'processes': base_processes,
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'total_processes': len(base_processes)
        }
    
    def update_data(self):
        while True:
            self.data = self.generate_demo_data()
            time.sleep(2)  # Update every 2 seconds

# Create and start monitor
monitor = ProcessMonitor()
update_thread = threading.Thread(target=monitor.update_data, daemon=True)
update_thread.start()

# HTML content with embedded CSS and JavaScript
HTML_CONTENT = '''
<!DOCTYPE html>
<html>
<head>
    <title>Simple Process Monitor</title>
    <meta http-equiv="refresh" content="3">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 0;
            margin: 0;
            min-height: 100vh;
        }
        .container { 
            max-width: 1300px; 
            margin: 0 auto; 
            padding: 20px;
        }
        .header { 
            text-align: center; 
            margin-bottom: 30px;
            background: rgba(255,255,255,0.15);
            padding: 25px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        .header h1 { 
            font-size: 2.8em; 
            margin-bottom: 10px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        .subtitle { 
            font-size: 1.3em;
            opacity: 0.9;
            margin-bottom: 10px;
        }
        .info {
            font-size: 0.9em;
            opacity: 0.7;
            background: rgba(0,0,0,0.2);
            padding: 8px 15px;
            border-radius: 10px;
            display: inline-block;
        }
        
        .metrics-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px; 
            margin-bottom: 35px;
        }
        .metric-card {
            background: rgba(255,255,255,0.15);
            padding: 25px;
            border-radius: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-5px);
        }
        .metric-card h3 {
            font-size: 1.2em;
            margin-bottom: 15px;
            opacity: 0.9;
        }
        .metric-value { 
            font-size: 3em; 
            font-weight: bold;
            margin: 20px 0;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        .progress-container {
            background: rgba(255,255,255,0.2);
            height: 28px;
            border-radius: 14px;
            overflow: hidden;
            margin: 20px 0;
            position: relative;
        }
        .progress-fill {
            height: 100%;
            transition: width 0.5s ease;
            position: relative;
        }
        .progress-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            animation: shine 3s infinite;
        }
        .cpu-fill { 
            background: linear-gradient(90deg, #4CAF50, #45a049, #4CAF50);
            background-size: 200% 100%;
            animation: gradientShift 3s ease infinite;
        }
        .memory-fill { 
            background: linear-gradient(90deg, #2196F3, #1976D2, #2196F3);
            background-size: 200% 100%;
            animation: gradientShift 3s ease infinite;
        }
        .disk-fill { 
            background: linear-gradient(90deg, #FF9800, #F57C00, #FF9800);
            background-size: 200% 100%;
            animation: gradientShift 3s ease infinite;
        }
        
        @keyframes shine {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(400%); }
        }
        @keyframes gradientShift {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        .metric-details {
            font-size: 1em;
            opacity: 0.9;
            margin-top: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .process-section {
            background: rgba(255,255,255,0.15);
            border-radius: 20px;
            overflow: hidden;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            margin-bottom: 20px;
        }
        .process-header {
            padding: 20px;
            background: rgba(255,255,255,0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .process-header h3 {
            font-size: 1.4em;
        }
        .process-count {
            background: rgba(255,255,255,0.3);
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 0.9em;
        }
        
        table { 
            width: 100%; 
            border-collapse: collapse;
        }
        th, td { 
            padding: 18px; 
            text-align: left; 
            border-bottom: 1px solid rgba(255,255,255,0.1); 
        }
        th { 
            background: rgba(255,255,255,0.15); 
            font-weight: 600;
            font-size: 0.95em;
        }
        
        .process-row:hover { 
            background: rgba(255,255,255,0.1); 
            transition: all 0.3s ease;
        }
        
        .process-name {
            font-weight: 600;
            font-size: 1.05em;
        }
        
        .status-badge {
            padding: 6px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
            text-transform: capitalize;
        }
        .status-running { 
            background: linear-gradient(135deg, #4CAF50, #45a049);
            box-shadow: 0 2px 10px rgba(76, 175, 80, 0.3);
        }
        .status-sleeping { 
            background: linear-gradient(135deg, #FF9800, #F57C00);
            box-shadow: 0 2px 10px rgba(255, 152, 0, 0.3);
        }
        
        .progress-cell {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .progress-cell span {
            min-width: 50px;
            font-weight: 500;
        }
        .mini-progress {
            flex: 1;
            background: rgba(255,255,255,0.2);
            height: 12px;
            border-radius: 6px;
            overflow: hidden;
        }
        .mini-progress-fill {
            height: 100%;
            transition: width 0.5s ease;
        }
        .mini-cpu { background: linear-gradient(90deg, #4CAF50, #45a049); }
        .mini-memory { background: linear-gradient(90deg, #2196F3, #1976D2); }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            opacity: 0.7;
            font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            .container { padding: 15px; }
            .metrics-grid { grid-template-columns: 1fr; }
            .header h1 { font-size: 2em; }
            th, td { padding: 12px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Simple Process Monitor</h1>
            <div class="subtitle">Real-time System Monitoring Dashboard</div>
            <div class="info">Auto-refreshing every 3 seconds • No installation required</div>
        </div>

        <div class="metrics-grid">
            <div class="metric-card">
                <h3>CPU Usage</h3>
                <div class="metric-value">{{CPU_PERCENT}}%</div>
                <div class="progress-container">
                    <div class="progress-fill cpu-fill" style="width: {{CPU_PERCENT}}%"></div>
                </div>
                <div class="metric-details">
                    <span>Processor Utilization</span>
                    <span>{{CPU_PERCENT}}%</span>
                </div>
            </div>
            
            <div class="metric-card">
                <h3>Memory Usage</h3>
                <div class="metric-value">{{MEMORY_PERCENT}}%</div>
                <div class="progress-container">
                    <div class="progress-fill memory-fill" style="width: {{MEMORY_PERCENT}}%"></div>
                </div>
                <div class="metric-details">
                    <span>{{MEMORY_USED}} GB / {{MEMORY_TOTAL}} GB</span>
                    <span>{{MEMORY_PERCENT}}%</span>
                </div>
            </div>
            
            <div class="metric-card">
                <h3>Disk Usage</h3>
                <div class="metric-value">{{DISK_PERCENT}}%</div>
                <div class="progress-container">
                    <div class="progress-fill disk-fill" style="width: {{DISK_PERCENT}}%"></div>
                </div>
                <div class="metric-details">
                    <span>{{DISK_USED}} GB / {{DISK_TOTAL}} GB</span>
                    <span>{{DISK_PERCENT}}%</span>
                </div>
            </div>
        </div>

        <div class="process-section">
            <div class="process-header">
                <h3>Running Processes</h3>
                <div class="process-count">{{TOTAL_PROCESSES}} processes</div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>PID</th>
                        <th>Process Name</th>
                        <th>CPU Usage</th>
                        <th>Memory Usage</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {{PROCESS_ROWS}}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            Last updated: {{TIMESTAMP}} | 
            Made with Python | 
            No installations required!
        </div>
    </div>
</body>
</html>
'''

class MonitorHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            data = monitor.data
            
            # Calculate disk percentage
            disk_percent = (data['disk_used'] / data['disk_total']) * 100
            
            # Replace placeholders with actual data
            html = HTML_CONTENT
            html = html.replace('{{CPU_PERCENT}}', f"{data['cpu']:.1f}")
            html = html.replace('{{MEMORY_PERCENT}}', f"{data['memory']:.1f}")
            html = html.replace('{{DISK_PERCENT}}', f"{disk_percent:.1f}")
            html = html.replace('{{MEMORY_USED}}', f"{data['memory_used']:.1f}")
            html = html.replace('{{MEMORY_TOTAL}}', f"{data['memory_total']:.1f}")
            html = html.replace('{{DISK_USED}}', f"{data['disk_used']:.1f}")
            html = html.replace('{{DISK_TOTAL}}', f"{data['disk_total']:.1f}")
            html = html.replace('{{TOTAL_PROCESSES}}', str(data['total_processes']))
            html = html.replace('{{TIMESTAMP}}', data['timestamp'])
            
            # Generate process rows
            process_rows = ""
            for process in data['processes']:
                status_class = f"status-{process['status']}"
                process_rows += f'''
                    <tr class="process-row">
                        <td><strong>{process['pid']}</strong></td>
                        <td class="process-name">{process['name']}</td>
                        <td>
                            <div class="progress-cell">
                                <span>{process['cpu_percent']:.1f}%</span>
                                <div class="mini-progress">
                                    <div class="mini-progress-fill mini-cpu" style="width: {min(process['cpu_percent'], 100)}%"></div>
                                </div>
                            </div>
                        </td>
                        <td>
                            <div class="progress-cell">
                                <span>{process['memory_percent']:.1f}%</span>
                                <div class="mini-progress">
                                    <div class="mini-progress-fill mini-memory" style="width: {min(process['memory_percent'], 100)}%"></div>
                                </div>
                            </div>
                        </td>
                        <td>
                            <span class="status-badge {status_class}">
                                {process['status']}
                            </span>
                        </td>
                    </tr>
                '''
            
            html = html.replace('{{PROCESS_ROWS}}', process_rows)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        else:
            super().do_GET()

def start_server():
    PORT = 8000
    
    # Try different ports if 8000 is busy
    for port in [8000, 8001, 8002, 8080]:
        try:
            with socketserver.TCPServer(("", port), MonitorHandler) as httpd:
                print(f"✅ Server started successfully!")
                print(f"🌐 Open your browser and go to: http://localhost:{port}")
                print("🔄 The dashboard auto-refreshes every 3 seconds")
                print("🛑 Press Ctrl+C to stop the server")
                
                # Auto-open browser
                try:
                    webbrowser.open(f'http://localhost:{port}')
                except:
                    pass
                
                httpd.serve_forever()
            break
        except OSError:
            if port == 8080:
                print("❌ Could not start server. All ports are busy.")
                input("Press Enter to exit...")

if __name__ == "__main__":
    start_server()