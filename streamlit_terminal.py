"""
AI Python Terminal - Streamlit Web Application
A simplified version for easy deployment on Streamlit Cloud
"""
import os
import sys
import json
import time
import shlex
import subprocess
from datetime import datetime
from typing import Dict, List, Optional

import streamlit as st
import psutil

# Configure Streamlit page with enhanced settings
st.set_page_config(
    page_title="AI Python Terminal",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com',
        'Report a bug': 'https://github.com',
        'About': "AI Python Terminal - Modern web-based command interface"
    }
)

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

# Modern light theme CSS with enhanced responsiveness
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Global styles and CSS variables */
    :root {
        --primary-color: #2563eb;
        --primary-light: #3b82f6;
        --primary-dark: #1d4ed8;
        --secondary-color: #64748b;
        --success-color: #059669;
        --warning-color: #d97706;
        --error-color: #dc2626;
        --background-primary: #ffffff;
        --background-secondary: #f8fafc;
        --background-tertiary: #f1f5f9;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --text-muted: #94a3b8;
        --border-color: #e2e8f0;
        --border-light: #f1f5f9;
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
        --radius-sm: 0.375rem;
        --radius-md: 0.5rem;
        --radius-lg: 0.75rem;
        --radius-xl: 1rem;
    }
    
    /* Reset and base styles */
    .main .block-container {
        padding: 2rem 1rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Hide default Streamlit elements */
    .stDeployButton { display: none; }
    header[data-testid="stHeader"] { display: none; }
    .stMainBlockContainer { padding-top: 1rem; }
    
    /* Main header component */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: var(--radius-xl);
        text-align: center;
        box-shadow: var(--shadow-xl);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
        opacity: 0.3;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: clamp(2rem, 5vw, 3.5rem);
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        margin: 1rem 0 0 0;
        font-size: clamp(1rem, 3vw, 1.25rem);
        opacity: 0.9;
        position: relative;
        z-index: 1;
        font-weight: 300;
    }
    
    /* Terminal output container */
    .terminal-container {
        background: var(--background-primary);
        border-radius: var(--radius-xl);
        box-shadow: var(--shadow-lg);
        border: 1px solid var(--border-color);
        overflow: hidden;
        margin: 2rem 0;
    }
    
    .terminal-header {
        background: linear-gradient(135deg, var(--background-secondary) 0%, var(--background-tertiary) 100%);
        padding: 1rem 1.5rem;
        border-bottom: 1px solid var(--border-color);
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .terminal-controls {
        display: flex;
        gap: 0.5rem;
    }
    
    .terminal-control {
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }
    
    .control-close { background: #ff5f57; }
    .control-minimize { background: #ffbd2e; }
    .control-maximize { background: #28ca42; }
    
    .terminal-title {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: var(--text-primary);
        font-size: 0.875rem;
    }
    
    .terminal-output {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: #e2e8f0;
        font-family: 'JetBrains Mono', 'Monaco', 'Menlo', monospace;
        padding: 2rem;
        height: 500px;
        overflow-y: auto;
        white-space: pre-wrap;
        font-size: 14px;
        line-height: 1.6;
        position: relative;
    }
    
    /* Command input section */
    .command-section {
        background: var(--background-primary);
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
        margin: 1.5rem 0;
    }
    
    .command-label {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: var(--text-primary);
        font-size: 1.125rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Enhanced input styling */
    .stTextInput > div > div > input {
        background: var(--background-secondary);
        border: 2px solid var(--border-color);
        border-radius: var(--radius-md);
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        padding: 0.875rem 1rem;
        color: var(--text-primary);
        transition: all 0.2s ease;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        outline: none;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--text-muted);
        font-style: italic;
    }
    
    /* Button enhancements */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
        color: white;
        border: none;
        border-radius: var(--radius-md);
        font-weight: 600;
        padding: 0.875rem 2rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        transition: all 0.2s ease;
        box-shadow: var(--shadow-md);
        cursor: pointer;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-color) 100%);
        transform: translateY(-1px);
        box-shadow: var(--shadow-lg);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: var(--shadow-sm);
    }
    
    /* Directory display */
    .directory-display {
        background: linear-gradient(135deg, var(--background-secondary) 0%, var(--background-tertiary) 100%);
        padding: 1.25rem 1.5rem;
        border-radius: var(--radius-lg);
        border: 1px solid var(--border-color);
        margin: 1.5rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
        box-shadow: var(--shadow-sm);
    }
    
    .directory-icon {
        font-size: 1.5rem;
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
    }
    
    .directory-label {
        color: var(--primary-color);
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
    }
    
    .directory-path {
        background: var(--background-primary);
        color: var(--success-color);
        padding: 0.5rem 1rem;
        border-radius: var(--radius-sm);
        font-family: 'JetBrains Mono', monospace;
        font-weight: 500;
        font-size: 0.875rem;
        border: 1px solid var(--border-light);
        box-shadow: var(--shadow-sm);
    }
    
    /* Sidebar enhancements */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--background-primary) 0%, var(--background-secondary) 100%);
        border-right: 1px solid var(--border-color);
    }
    
    .sidebar-section {
        background: var(--background-primary);
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: var(--radius-lg);
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
    }
    
    .sidebar-header {
        color: var(--primary-color);
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.25rem;
        text-align: center;
        margin-bottom: 1rem;
        padding: 1rem;
        background: linear-gradient(135deg, var(--background-secondary) 0%, var(--background-tertiary) 100%);
        border-radius: var(--radius-md);
        border: 1px solid var(--border-light);
    }
    
    /* System metrics cards */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: var(--background-primary);
        padding: 2rem 1.5rem;
        border-radius: var(--radius-lg);
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-md);
        text-align: center;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color), var(--primary-light));
        opacity: 0.8;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.875rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-detail {
        color: var(--text-muted);
        font-size: 0.75rem;
        margin-top: 0.25rem;
    }
    
    /* Color utilities */
    .text-success { color: var(--success-color); }
    .text-warning { color: var(--warning-color); }
    .text-error { color: var(--error-color); }
    .text-primary { color: var(--primary-color); }
    .text-secondary { color: var(--text-secondary); }
    
    /* Terminal content styling */
    .terminal-prompt {
        color: #10b981;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
    }
    
    .terminal-command {
        color: #e2e8f0;
        font-weight: 500;
    }
    
    .terminal-output-text {
        color: #3b82f6;
        margin-left: 1rem;
    }
    
    .terminal-error-text {
        color: #ef4444;
        font-weight: 500;
        margin-left: 1rem;
    }
    
    .terminal-timestamp {
        color: #64748b;
        font-size: 0.75rem;
        margin-left: 1.5rem;
        opacity: 0.7;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: var(--text-muted);
        font-size: 0.875rem;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid var(--border-color);
        background: var(--background-secondary);
        border-radius: var(--radius-lg);
        font-family: 'Inter', sans-serif;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem 0.5rem;
        }
        
        .main-header {
            padding: 2rem 1rem;
        }
        
        .terminal-output {
            height: 350px;
            padding: 1rem;
            font-size: 12px;
        }
        
        .metrics-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .metric-card {
            padding: 1.5rem 1rem;
        }
        
        .command-section {
            padding: 1rem;
        }
        
        .directory-display {
            padding: 1rem;
            flex-direction: column;
            align-items: flex-start;
            gap: 0.75rem;
        }
    }
    
    @media (max-width: 480px) {
        .main-header h1 {
            font-size: 1.75rem;
        }
        
        .main-header p {
            font-size: 0.875rem;
        }
        
        .terminal-output {
            height: 300px;
            font-size: 11px;
        }
        
        .metric-icon {
            font-size: 2rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
    }
    
    /* Scrollbar styling */
    .terminal-output::-webkit-scrollbar {
        width: 8px;
    }
    
    .terminal-output::-webkit-scrollbar-track {
        background: #1e293b;
        border-radius: 4px;
    }
    
    .terminal-output::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 4px;
    }
    
    .terminal-output::-webkit-scrollbar-thumb:hover {
        background: #64748b;
    }
    
    /* Animation keyframes */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.3s ease-out;
    }
    
    .blinking-cursor {
        animation: blink 1s infinite;
        color: #10b981;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'command_history' not in st.session_state:
    st.session_state.command_history = []
if 'output_history' not in st.session_state:
    st.session_state.output_history = []
if 'current_directory' not in st.session_state:
    st.session_state.current_directory = os.getcwd()
if 'ai_enabled' not in st.session_state:
    st.session_state.ai_enabled = True
if 'available_directories' not in st.session_state:
    st.session_state.available_directories = []

# Gemini API configuration
GEMINI_API_KEY = "AIzaSyBM7VpSZ8MtAkX53h3KbDcAZtj_w0-U5i0"
GEMINI_PROJECT_NUMBER = "866760035068"

def get_available_directories(base_path=None):
    """Get list of available directories for selection"""
    if base_path is None:
        base_path = os.getcwd()
    
    directories = []
    
    # Add common system directories
    common_dirs = [
        os.path.expanduser("~"),  # Home directory
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Downloads"),
        "C:\\" if os.name == 'nt' else "/",  # Root directory
        base_path,  # Current directory
    ]
    
    for dir_path in common_dirs:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            directories.append(dir_path)
    
    # Add subdirectories of current directory
    try:
        for item in os.listdir(base_path):
            item_path = os.path.join(base_path, item)
            if os.path.isdir(item_path) and not item.startswith('.'):
                directories.append(item_path)
    except PermissionError:
        pass
    
    # Remove duplicates and sort
    directories = list(set(directories))
    directories.sort()
    
    return directories

def format_directory_name(dir_path):
    """Format directory name for display"""
    if dir_path == os.path.expanduser("~"):
        return "🏠 Home Directory"
    elif dir_path == os.path.expanduser("~/Desktop"):
        return "🖥️ Desktop"
    elif dir_path == os.path.expanduser("~/Documents"):
        return "📄 Documents"
    elif dir_path == os.path.expanduser("~/Downloads"):
        return "📥 Downloads"
    elif dir_path == "C:\\" or dir_path == "/":
        return "💿 Root Directory"
    else:
        return f"📁 {os.path.basename(dir_path) or dir_path}"

class SimpleTerminal:
    """Simplified terminal for Streamlit"""
    
    def __init__(self):
        # Always use the session state directory
        self.current_dir = st.session_state.current_directory
    
    def update_current_dir(self):
        """Update current directory from session state"""
        self.current_dir = st.session_state.current_directory
    
    def execute_command(self, command: str) -> Dict:
        """Execute a command and return result"""
        # Update current directory from session state
        self.update_current_dir()
        
        if not command.strip():
            return {"output": "", "error": "", "exit_code": 0}
        
        # Handle built-in commands
        parts = shlex.split(command)
        cmd = parts[0].lower()
        
        try:
            if cmd == 'pwd':
                return {"output": self.current_dir, "error": "", "exit_code": 0}
            
            elif cmd == 'cd':
                if len(parts) > 1:
                    new_dir = parts[1]
                    if new_dir == '..':
                        new_dir = os.path.dirname(self.current_dir)
                    elif new_dir == '~':
                        new_dir = os.path.expanduser("~")
                    elif not os.path.isabs(new_dir):
                        new_dir = os.path.join(self.current_dir, new_dir)
                    
                    if os.path.exists(new_dir) and os.path.isdir(new_dir):
                        self.current_dir = os.path.abspath(new_dir)
                        # Update session state
                        st.session_state.current_directory = self.current_dir
                        return {"output": f"Changed to {self.current_dir}", "error": "", "exit_code": 0}
                    else:
                        return {"output": "", "error": f"Directory not found: {new_dir}", "exit_code": 1}
                else:
                    return {"output": self.current_dir, "error": "", "exit_code": 0}
            
            elif cmd == 'ls' or cmd == 'dir':
                try:
                    items = []
                    for item in sorted(os.listdir(self.current_dir)):
                        path = os.path.join(self.current_dir, item)
                        if os.path.isdir(path):
                            items.append(f"📁 {item}/")
                        else:
                            items.append(f"📄 {item}")
                    return {"output": "\n".join(items), "error": "", "exit_code": 0}
                except PermissionError:
                    return {"output": "", "error": "Permission denied", "exit_code": 1}
            
            elif cmd == 'mkdir':
                if len(parts) > 1:
                    dir_name = parts[1]
                    dir_path = os.path.join(self.current_dir, dir_name)
                    try:
                        os.makedirs(dir_path, exist_ok=True)
                        return {"output": f"Directory created: {dir_name}", "error": "", "exit_code": 0}
                    except Exception as e:
                        return {"output": "", "error": str(e), "exit_code": 1}
                else:
                    return {"output": "", "error": "Usage: mkdir <directory_name>", "exit_code": 1}
            
            elif cmd == 'ps':
                try:
                    processes = []
                    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                        try:
                            info = proc.info
                            processes.append(f"{info['pid']:<8} {info['name']:<20} {info['cpu_percent']:.1f}%")
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                    
                    if processes:
                        header = f"{'PID':<8} {'NAME':<20} {'CPU%'}"
                        return {"output": header + "\n" + "-"*40 + "\n" + "\n".join(processes[:20]), "error": "", "exit_code": 0}
                    else:
                        return {"output": "No processes found", "error": "", "exit_code": 0}
                except Exception as e:
                    return {"output": "", "error": str(e), "exit_code": 1}
            
            elif cmd == 'top' or cmd == 'htop':
                try:
                    cpu_percent = psutil.cpu_percent(interval=1)
                    memory = psutil.virtual_memory()
                    disk = psutil.disk_usage('/')
                    
                    output = f"""System Information:
CPU Usage: {cpu_percent}%
Memory: {memory.percent}% ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)
Disk: {disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)

Top Processes:"""
                    
                    processes = []
                    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                        try:
                            info = proc.info
                            processes.append((info['cpu_percent'], info['pid'], info['name'], info['memory_percent']))
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
                    
                    processes.sort(reverse=True)
                    for cpu, pid, name, mem in processes[:10]:
                        output += f"\n{pid:<8} {name:<20} {cpu:.1f}% CPU, {mem:.1f}% MEM"
                    
                    return {"output": output, "error": "", "exit_code": 0}
                except Exception as e:
                    return {"output": "", "error": str(e), "exit_code": 1}
            
            elif cmd == 'clear' or cmd == 'cls':
                st.session_state.output_history = []
                return {"output": "Terminal cleared", "error": "", "exit_code": 0}
            
            elif cmd == 'help':
                help_text = """Available Commands:
📁 File & Directory Operations:
   ls, dir          - List directory contents
   cd <path>        - Change directory  
   pwd              - Show current directory
   mkdir <name>     - Create directory

🖥️  System Information:
   ps               - List running processes
   top, htop        - System resource usage
   
🔧 Terminal Commands:
   clear, cls       - Clear terminal
   help             - Show this help message
   
🤖 AI Features:
   Try natural language commands like:
   "show me all files"
   "create a folder called test"
   "what processes are running"
"""
                return {"output": help_text, "error": "", "exit_code": 0}
            
            else:
                # Try to execute as system command
                try:
                    # Change to current directory
                    original_cwd = os.getcwd()
                    os.chdir(self.current_dir)
                    
                    result = subprocess.run(
                        command, 
                        shell=True, 
                        capture_output=True, 
                        text=True, 
                        timeout=10
                    )
                    
                    os.chdir(original_cwd)
                    
                    return {
                        "output": result.stdout,
                        "error": result.stderr,
                        "exit_code": result.returncode
                    }
                except subprocess.TimeoutExpired:
                    return {"output": "", "error": "Command timed out", "exit_code": 1}
                except Exception as e:
                    return {"output": "", "error": f"Command not found: {cmd}", "exit_code": 1}
        
        except Exception as e:
            return {"output": "", "error": str(e), "exit_code": 1}

def interpret_natural_language(text: str) -> Optional[str]:
    """Use Gemini AI to interpret natural language commands"""
    if not st.session_state.ai_enabled:
        return None
    
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""Convert this natural language request into a terminal command.
Available commands: ls, dir, cd, pwd, mkdir, ps, top, clear, help
User request: "{text}"
Respond with just the command, nothing else. If you can't convert it, respond with "unknown"."""
        
        response = model.generate_content(prompt)
        command = response.text.strip().lower()
        
        if command != "unknown" and command:
            return command
        
    except Exception as e:
        st.error(f"AI interpretation error: {e}")
    
    return None

def main():
    """Main Streamlit application"""
    
    # Modern Enhanced Header
    st.markdown("""
    <div class='main-header animate-fade-in'>
        <h1>🚀 AI Python Terminal</h1>
        <p>Modern Web-Based Command Interface with Intelligent AI Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Modern Enhanced Sidebar
    with st.sidebar:
        st.markdown("""
        <div class='sidebar-header'>
            🎛️ Control Center
        </div>
        """, unsafe_allow_html=True)
        
        # Directory Selection Section
        st.markdown("### 📂 Directory Navigator")
        
        # Get available directories
        available_dirs = get_available_directories(st.session_state.current_directory)
        
        # Directory selector
        dir_options = {}
        dir_display_names = []
        
        for dir_path in available_dirs:
            display_name = format_directory_name(dir_path)
            # Ensure unique display names
            counter = 1
            original_display = display_name
            while display_name in dir_options:
                display_name = f"{original_display} ({counter})"
                counter += 1
            
            dir_options[display_name] = dir_path
            dir_display_names.append(display_name)
        
        # Find current directory in options
        current_display = None
        current_abs_path = os.path.abspath(st.session_state.current_directory)
        
        for display_name, path in dir_options.items():
            if os.path.abspath(path) == current_abs_path:
                current_display = display_name
                break
        
        # If current directory not in list, add it
        if current_display is None:
            current_display = f"📁 {os.path.basename(st.session_state.current_directory) or 'Current'}"
            dir_options[current_display] = st.session_state.current_directory
            dir_display_names.insert(0, current_display)
        
        # Directory selector with proper key
        selected_dir_display = st.selectbox(
            "Select Directory:",
            options=dir_display_names,
            index=dir_display_names.index(current_display),
            key="directory_selector",
            help="Choose a directory to navigate to"
        )
        
        # Update current directory if selection changed
        if selected_dir_display in dir_options:
            new_dir = dir_options[selected_dir_display]
            new_abs_path = os.path.abspath(new_dir)
            
            if new_abs_path != current_abs_path:
                if os.path.exists(new_dir) and os.path.isdir(new_dir):
                    st.session_state.current_directory = new_abs_path
                    st.success(f"✅ Navigated to: {new_abs_path}")
                    # Force refresh
                    time.sleep(0.1)
                    st.rerun()
                else:
                    st.error("❌ Directory no longer exists")
        
        # Manual directory input
        with st.expander("🔧 Manual Path Entry"):
            manual_path = st.text_input(
                "Enter directory path:",
                value="",
                placeholder="e.g., /home/user or C:\\Users\\User",
                key="manual_directory_input",
                help="Type the full path to navigate to any directory"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📍 Navigate", key="navigate_manual", use_container_width=True):
                    if manual_path.strip():
                        expanded_path = os.path.expanduser(manual_path.strip())
                        if os.path.exists(expanded_path) and os.path.isdir(expanded_path):
                            st.session_state.current_directory = os.path.abspath(expanded_path)
                            st.success(f"✅ Navigated to: {expanded_path}")
                            time.sleep(0.1)
                            st.rerun()
                        else:
                            st.error("❌ Directory not found or invalid path")
                    else:
                        st.warning("⚠️ Please enter a directory path")
            
            with col2:
                if st.button("📋 Current", key="copy_current", use_container_width=True, help="Copy current directory path"):
                    st.code(st.session_state.current_directory, language=None)
        
        st.markdown("---")
        
        # AI Features Section
        st.markdown("### 🤖 AI Assistant")
        ai_enabled = st.checkbox("Enable Natural Language Processing", value=st.session_state.ai_enabled)
        st.session_state.ai_enabled = ai_enabled
        
        if ai_enabled:
            st.success("✅ Gemini AI Active")
            st.info("💡 Try natural language commands like:\n- 'show me all files'\n- 'what processes are running'\n- 'create a test folder'")
        else:
            st.warning("⚠️ Basic Terminal Mode")
            st.info("📝 Standard commands available:\nls, cd, pwd, mkdir, ps, top, clear, help")
        
        st.markdown("---")
        
        # Command History Section
        st.markdown("### � Command History")
        if st.session_state.command_history:
            st.markdown("*Click any command to rerun:*")
            with st.container():
                for i, cmd in enumerate(reversed(st.session_state.command_history[-6:])):
                    if st.button(
                        f"📝 {cmd[:25]}{'...' if len(cmd) > 25 else ''}", 
                        key=f"hist_{i}", 
                        help=f"Rerun: {cmd}",
                        use_container_width=True
                    ):
                        st.session_state.rerun_command = cmd
        else:
            st.info("📋 No commands executed yet")
        
        st.markdown("---")
        
        # Quick Actions Section
        st.markdown("### ⚡ Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧹 Clear", help="Clear all history", use_container_width=True):
                st.session_state.command_history = []
                st.session_state.output_history = []
                st.rerun()
        
        with col2:
            if st.button("🏠 Home", help="Go to home directory", use_container_width=True):
                home_dir = os.path.expanduser("~")
                st.session_state.current_directory = home_dir
                st.rerun()
        
        # Additional actions
        if st.button("📊 System Info", help="Show system information", use_container_width=True):
            st.session_state.rerun_command = "top"
        
        if st.button("📁 List Files", help="List current directory", use_container_width=True):
            st.session_state.rerun_command = "ls"
        
        if st.button("🔄 Refresh", help="Refresh directory list", use_container_width=True):
            st.rerun()
    
    # Main terminal interface
    terminal = SimpleTerminal()
    
    # Enhanced current directory display
    st.markdown(f"""
    <div class='directory-display animate-fade-in'>
        <div class='directory-icon'>📁</div>
        <div>
            <div class='directory-label'>Current Directory</div>
            <div class='directory-path'>{st.session_state.current_directory}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced command input section
    st.markdown("""
    <div class='command-section animate-fade-in'>
        <div class='command-label'>
            💻 Terminal Command Input
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        command = st.text_input(
            "Enter command:",
            placeholder="Type a command (ls, cd, pwd, mkdir) or try natural language (e.g., 'show me all files')",
            key="command_input",
            label_visibility="collapsed"
        )
    
    with col2:
        execute_button = st.button("▶️ Execute", type="primary", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Handle command execution
    if execute_button and command:
        # Check if it's a natural language command
        if st.session_state.ai_enabled and not command.split()[0].lower() in ['ls', 'cd', 'pwd', 'mkdir', 'ps', 'top', 'clear', 'help', 'dir']:
            ai_command = interpret_natural_language(command)
            if ai_command:
                st.info(f"🤖 AI interpreted: '{command}' → '{ai_command}'")
                command = ai_command
        
        # Execute command
        result = terminal.execute_command(command)
        
        # Add to history
        st.session_state.command_history.append(command)
        
        # Add to output history
        timestamp = datetime.now().strftime("%H:%M:%S")
        output_entry = {
            "timestamp": timestamp,
            "command": command,
            "result": result
        }
        st.session_state.output_history.append(output_entry)
        
        # Limit history size
        if len(st.session_state.output_history) > 50:
            st.session_state.output_history = st.session_state.output_history[-50:]
    
    # Handle history button clicks
    if hasattr(st.session_state, 'rerun_command'):
        command = st.session_state.rerun_command
        delattr(st.session_state, 'rerun_command')
        
        result = terminal.execute_command(command)
        timestamp = datetime.now().strftime("%H:%M:%S")
        output_entry = {
            "timestamp": timestamp,
            "command": command,
            "result": result
        }
        st.session_state.output_history.append(output_entry)
    
    # Modern Terminal Output Display
    st.markdown("### �️ Terminal Output")
    
    if st.session_state.output_history:
        terminal_content = ""
        
        for entry in st.session_state.output_history[-15:]:  # Show last 15 commands
            # Command line with enhanced prompt
            terminal_content += f"<div style='margin: 10px 0;'>"
            terminal_content += f"<span class='prompt'>┌─ terminal@ai-python:{os.path.basename(terminal.current_dir)}$</span> <span style='color: #c9d1d9; font-weight: 500;'>{entry['command']}</span><br>"
            
            # Output with proper formatting
            if entry['result']['output']:
                terminal_content += f"<span style='color: #58a6ff;'>└─ </span><span class='success'>{entry['result']['output']}</span><br>"
            
            # Errors with enhanced styling
            if entry['result']['error']:
                terminal_content += f"<span style='color: #58a6ff;'>└─ </span><span class='error'>❌ Error: {entry['result']['error']}</span><br>"
            
            # Timestamp with subtle styling
            terminal_content += f"<span style='color: #6e7681; font-size: 11px; margin-left: 20px;'>⏱️ [{entry['timestamp']}]</span>"
            terminal_content += "</div>"
        
        st.markdown(f"""
        <div class='terminal-output' style='margin-top: 30px;'>
            {terminal_content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='terminal-output' style='margin-top: 30px;'>
            <div style='padding-top: 40px;'>
                <span class='info' style='font-size: 1.1rem;'>🚀 AI Python Terminal Ready!</span><br><br>
                <span class='info'>Type 'help' for available commands or try natural language like:</span><br><br>
                <div style='margin-left: 20px; line-height: 1.8;'>
                    <span class='warning'>• "show me all files"</span><br>
                    <span class='warning'>• "create a folder called test"</span><br>
                    <span class='warning'>• "what processes are running"</span><br>
                    <span class='warning'>• "show system information"</span><br>
                </div>
                <br><br>
                <span class='prompt'>┌─ terminal@ai-python:~$</span> <span class='blinking-cursor' style='color: #3fb950;'>▊</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Modern System Monitoring Dashboard
    st.markdown("### 📊 System Monitoring Dashboard")
    
    try:
        # Create metrics grid
        st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            cpu = psutil.cpu_percent()
            cpu_color = "var(--error-color)" if cpu > 80 else "var(--warning-color)" if cpu > 60 else "var(--success-color)"
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-icon'>🖥️</div>
                <div class='metric-value' style='color: {cpu_color};'>{cpu}%</div>
                <div class='metric-label'>CPU Usage</div>
                <div class='metric-detail'>Processing Power</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            memory = psutil.virtual_memory()
            mem_color = "var(--error-color)" if memory.percent > 80 else "var(--warning-color)" if memory.percent > 60 else "var(--success-color)"
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-icon'>💾</div>
                <div class='metric-value' style='color: {mem_color};'>{memory.percent:.1f}%</div>
                <div class='metric-label'>Memory Usage</div>
                <div class='metric-detail'>{memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            disk = psutil.disk_usage('/')
            disk_color = "var(--error-color)" if disk.percent > 90 else "var(--warning-color)" if disk.percent > 75 else "var(--success-color)"
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-icon'>💿</div>
                <div class='metric-value' style='color: {disk_color};'>{disk.percent:.1f}%</div>
                <div class='metric-label'>Disk Usage</div>
                <div class='metric-detail'>{disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            processes = len(list(psutil.process_iter()))
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-icon'>⚙️</div>
                <div class='metric-value' style='color: var(--primary-color);'>{processes}</div>
                <div class='metric-label'>Active Processes</div>
                <div class='metric-detail'>Running Tasks</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"❌ System monitoring unavailable: {str(e)}")
    
    # Enhanced Footer
    st.markdown("""
    <div class='footer'>
        <div style='font-weight: 600; margin-bottom: 0.5rem;'>
            🚀 AI Python Terminal
        </div>
        <div>
            Powered by Streamlit • Google Gemini AI • Real-time System Monitoring
        </div>
        <div style='margin-top: 0.5rem; font-size: 0.75rem; opacity: 0.7;'>
            Modern Web-Based Command Interface
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
