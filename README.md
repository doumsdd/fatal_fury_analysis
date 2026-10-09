# Fatal Fury: City of the Wolves - Character Analysis Project

A comprehensive data storytelling and visualization project exploring the roster of **Fatal Fury: City of the Wolves** through frame data analysis, statistical clustering, and machine learning.

## 🎮 About the Project

This project scrapes character stats, move properties, and portraits from the DreamCancel Wiki to generate insights into the fighting game's balance and character archetypes. It combines raw frame data analysis with interactive dashboarding (powered by Lovable) to visualize relationships between characters.

### Key Features

*   **Frame Data Extraction**: Automated parsing of startup frames, damage values, and recovery times.
*   **Machine Learning Clustering**: Unsupervised learning (K-Means) to identify playstyles (Zoners, Rushdown, Grapplers).
*   **Portrait Scraping**: Automatically downloads official character art directly from the wiki.
*   **Interactive Dashboard**: Ready-to-deploy JSON structure for frontend visualization on Lovable.

## 📂 Project Structure

| File | Description |
| :--- | :--- |
| `config.py` | Centralized configuration for API endpoints and fallback data. |
| `wiki_api.py` | Wrapper for MediaWiki API requests. |
| `scrape_portraits.py` | Script to download character portraits based on CSV/JSON input. |
| `generate_lovable_json.py` | Generates the final JSON payload with embedded image links/Base64. |
| `lovable_data.json` | The output file ready for import into Lovable. |
| `README.md` | This documentation file. |

## 🚀 Getting Started

To run this analysis locally, you need Python 3.8+ and the following dependencies:

```bash
pip install pandas requests beautifulsoup4 numpy scikit-learn
```

### Running the Scraper

1.  Ensure the game page is accessible at `https://dreamcancel.com/wiki/Fatal_Fury:_City_of_the_Wolves`.
2.  Run the configuration and scraping scripts:
    ```bash
    python config.py  # Optional: just checks environment
    python scrape_portraits.py
    ```

### Generating the Dashboard

After collecting data, generate the JSON file for your frontend:
```bash
python generate_lovable_json.py
```

## 🤖 Methodology & ML Insights

*   **Data Collection**: We aggregate per-move statistics (Startup, Active, Recovery, Damage) to calculate "Character Averages".
*   **Clustering**: We normalize features like *Average Startup Speed* vs *Total Damage Output* to see where characters fall on the power-spectrum curve.
*   **Anomaly Detection**: We identify "Outliers" – characters who have extreme stats compared to their peers (e.g., a slow character with massive damage).

## 📜 License

For educational and analytical purposes only. Fatal Fury is a registered trademark of SNK.