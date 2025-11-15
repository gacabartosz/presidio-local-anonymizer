"""
Setup API - Backend installation wizard
Provides endpoints for system checks and installation
"""

import os
import sys
import subprocess
import platform
import shutil
import logging
from pathlib import Path
from flask import Blueprint, jsonify, request

logger = logging.getLogger(__name__)
setup_bp = Blueprint('setup', __name__)

def check_command(command):
    """Check if command is available"""
    return shutil.which(command) is not None

def run_command(cmd, cwd=None, timeout=300):
    """Run shell command and return output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'stdout': '',
            'stderr': 'Command timeout',
            'returncode': -1
        }
    except Exception as e:
        return {
            'success': False,
            'stdout': '',
            'stderr': str(e),
            'returncode': -1
        }

@setup_bp.route('/check-system', methods=['GET'])
def check_system():
    """Check if system has all requirements"""
    logger.info("Checking system requirements...")

    checks = {
        'python': {
            'name': 'Python 3.8+',
            'status': False,
            'version': None,
            'message': ''
        },
        'pip': {
            'name': 'pip (Python package manager)',
            'status': False,
            'version': None,
            'message': ''
        },
        'git': {
            'name': 'Git',
            'status': False,
            'version': None,
            'message': ''
        },
        'venv': {
            'name': 'Python venv module',
            'status': False,
            'version': None,
            'message': ''
        }
    }

    # Check Python
    try:
        python_version = sys.version_info
        version_str = f"{python_version.major}.{python_version.minor}.{python_version.micro}"
        checks['python']['version'] = version_str
        checks['python']['status'] = python_version >= (3, 8)
        checks['python']['message'] = f"Python {version_str} installed"
    except Exception as e:
        checks['python']['message'] = str(e)

    # Check pip
    if check_command('pip3') or check_command('pip'):
        result = run_command('pip3 --version' if check_command('pip3') else 'pip --version')
        if result['success']:
            checks['pip']['status'] = True
            checks['pip']['version'] = result['stdout'].strip()
            checks['pip']['message'] = 'pip is installed'
    else:
        checks['pip']['message'] = 'pip not found'

    # Check git
    if check_command('git'):
        result = run_command('git --version')
        if result['success']:
            checks['git']['status'] = True
            checks['git']['version'] = result['stdout'].strip()
            checks['git']['message'] = 'Git is installed'
    else:
        checks['git']['message'] = 'Git not found'

    # Check venv
    result = run_command(f'{sys.executable} -m venv --help')
    checks['venv']['status'] = result['success']
    checks['venv']['message'] = 'venv module available' if result['success'] else 'venv module not found'

    # Calculate overall status
    all_passed = all(check['status'] for check in checks.values())

    return jsonify({
        'success': True,
        'all_passed': all_passed,
        'platform': {
            'system': platform.system(),
            'machine': platform.machine(),
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        },
        'checks': checks
    })

@setup_bp.route('/install-instructions', methods=['GET'])
def install_instructions():
    """Get platform-specific installation instructions"""
    system = platform.system()

    instructions = {
        'Darwin': {  # macOS
            'python': 'brew install python3',
            'git': 'brew install git',
            'pip': 'Already included with Python 3',
            'venv': 'Already included with Python 3'
        },
        'Linux': {
            'python': 'sudo apt install python3 python3-pip python3-venv  # Ubuntu/Debian\nsudo dnf install python3 python3-pip  # Fedora',
            'git': 'sudo apt install git  # Ubuntu/Debian\nsudo dnf install git  # Fedora',
            'pip': 'Included with Python 3',
            'venv': 'Included with Python 3'
        },
        'Windows': {
            'python': 'Download from https://www.python.org/downloads/\nMake sure to check "Add Python to PATH"',
            'git': 'Download from https://git-scm.com/download/win',
            'pip': 'Included with Python 3',
            'venv': 'Included with Python 3'
        }
    }

    return jsonify({
        'success': True,
        'system': system,
        'instructions': instructions.get(system, instructions['Linux'])
    })

@setup_bp.route('/status', methods=['GET'])
def get_status():
    """Get current backend status"""
    backend_dir = Path(__file__).parent.parent
    venv_dir = backend_dir / '.venv'
    requirements_file = backend_dir / 'requirements.txt'

    return jsonify({
        'success': True,
        'backend_running': True,  # If this endpoint responds, backend is running
        'venv_exists': venv_dir.exists(),
        'requirements_exists': requirements_file.exists(),
        'backend_dir': str(backend_dir)
    })
