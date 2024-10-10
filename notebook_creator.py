import nbformat as nbf
import os
import logging
from utils.logger import Logger

logger_level = os.getenv("LOGGER_LEVEL", "INFO").upper()
log_level = getattr(logging, logger_level, logging.INFO)
logger = Logger(log_level).get_logger()


def validate_inputs(python_files, output_file, requirements_files):
    """
    Validate the inputs before proceeding with notebook creation.

    :param python_files: List of Python file paths to validate
    :param output_file: Output notebook file path to validate
    :param requirements_files: List of paths to the requirements.txt files to validate
    :return: True if all inputs are valid, else raise an error
    """
    logger.info("Validating inputs.")

    # Check if all Python files exist and have a .py extension
    for py_file in python_files:
        if not os.path.isfile(py_file):
            logger.error(f"File not found: {py_file}")
            raise FileNotFoundError(f"File not found: {py_file}")
        if not (py_file.endswith(".py") or py_file.endswith(".txt")):
            logger.error(f"Invalid file extension for file: {py_file}")
            raise ValueError(f"Invalid file extension for file: {py_file}")
        logger.info(f"File '{py_file}' validated.")

    # Check if all requirements files exist and are not empty
    for req_file in requirements_files:
        if not os.path.isfile(req_file):
            logger.error(f"Requirements file not found: {req_file}")
            raise FileNotFoundError(f"Requirements file not found: {req_file}")

        with open(req_file, "r") as f:
            requirements = f.read().strip()

        if not requirements:
            logger.error(f"The requirements file '{req_file}' is empty.")
            raise ValueError(f"The requirements file '{req_file}' is empty.")

        logger.info(f"Requirements file '{req_file}' validated.")

    # Check if the output file has a valid .ipynb extension
    if not output_file.endswith(".ipynb"):
        logger.error("Output file must have a .ipynb extension.")
        raise ValueError("Output file must have a .ipynb extension.")

    logger.info(f"Output file '{output_file}' validated.")

    return True


def create_notebook(python_files, output_file, requirements_files):
    """
    Create a Jupyter notebook from multiple Python files and requirements.txt files.

    :param python_files: List of Python file paths to be included in the notebook
    :param output_file: Path for the output Jupyter notebook file (.ipynb)
    :param requirements_files: List of paths to the requirements.txt files
    """
    try:
        # Validate inputs before proceeding
        logger.info("Starting notebook creation.")
        validate_inputs(python_files, output_file, requirements_files)

        # Create a new Jupyter Notebook
        notebook = nbf.v4.new_notebook()
        logger.info("New notebook created.")

        # Consolidate all requirements from the multiple requirements files
        all_requirements = []
        try:
            for req_file in requirements_files:
                with open(req_file, "r") as f:
                    requirements = f.read().splitlines()
                    all_requirements.extend(requirements)

            # Remove duplicates from the list of requirements
            all_requirements = list(set(all_requirements))

            pip_install_code = "!pip install " + " ".join(all_requirements)
            install_cell = nbf.v4.new_code_cell(pip_install_code)

            # Add the pip install cell as the first cell in the notebook
            notebook.cells.append(install_cell)
            logger.info(
                f"Added pip install command for consolidated requirements: {all_requirements}."
            )

        except Exception as e:
            logger.error(f"Error reading or processing the requirements files: {e}")
            return

        # Add each Python file as a separate code cell
        for py_file in python_files:
            try:
                with open(py_file, "r") as f:
                    code_lines = f.readlines()

                # Filter out lines ending with # SKIP
                filtered_code = [
                    line for line in code_lines if not line.strip().endswith("# SKIP")
                ]

                # Combine the lines back to form the complete code block
                code = "".join(filtered_code)

                # Create a new code cell for the content of the Python file
                code_cell = nbf.v4.new_code_cell(code)
                notebook.cells.append(code_cell)
                logger.info(f"Added code from Python file '{py_file}'.")

            except Exception as e:
                logger.error(
                    f"Error reading or processing the Python file '{py_file}': {e}"
                )
                return

        # Write the notebook to the output file
        try:
            with open(output_file, "w") as f:
                nbf.write(notebook, f)
            logger.info(f"Notebook '{output_file}' created successfully.")

        except Exception as e:
            logger.error(f"Error writing the notebook file: {e}")
            return

    except (FileNotFoundError, ValueError) as e:
        logger.error(f"Error: {e}")
