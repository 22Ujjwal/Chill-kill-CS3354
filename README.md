## About OneStopSwitch2
This project is Group 11's project for CS 3354. We have implemented a chatbot that answers questions on the Nintendo Switch 2. This product is meant to educate potential buyers or parents of potential buyers on the 

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

This is a list of things you need to use the software.
* npm (installation command below)
  ```sh
  npm install npm@latest -g
  ```
* python3 (install via [https://www.python.org/downloads/](https://www.python.org/downloads/))
* Live Server extension on VSCode
<img width="1085" height="229" alt="Screenshot 2025-11-21 201451" src="https://github.com/user-attachments/assets/5c4f6165-9df0-446f-83fa-849fcc79e59e" />
* Scripts enabled
* Get the API keys for Firecrawl, Google Gemini, and Pinecone

### Installation and Running the Code

1. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
2. Install NPM packages
   ```sh
   npm install
   ```
3. Make your .env file in `./AI-Agent/backend` and paste your API keys
4. Run these commands
   ```sh
    cd AI-Agent
    python3 -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
   ```
5. Run the executables 
  * If you are on Windows, run: 
    ```
      ./backend-run.ps1
    ```
  * If you are on Linux or have WSL, run:
    ```
      bash backend-run.sh
    ```
6. Go to `\AI-Agent\frontend\homepageUI\nintendoHomePage.html` on VSCode, right click on the file, and select `Open with Live Server`


