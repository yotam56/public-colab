from datetime import datetime

from notebook_creator import create_notebook

python_files = [
    "utils/logger.py",
    "utils/utils.py",
    "MiniCPM-V-2_6-int4/ngrok.txt",
    "MiniCPM-V-2_6-int4/main.py",
    "MiniCPM-V-2_6-int4/app.py"

]  # List of your Python files
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Generate timestamp
output_file = f"MiniCPM-V-2_6-int4/notebooks/MiniCPM-V-2_6-int4_{timestamp}.ipynb"  # Output notebook path with timestamp suffix
requirements_files = [
    "MiniCPM-V-2_6-int4/requirements/requirements.txt",
    "MiniCPM-V-2_6-int4/requirements/requirements-local.txt",
]  # List of paths to requirements files
create_notebook(python_files, output_file, requirements_files)