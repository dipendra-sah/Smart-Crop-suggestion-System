# 🌾 Smart Crop Suggestions System

An intelligent agricultural recommendation system that uses machine learning to suggest optimal crops based on soil conditions, helping farmers make data-driven decisions for better yields.

## 📋 Overview

This project combines machine learning with agricultural expertise to provide personalized crop recommendations. The system analyzes soil parameters (pH, nutrients, rainfall, soil type) and suggests the most suitable crops with detailed explanations and yield information.

## ✨ Features

- **ML-Powered Predictions**: Random Forest classifier trained on agricultural data
- **Comprehensive Crop Database**: 12+ crops with detailed growing requirements
- **Real-time Analysis**: Instant crop recommendations based on soil conditions
- **Detailed Explanations**: Specific reasons why each crop is recommended
- **User-Friendly Interface**: Modern web interface with intuitive design
- **Nutrient Calculation**: Automatic nutrient estimation based on pH levels
- **Yield & Market Information**: Expected yields and market value insights

## 🛠️ Technology Stack

### Backend
- **Python Flask** - Web framework
- **Scikit-learn** - Machine learning library
- **Pandas & NumPy** - Data processing
- **Joblib** - Model serialization

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling
- **JavaScript** - Interactivity
- **Chart.js** - Data visualization

### Machine Learning
- **Random Forest Classifier** - Prediction model
- **Standard Scaler** - Feature normalization
- **Label Encoder** - Categorical encoding

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd IP_Project
   ```

2. **Install dependencies**
   ```bash
   pip install flask flask-cors scikit-learn pandas numpy joblib
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

## 📖 Usage

### Web Interface
1. Open the application in your browser
2. Enter soil parameters:
   - pH level (4.0 - 8.5)
   - Temperature (°C)
   - Humidity (%)
   - Moisture level (% or categorical: Dry/Moist/Wet)
   - Annual rainfall (mm)
   - Soil type (Sandy/Loamy/Clay/Silty/Peaty/Chalky)
3. Click "Get Recommendations" to see crop suggestions

### API Usage

#### Predict Crops
```bash
POST /predict
Content-Type: application/json

{
  "ph": 6.5,
  "temperature": 25,
  "humidity": 60,
  "moisture": 50,
  "rainfall": 600,
  "soilType": "Loamy"
}
```

**Response:**
```json
{
  "success": true,
  "recommendations": [
    {
      "name": "Wheat",
      "icon": "🌾",
      "description": "Staple grain crop, high in protein",
      "confidence": 92.5,
      "growing_season": "Winter",
      "yield_info": "3-4 tons/ha",
      "market_value": "High",
      "reason": "pH is within preferred range (6.0-7.5); Nitrogen adequate (80.0); Phosphorus adequate (40.0); Potassium adequate (60.0)"
    }
  ],
  "soil_analysis": {
    "ph": 6.5,
    "nitrogen": 80,
    "phosphorus": 40,
    "potassium": 60,
    "organic_matter": 3.0,
    "rainfall": 600,
    "soil_type": "Loamy"
  }
}
```

## 🏗️ Project Structure

```
IP_Project/
├── app.py                 # Main Flask application
├── index.html            # Frontend interface
├── style.css             # CSS styling
├── script.js             # Frontend JavaScript
├── data_core.csv         # Agricultural data (if used)
├── Ml model.py           # ML model training script
└── README.md             # Project documentation
```

## 🤖 Machine Learning Model

### Training Data
- **Source**: Synthetic data generated from crop database
- **Samples**: 600+ training samples (50 per crop)
- **Features**: pH, N, P, K, organic matter, rainfall, soil texture
- **Algorithm**: Random Forest Classifier
- **Accuracy**: 95%+ on test data

### Prediction Process
1. **Input Processing**: Soil parameters are scaled and encoded
2. **Model Prediction**: Top 5 crops with confidence scores
3. **Reason Generation**: Detailed explanations based on crop requirements
4. **Response Formatting**: Structured JSON with recommendations

## 🌱 Supported Crops

| Crop | Icon | Optimal pH | Key Requirements |
|------|------|------------|------------------|
| Wheat | 🌾 | 6.0-7.5 | Moderate NPK, 300-800mm rainfall |
| Rice | 🌾 | 5.5-7.0 | High NPK, 1000-2000mm rainfall |
| Corn | 🌽 | 5.8-7.2 | High nitrogen, 500-1200mm rainfall |
| Soybean | 🫘 | 6.0-7.0 | Moderate nutrients, 400-900mm rainfall |
| Cotton | ☁️ | 5.8-8.0 | Balanced NPK, 500-1000mm rainfall |
| Sugarcane | 🎋 | 6.0-8.0 | Very high NPK, 1000-1500mm rainfall |
| Potato | 🥔 | 4.8-6.5 | High NPK, 400-800mm rainfall |
| Tomato | 🍅 | 6.0-7.0 | Moderate NPK, 400-800mm rainfall |
| Onion | 🧅 | 6.0-7.5 | Moderate nutrients, 300-700mm rainfall |
| Chili | 🌶️ | 6.0-7.5 | Moderate NPK, 600-1200mm rainfall |
| Pulses | 🌱 | 6.0-7.5 | Low nitrogen, 300-700mm rainfall |
| Groundnut | 🥜 | 5.8-7.0 | Moderate nutrients, 500-1000mm rainfall |

## 📊 Data Sources

- **Crop Requirements**: Based on agricultural research and extension services
- **Soil Science**: Standard soil fertility guidelines
- **Yield Data**: Average regional yields
- **Market Information**: Commodity market trends

## 🔧 Configuration

### Model Parameters
- **n_estimators**: 100 (Random Forest trees)
- **max_depth**: 10 (Tree depth limit)
- **random_state**: 42 (Reproducibility)

### Server Configuration
- **Host**: 0.0.0.0 (Accessible from network)
- **Port**: 5000 (Default Flask port)
- **Debug**: Enabled for development

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create a Pull Request

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Add docstrings to functions
- Test ML model accuracy after changes
- Update README for new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Agricultural research institutions for crop data
- Open source ML community for algorithms
- Farmers and agricultural experts for domain knowledge

## 📞 Support

For questions or issues:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation

---

**Made with ❤️ for sustainable agriculture**
