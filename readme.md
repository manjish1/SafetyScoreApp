Please note that this is a work in progress. This came about as a startup idea with a few MBA colleagues and we worked 1 year to do customer discovery with 250 random strangers. The business model canvas is solid, now I am stumbling my way through coding this. I will update this readme with my progress. But I believe this app will have three main compoenents: Live connection to latest crime statistics, geocoding all addresses and determining the disctance to user supplied address, safety scoring algorithm and methodology. I have been able to finish the first piece and have successfully downloaded all crime stats from the Atlanta Police Department website. Now I am working on the next pieces.

# 🛡️ Atlanta Neighborhood Safety Score Web App

This Flask-based web application allows users to **enter any address in Atlanta, GA**, and instantly receive a **Safety Score (0–100)** based on **real crime data** from the Atlanta Police Department.

The app:

- ✅ Automatically **downloads the latest crime data** from [CivicTechAtlanta/apd-crime-data](https://github.com/CivicTechAtlanta/apd-crime-data)
- ✅ **Geocodes** user-entered addresses to latitude/longitude
- ✅ **Finds nearby crimes** within a 1 km radius
- ✅ **Calculates a Safety Score** (higher = safer)
- ✅ **Displays nearby crimes** on a clean webpage

---

## 📦 Features

| Feature                        | Details                                                                 |
|---------------------------------|-------------------------------------------------------------------------|
| 🔄 Auto-Updates Data            | Automatically scrapes latest crime CSV from GitHub releases.           |
| 📍 Address Geocoding            | Converts user input addresses into geographic coordinates.             |
| 📊 Proximity-Based Crime Search | Searches for crimes within a 1 km radius of the address.               |
| 🎯 Safety Scoring               | 100 - (5 × number of crimes); minimum score is 0.                      |
| 🌐 Simple Web Interface         | Clean, minimal form-based webpage to check scores instantly.           |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/atlanta-safety-score.git
cd atlanta-safety-score
```

*(Replace `yourusername` with your GitHub username if uploading.)*

---

### 2. Install Requirements

Make sure Python 3.8+ is installed.

Then run:

```bash
pip install flask pandas geopy requests beautifulsoup4
```

---

### 3. Run the App

```bash
python app.py
```

Open your browser and navigate to:

🔗 [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 🖼️ Screenshot (Optional)

> *(You can insert a screenshot showing the homepage and a sample result.)*

---

## ⚙️ How It Works

1. **User Inputs Address**  
   Example: `660 Peachtree St NE, Atlanta, GA`
   
2. **Address is Geocoded**  
   Using OpenStreetMap Nominatim API.

3. **Crime Data Downloaded**  
   Latest public CSV from CivicTechAtlanta GitHub.

4. **Nearby Crimes Filtered**  
   Crimes within 1 km radius are selected.

5. **Safety Score Calculated**  
   Formula: `Safety Score = 100 - (# crimes × 5)`, minimum 0.

6. **Results Displayed**  
   Safety score and crime details shown on the webpage.

---

## 📚 Project Structure

```
atlanta-safety-score/
│
├── app.py              # Main Flask application
├── templates/
│   └── index.html      # Web front-end
├── README.md           # This file
└── requirements.txt    # (Optional) Python dependencies
```

---

## 📈 Future Enhancements

- 🌎 Add an interactive map showing crime locations
- 📅 Allow filtering by date range (e.g., last 30 days)
- 📄 Enable exporting filtered results as CSV
- 📱 Make it mobile-friendly with responsive design
- 🔔 Offer email alerts for certain addresses

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Credits

- [CivicTechAtlanta](https://github.com/CivicTechAtlanta/apd-crime-data) — for maintaining public crime datasets
- [Nominatim OpenStreetMap API](https://nominatim.openstreetmap.org/) — for geocoding services
- [Flask Web Framework](https://flask.palletsprojects.com/)

---

## 📬 Contact

Built with ❤️ to help Atlantans stay safe.  

Have questions or suggestions?  
📧 Email: naikma@gmail.com

---

## ✅ Quick Setup Commands

```bash
pip install flask pandas geopy requests beautifulsoup4
python app.py
open http://127.0.0.1:5000/
```
