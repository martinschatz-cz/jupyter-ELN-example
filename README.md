# 🔬 ELN Analysis & Reporting Workflow

Welcome to the reproducible Electronic Laboratory Notebook (ELN) workflow. This project integrates Jupyter Notebooks for live data analysis, RISE for interactive presentations, and Jupyter Book for final summary exports.

---

## 🛠️ Environment Setup (Local Conda)

To ensure consistent results, we use **conda-forge** as our primary package channel. It is the community-led collection of recipes that provides the most up-to-date scientific packages.

### 1. Install Conda
If you don't have Conda installed, we recommend **Miniforge**. It comes pre-configured with `conda-forge` and is lighter than the full Anaconda distribution.
* **Get it here:** [Miniforge GitHub](https://github.com/conda-forge/miniforge)

### 2. Create the Environment
Navigate to the project root and run:
```bash
conda env create -f environment.yml
```

### 3. Activate and Launch
```bash
conda activate eln_env
jupyter lab
```

## Docker Setup & Prerequisites

To run this ELN workflow via Docker, you must ensure your host machine is prepared. This section covers what you need to have installed and how to configure it.

### 1. Prerequisites (What you need to have)

Before starting, ensure the following software is installed on your system:

* **Git:** To clone this repository. [Download here](https://git-scm.com/downloads).
* **Docker:** * **Windows/macOS:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) is required.
    * **Linux:** [Docker Engine](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) are required.
* **Hardware Virtualization:** This must be **Enabled** in your computer's BIOS/UEFI settings. (Docker will not run without it).

### 2. Windows Setup (Crucial)

If you are on Windows, you **must** use the WSL 2 (Windows Subsystem for Linux) backend for Docker to function correctly with this Python environment.

1.  **Install WSL 2:** Open PowerShell as Administrator and run:
    `wsl --install`
2.  **Docker Settings:** * Open Docker Desktop.
    * Go to **Settings > General** and ensure "Use the WSL 2 based engine" is checked.
    * Go to **Settings > Resources > WSL Integration** and enable it for your default distro.

### Docker Deployment (The Golden Standard)
For absolute reproducibility (Data Steward approved), use Docker. This ensures the code runs in the exact same environment regardless of your Operating System.

#### Option A: Standard Docker (One-liner)
##### 1. Build the image:

```bash
docker build -t eln-analysis:v1.0 .
```

##### 2. Run the container:

```bash
docker run -p 8888:8888 --name eln_instance eln-analysis:v1.0
```

#### Option B: Docker Compose (Recommended for Dev)
Docker Compose handles port mapping and volume mounting automatically, so your changes to notebooks are saved back to your local machine.

```bash
docker-compose up
```

## 💻 Operating System Specifics

Setting up a cross-platform environment requires a few "quality of life" adjustments depending on your host OS.

### 🐧 Linux (Native Docker)
Linux offers the best performance for Docker, but file permissions are the main "gotcha."

* **Permission Management:** Docker runs as `root`. Files created by the container in a mounted volume will be owned by `root`. 
  * *Fix:* Use `docker-compose` which typically handles mapping, or manually change ownership after a run: `sudo chown -R $USER:$USER ./data`.
* **Sudo Requirements:** Depending on your setup, you may need to prefix commands with `sudo` unless you’ve added your user to the `docker` group.

### 🪟 Windows (WSL 2 is Mandatory)
To avoid performance lag and pathing errors, do not run Docker on "legacy" Windows. Use **Windows Subsystem for Linux (WSL 2)**.



* **The WSL 2 Backend:** Ensure "Use the WSL 2 based engine" is checked in your **Docker Desktop Settings**. 
* **The "Line Ending" Trap:** Linux/Docker uses `LF` line endings, while Windows often defaults to `CRLF`. If your shell scripts or `environment.yml` fail with "file not found" errors, your line endings are likely wrong.
  * *Fix:* Set your editor (VS Code) to `LF` or run `git config --global core.autocrlf input` before cloning the repo.
* **Path Syntax in Terminal:**
  * **PowerShell:** Use `${PWD}` for the current directory:
    `docker run -v ${PWD}:/home/jovyan/work -p 8888:8888 eln-analysis:v1.0`
  * **Command Prompt (CMD):** Use `%cd%`:
    `docker run -v %cd%:/home/jovyan/work -p 8888:8888 eln-analysis:v1.0`



---

### 🛡️ Data Steward's Rule of Thumb
Regardless of your OS, **always run Docker commands from the project root directory**. This ensures that the relative paths defined in your `Dockerfile` and `docker-compose.yml` resolve correctly across all team members' machines.