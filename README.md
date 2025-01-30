Code Organization:
------------------
- The project follows a modular structure, separating core functionality into differebt modules for better maintainability.
- The main functionality is found in research_paper_fetcher_pubmed.
- Tests are located in test directory.
- pyproject.toml is a configuration file which is used to manage dependencies and environment settings.
- main.py and fetcher.py are located in research_paper_fetcher_pubmed.


Setting up environment and dependencies using poetry:
----------------------------------------
1. Poetry installation : pip install poetry
2. Any library installation : pip install <library_name>
3. Poetry version check : poetry --version
4. Create new project : poetry new <project_name> (navigate to the folder where you want to create a project)
5. Create environment : poetry install (automatically creates a virtual environment)
6. Install and add dependencies : poetry add <dependency_name>
7. Activate virtual environment : poetry shell
8. If shell doesnt work then navigate to venv path and use : <path>\Scripts\activate
9. To check environment info : poetry env info
10. To run a file : poetry run python <file_name>
11. To deactivate : deactivate


Libraries and LLM's used:
-------------------------
1. sys : Used for command line arguments.
2. os : Used to fetch the path of the saved file.
3. requests : Sending requests to the organization for access of database and fetching their responses.
4. csv : To handle csv format files.
5. xml : It is used for parsing and creating xml documents.
6. GitHub copilot : Used for text generation like comments and text modification.
7. ChatGPT : Used for code analysis, increase efficiency and performance of the logic.