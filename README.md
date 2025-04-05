# Brazilian Petroleum Data Report Generator

## 🧠 Project Purpose

This project automates the creation of reports based on data from ANP (Agência Nacional do Petróleo) regarding Brazilian petroleum operations. The system processes various aspects of petroleum data including:

- Import/export volumes
- National production statistics
- Derivatives processing data

The project takes raw data in `.xls` format and transforms it into a comprehensive report through an automated pipeline. The goal is to:

1. Automate data extraction from source files
2. Process and clean the data
3. Generate meaningful visualizations
4. Create a final PDF report

The system is designed to be modular, allowing for future integration with a Streamlit web interface for enhanced user interaction.

## 📑 Table of Contents

- [Project Purpose](#-project-purpose)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [How to Use](#-how-to-use)
- [Files and Functions](#-files-and-functions)
- [Next Steps](#-next-steps)

## 🗂️ Project Structure

```
project_root/
├── config.yaml
├── app.py (optional Streamlit interface - to be built)
├── src/
│   ├── gen_csvs.py
│   └── utils/
│       └── utils.py
├── data/
│   ├── raw/
│   │   └── importacoes-exportacoes-b.xlsx
│   └── processed/
├── images/
├── report/
└── README.md
```

## 📦 Requirements

The project uses the following Python packages:

- `pandas` - For data manipulation and analysis
- `openpyxl` - For Excel file handling
- `matplotlib` or `plotly` - For data visualization (optional)
- `fpdf` - For PDF generation (optional)
- `pyyaml` - For configuration file handling

### Installation

```bash
pip install -r requirements.txt
```

## ⚙️ How to Use

1. Place your ANP data files (`.xls` format) in the `data/raw/` directory
2. Run the extraction script:

```bash
python src/gen_csvs.py
```

3. Processed data will be saved as `.csv` files in the `data/processed/` directory

## 📁 Files and Functions

### `config.yaml`
Configuration file that stores relative paths for all project folders and settings.

### `src/utils/utils.py`
Contains utility functions including:
- `load_config()`: Reads the config file and returns a dictionary with absolute paths

### `src/gen_csvs.py`
Main data processing script containing:
- `extract_importacao_petroleo()`: Extracts petroleum import data from Excel files
- `extract_dispendio_importacao_petroleo()`: Extracts petroleum import expenditure data

### Data Directories
- `data/raw/`: Stores original Excel files from ANP
- `data/processed/`: Contains processed CSV files ready for analysis

## 🚧 Next Steps

The project roadmap includes:

1. **Enhanced Data Extraction**
   - Generalize Excel table extraction to support different file structures
   - Add support for more data types and formats

2. **Visualization Features**
   - Implement data visualization using matplotlib/plotly
   - Create interactive charts and graphs

3. **Report Generation**
   - Develop PDF report generation module
   - Add customizable report templates

4. **Web Interface**
   - Build Streamlit front-end for:
     - File upload and management
     - Interactive data visualization
     - Report customization and generation

5. **Documentation**
   - Add detailed API documentation
   - Create user guides and tutorials

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
