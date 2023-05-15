#!/bin/bash
set -e
trap 'err=$?; echo >&2 "Exiting on error $err"; exit $err' ERR

function cecho() {
    color=$1
    shift
    text=$@
    NC='\033[0m' # No Color
    case $color in
        red)     col=$'\e[1;31m' ;;
        green)   col=$'\e[1;32m' ;;
        yellow)  col=$'\e[1;33m' ;;
        blue)    col=$'\e[1;34m' ;;
        magenta) col=$'\e[1;35m' ;;
        cyan)    col=$'\e[1;36m' ;;
    esac
    echo -e "${col}${text}${NC}"
}

activate_virtualenv() {
    cecho yellow "Activating virtual environment..."
    # check if virtual environment exists
    if [ ! -d "venv" ]; then
        cecho red "Virtual environment does not exist. Run install command to create one."
        exit 1
    fi

    # Check if bin/Scripts directory exists
    if [ -d "venv/bin" ]; then
        source venv/bin/activate
    elif [ -d "venv/Scripts" ]; then
        source venv/Scripts/activate
    else
        cecho red "Virtual environment is not activated. Please activate it manually."
        exit 1
    fi
}

# Function to get the FastAPI server PID
get_fastapi_pid() {
    cecho yellow "Searching for FastAPI server PID..."

    if [ -f fastapi.pid ]; then
        fastapi_pid=$(cat fastapi.pid)
    else
        fastapi_pid=""
    fi
}

# Function to start the FastAPI server
start_fastapi() {
    get_fastapi_pid
    if [ -z "$fastapi_pid" ]; then
        nohup python run.py > uvicorn.log 2>&1 &
        fastapi_pid=$!
        echo $fastapi_pid > fastapi.pid
        cecho green "-------------- FastAPI server started --------------"
    else
        cecho blue "-------------- FastAPI server is already running --------------"
    fi
}

# Function to check the status of the FastAPI server
status_fastapi() {
    get_fastapi_pid
    if [ -z "$fastapi_pid" ]; then
        cecho red "-------------- FastAPI server is not running --------------"
    else
        cecho green "-------------- FastAPI server is running with PID: $fastapi_pid --------------"
    fi
}

# Function to stop the FastAPI server
stop_fastapi() {
    get_fastapi_pid
    if [ -z "$fastapi_pid" ]; then
        cecho red "-------------- FastAPI server is not running --------------"
    else
        kill -9 $fastapi_pid
        rm fastapi.pid
        cecho green "-------------- FastAPI server stopped --------------"
    fi
}

# Function to restart the FastAPI server
restart_fastapi() {
    stop_fastapi
    start_fastapi
}


# Function to install all requirements
install_requirements(){

    cecho yellow "Searching for Python installation..."
    # Locate the latest version of Python installed
    python_path=$(ls -t $(which -a python python2 python3) | head -1)

    # Check if Python is installed, else throw an error message
    if [ -z "$python_path" ]; then
        cecho red "Python is not installed. Please install it before proceeding."
        exit 1
    else
        cecho green "Using python installed at: $python_path"
    fi

    cecho yellow "Searching for venv ..."
    # Check if a virtual environment exists or create one
    venv_dir="venv"
    if [ ! -d "$venv_dir" ]; then
        cecho yellow "Creating a virtual environment..."
        "$python_path" -m venv "$venv_dir"
    else
        cecho green "Virtual enviroment already exists."
    fi

    # Activate the virtual environment
    activate_virtualenv

    cecho yellow "Installing latest pip ..."
    # Upgrade pip
    python -m pip install --upgrade pip

    # Install all requirements from requirements.txt using activated virtual environment
    if [ -f "requirements.txt" ]; then
        cecho yellow "Installing requirements ..."
        pip3 install -r requirements.txt

        cecho green "Requirements installed successfully."
    else
        echo red "requirements.txt not found."
    fi
}



# activate the virtual environment
venv_dir="venv"
if [ ! -d "$venv_dir" ]; then
    cecho red "Virtual enviroment does not exist. Run install command to create one."
else
    activate_virtualenv
fi

# Check the command after the server.sh script
case "$1" in
    "start")
        start_fastapi
        ;;
    "restart")
        restart_fastapi
        ;;
    "status")
        status_fastapi
        ;;
    "stop")
        stop_fastapi
        ;;
    "install")
        install_requirements
        ;;
    *)
        echo "Usage: $0 {start|restart|status|stop|install}"
esac
