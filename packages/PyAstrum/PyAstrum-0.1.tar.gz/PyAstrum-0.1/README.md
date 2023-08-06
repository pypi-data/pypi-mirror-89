# PyAstrum
Python SDK to handle RESTful API of several aerospace organizations:
- NASA (api.nasa.gov)
- ESA (open.esa.int)

## Installation
1. Install `tox` on your system
    - `pip install tox`

2. Go to the project folder
    - `cd PyAstrum`

3. Set up your development environment
    - `tox --devenv <virtual_environment> -e <python_environment>`

### Example
`tox --devenv .venv-pyastrum -e py38`

4. Activate your virtual environment
    - `source .venv-pyastrum/bin/activate`

5. Run the tests and validate succesful build in the project's root directory
    - `tox`

6. If you want to run a specific environment
    - `tox -e py38`