# Disease Death Count Dashboard

An interactive dashboard built using [Dash](https://dash.plotly.com/) to visualize death counts from COVID-19, pneumonia, influenza, and other causes across U.S. states.

## Important Notes
The dashboard requires COVID-19_Death_Counts.csv in the same directory as app.py.

Default port is 8052. You can change it by modifying the app.run() line in app.py.

All updates to the visualizations are triggered via buttons – no need to auto-refresh.

## Built With
Dash
Plotly
Pandas
NumPy

---

##  Included Files

- `app.py` – Main script to run the dashboard.
- `requirements.txt` – Python dependencies.
- `COVID-19_Death_Counts.csv` – **Required CSV file** with death count data *(must be in the same folder as `app.py`)*.

---

## Requirements

- Python 3.7+
- `pip` (Python package installer)

---

## Getting Started

Follow these steps to run the dashboard locally:

### 1.1 Clone or Download the Repository if you use git

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

### 1.2 Or download and extract the ZIP file manually.**

If you prefer not to use Git, follow these steps to download the files manually:
<img width="989" alt="Screenshot 2025-03-21 at 6 06 54 PM" src="https://github.com/user-attachments/assets/3ad523c4-679f-4290-9bef-4f79a672a30e" />

Click the "Code" button at the top of the repository.

Select "Download ZIP".

Once downloaded, locate the ZIP file on your computer.

Extract the ZIP 
Open the extracted folder and proceed with the setup instructions.



### 2. (Optional) Create a Virtual Environment
``` bash
python -m venv venv
# Activate the environment:
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```
It creates a virtual environment (a folder named venv) that contains its own installation of Python and pip. 

Any packages you install (like Dash, Pandas, etc.) go only into this environment, not your global Python setup.
It keeps your project clean and prevents version conflicts between different projects.

### 3.Install Dependencies
```bash
pip install -r requirements.txt
```

### 4.Run the Application
```bash
python app.py
```
If successful, the terminal will show something like:
**Dash Running on http://127.0.0.1:8052/**

### 5. Open the Dashboard
Go to your browser and copy and post the link after Dash Running on:

http://127.0.0.1:8052/


You’ll see a fully interactive dashboard with:
Time Series Plot
Violin & Box Plots
Scatterplot Matrix
Heatmap

