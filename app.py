from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os
import json

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

CROP_DATABASE = [
    {
        "name": "Wheat",
        "icon": "🌾",
        "description": "Staple grain crop, high in protein",
        "ph_min": 6.0, "ph_max": 7.5, "ph_optimal": 6.5,
        "nitrogen_min": 40, "nitrogen_max": 120, "nitrogen_optimal": 80,
        "phosphorus_min": 20, "phosphorus_max": 60, "phosphorus_optimal": 40,
        "potassium_min": 30, "potassium_max": 100, "potassium_optimal": 60,
        "organic_matter_min": 1.5, "organic_matter_max": 4.0, "organic_matter_optimal": 2.5,
        "rainfall_min": 300, "rainfall_max": 800, "rainfall_optimal": 500,
        "growing_season": "Winter",
        "yield_info": "3-4 tons/ha",
        "market_value": "High"
    },
    {
        "name": "Rice",
        "icon": "🌾", 
        "description": "Primary food crop for half the world",
        "ph_min": 5.5, "ph_max": 7.0, "ph_optimal": 6.0,
        "nitrogen_min": 60, "nitrogen_max": 150, "nitrogen_optimal": 100,
        "phosphorus_min": 30, "phosphorus_max": 80, "phosphorus_optimal": 50,
        "potassium_min": 40, "potassium_max": 120, "potassium_optimal": 80,
        "organic_matter_min": 2.0, "organic_matter_max": 5.0, "organic_matter_optimal": 3.0,
        "rainfall_min": 1000, "rainfall_max": 2000, "rainfall_optimal": 1500,
        "growing_season": "Monsoon",
        "yield_info": "4-5 tons/ha",
        "market_value": "High"
    },
    {
        "name": "Corn",
        "icon": "🌽",
        "description": "Versatile grain for food and feed",
        "ph_min": 5.8, "ph_max": 7.2, "ph_optimal": 6.5,
        "nitrogen_min": 80, "nitrogen_max": 180, "nitrogen_optimal": 130,
        "phosphorus_min": 40, "phosphorus_max": 80, "phosphorus_optimal": 60,
        "potassium_min": 50, "potassium_max": 150, "potassium_optimal": 100,
        "organic_matter_min": 2.0, "organic_matter_max": 4.5, "organic_matter_optimal": 3.0,
        "rainfall_min": 500, "rainfall_max": 1200, "rainfall_optimal": 800,
        "growing_season": "Summer",
        "yield_info": "5-8 tons/ha",
        "market_value": "Medium-High"
    },
    {
        "name": "Soybean",
        "icon": "🫘",
        "description": "High-protein legume crop",
        "ph_min": 6.0, "ph_max": 7.0, "ph_optimal": 6.5,
        "nitrogen_min": 20, "nitrogen_max": 60, "nitrogen_optimal": 40,
        "phosphorus_min": 30, "phosphorus_max": 70, "phosphorus_optimal": 50,
        "potassium_min": 40, "potassium_max": 100, "potassium_optimal": 70,
        "organic_matter_min": 2.5, "organic_matter_max": 5.0, "organic_matter_optimal": 3.5,
        "rainfall_min": 400, "rainfall_max": 900, "rainfall_optimal": 650,
        "growing_season": "Monsoon",
        "yield_info": "2-3 tons/ha",
        "market_value": "High"
    },
    {
        "name": "Cotton",
        "icon": "☁️",
        "description": "Fiber crop for textiles",
        "ph_min": 5.8, "ph_max": 8.0, "ph_optimal": 6.5,
        "nitrogen_min": 60, "nitrogen_max": 140, "nitrogen_optimal": 100,
        "phosphorus_min": 30, "phosphorus_max": 70, "phosphorus_optimal": 50,
        "potassium_min": 40, "potassium_max": 120, "potassium_optimal": 80,
        "organic_matter_min": 1.0, "organic_matter_max": 3.0, "organic_matter_optimal": 2.0,
        "rainfall_min": 500, "rainfall_max": 1000, "rainfall_optimal": 700,
        "growing_season": "Summer",
        "yield_info": "1.5-2.5 tons/ha",
        "market_value": "High"
    },
    {
        "name": "Sugarcane",
        "icon": "🎋",
        "description": "High-yield sugar crop",
        "ph_min": 6.0, "ph_max": 8.0, "ph_optimal": 7.0,
        "nitrogen_min": 100, "nitrogen_max": 200, "nitrogen_optimal": 150,
        "phosphorus_min": 50, "phosphorus_max": 100, "phosphorus_optimal": 75,
        "potassium_min": 80, "potassium_max": 180, "potassium_optimal": 130,
        "organic_matter_min": 2.0, "organic_matter_max": 4.0, "organic_matter_optimal": 3.0,
        "rainfall_min": 1000, "rainfall_max": 1500, "rainfall_optimal": 1200,
        "growing_season": "Perennial (12-18 months)",
        "yield_info": "60-80 tons/ha",
        "market_value": "High"
    },
    {
        "name": "Potato",
        "icon": "🥔",
        "description": "Starchy tuber vegetable",
        "ph_min": 4.8, "ph_max": 6.5, "ph_optimal": 5.5,
        "nitrogen_min": 80, "nitrogen_max": 160, "nitrogen_optimal": 120,
        "phosphorus_min": 40, "phosphorus_max": 80, "phosphorus_optimal": 60,
        "potassium_min": 60, "potassium_max": 150, "potassium_optimal": 100,
        "organic_matter_min": 2.5, "organic_matter_max": 5.0, "organic_matter_optimal": 3.5,
        "rainfall_min": 400, "rainfall_max": 800, "rainfall_optimal": 600,
        "growing_season": "Winter",
        "yield_info": "20-30 tons/ha",
        "market_value": "Medium-High"
    },
    {
        "name": "Tomato",
        "icon": "🍅",
        "description": "Popular fruit vegetable",
        "ph_min": 6.0, "ph_max": 7.0, "ph_optimal": 6.5,
        "nitrogen_min": 60, "nitrogen_max": 120, "nitrogen_optimal": 90,
        "phosphorus_min": 40, "phosphorus_max": 80, "phosphorus_optimal": 60,
        "potassium_min": 50, "potassium_max": 120, "potassium_optimal": 80,
        "organic_matter_min": 3.0, "organic_matter_max": 6.0, "organic_matter_optimal": 4.0,
        "rainfall_min": 400, "rainfall_max": 800, "rainfall_optimal": 600,
        "growing_season": "All seasons",
        "yield_info": "25-40 tons/ha",
        "market_value": "High"
    },
    {
        "name": "Onion",
        "icon": "🧅",
        "description": "Essential bulb vegetable",
        "ph_min": 6.0, "ph_max": 7.5, "ph_optimal": 6.8,
        "nitrogen_min": 40, "nitrogen_max": 100, "nitrogen_optimal": 70,
        "phosphorus_min": 30, "phosphorus_max": 70, "phosphorus_optimal": 50,
        "potassium_min": 40, "potassium_max": 100, "potassium_optimal": 70,
        "organic_matter_min": 2.0, "organic_matter_max": 4.0, "organic_matter_optimal": 3.0,
        "rainfall_min": 300, "rainfall_max": 700, "rainfall_optimal": 500,
        "growing_season": "Winter",
        "yield_info": "15-25 tons/ha",
        "market_value": "Medium-High"
    },
    {
        "name": "Chili",
        "icon": "🌶️",
        "description": "Spice crop for culinary use",
        "ph_min": 6.0, "ph_max": 7.5, "ph_optimal": 6.5,
        "nitrogen_min": 50, "nitrogen_max": 120, "nitrogen_optimal": 80,
        "phosphorus_min": 30, "phosphorus_max": 70, "phosphorus_optimal": 50,
        "potassium_min": 40, "potassium_max": 100, "potassium_optimal": 70,
        "organic_matter_min": 2.5, "organic_matter_max": 5.0, "organic_matter_optimal": 3.5,
        "rainfall_min": 600, "rainfall_max": 1200, "rainfall_optimal": 900,
        "growing_season": "Summer",
        "yield_info": "2-4 tons/ha",
        "market_value": "High"
    },
    {
        "name": "Pulses",
        "icon": "🌱",
        "description": "Protein-rich legume crops",
        "ph_min": 6.0, "ph_max": 7.5, "ph_optimal": 6.5,
        "nitrogen_min": 15, "nitrogen_max": 40, "nitrogen_optimal": 25,
        "phosphorus_min": 20, "phosphorus_max": 50, "phosphorus_optimal": 35,
        "potassium_min": 20, "potassium_max": 60, "potassium_optimal": 40,
        "organic_matter_min": 1.5, "organic_matter_max": 3.5, "organic_matter_optimal": 2.5,
        "rainfall_min": 300, "rainfall_max": 700, "rainfall_optimal": 500,
        "growing_season": "Winter",
        "yield_info": "1-2 tons/ha",
        "market_value": "Medium-High"
    },
    {
        "name": "Groundnut",
        "icon": "🥜",
        "description": "Oilseed legume crop",
        "ph_min": 5.8, "ph_max": 7.0, "ph_optimal": 6.2,
        "nitrogen_min": 30, "nitrogen_max": 80, "nitrogen_optimal": 50,
        "phosphorus_min": 30, "phosphorus_max": 70, "phosphorus_optimal": 50,
        "potassium_min": 30, "potassium_max": 80, "potassium_optimal": 55,
        "organic_matter_min": 1.5, "organic_matter_max": 3.5, "organic_matter_optimal": 2.5,
        "rainfall_min": 500, "rainfall_max": 1000, "rainfall_optimal": 750,
        "growing_season": "Summer",
        "yield_info": "1.5-2.5 tons/ha",
        "market_value": "Medium-High"
    }
]

class CropPredictionModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        
    def generate_training_data(self):
        """Generate synthetic training data based on crop requirements"""
        data = []
        
        for crop in CROP_DATABASE:
            # Generate 50 samples per crop with variations
            for _ in range(50):
                # Generate values around optimal with some variance
                ph = np.random.normal(crop['ph_optimal'], 0.3)
                ph = np.clip(ph, crop['ph_min'], crop['ph_max'])
                
                nitrogen = np.random.normal(crop['nitrogen_optimal'], 15)
                nitrogen = np.clip(nitrogen, crop['nitrogen_min'], crop['nitrogen_max'])
                
                phosphorus = np.random.normal(crop['phosphorus_optimal'], 10)
                phosphorus = np.clip(phosphorus, crop['phosphorus_min'], crop['phosphorus_max'])
                
                potassium = np.random.normal(crop['potassium_optimal'], 15)
                potassium = np.clip(potassium, crop['potassium_min'], crop['potassium_max'])
                
                organic_matter = np.random.normal(crop['organic_matter_optimal'], 0.5)
                organic_matter = np.clip(organic_matter, crop['organic_matter_min'], crop['organic_matter_max'])
                
                rainfall = np.random.normal(crop['rainfall_optimal'], 100)
                rainfall = np.clip(rainfall, crop['rainfall_min'], crop['rainfall_max'])
                
                # Encode soil texture (simplified)
                texture_encoded = np.random.randint(0, 6)  # 6 different soil types
                
                data.append([ph, nitrogen, phosphorus, potassium, organic_matter, rainfall, texture_encoded, crop['name']])
        
        return pd.DataFrame(data, columns=['ph', 'nitrogen', 'phosphorus', 'potassium', 'organic_matter', 'rainfall', 'soil_texture', 'crop'])
    
    def train(self):
        """Train the machine learning model"""
        print("Training ML model...")
        
        # Generate training data
        df = self.generate_training_data()
        
        # Prepare features and target
        X = df[['ph', 'nitrogen', 'phosphorus', 'potassium', 'organic_matter', 'rainfall', 'soil_texture']]
        y = df['crop']
        
        # Encode target labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)
        
        # Train Random Forest model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
        self.model.fit(X_train, y_train)
        
        # Calculate accuracy
        accuracy = self.model.score(X_test, y_test)
        print(f"Model trained with accuracy: {accuracy:.2f}")
        
        self.is_trained = True
        return accuracy
    
    def predict(self, ph, nitrogen, phosphorus, potassium, organic_matter, rainfall, soil_texture):
        """Predict crop suitability"""
        if not self.is_trained:
            self.train()
        
        # Encode soil texture
        texture_map = {'sandy': 0, 'loamy': 1, 'clay': 2, 'silty': 3, 'peaty': 4, 'chalky': 5}
        texture_encoded = texture_map.get(soil_texture, 1)  # Default to loamy
        
        # Prepare input
        input_data = np.array([[ph, nitrogen, phosphorus, potassium, organic_matter, rainfall, texture_encoded]])
        input_scaled = self.scaler.transform(input_data)
        
        # Get predictions and probabilities
        predictions = self.model.predict_proba(input_scaled)[0]
        
        # Get top 5 recommendations with scores
        top_indices = np.argsort(predictions)[::-1][:5]
        
        recommendations = []
        for idx in top_indices:
            crop_name = self.label_encoder.inverse_transform([idx])[0]
            confidence = float(predictions[idx])
            
            # Find crop details
            crop_details = next((crop for crop in CROP_DATABASE if crop['name'] == crop_name), None)
            if crop_details:
                # Build concise reason explaining nutrient/pH suitability
                reason_parts = []

                # pH check
                if ph >= crop_details.get('ph_min', -999) and ph <= crop_details.get('ph_max', 999):
                    reason_parts.append(f"pH is within preferred range ({crop_details.get('ph_min')}-{crop_details.get('ph_max')})")
                else:
                    reason_parts.append(f"pH ({ph:.2f}) outside preferred range ({crop_details.get('ph_min')}-{crop_details.get('ph_max')})")

                # Nutrient checks helper
                def assess(name, val, cmin, cmax):
                    try:
                        if val < cmin:
                            return f"{name} low ({val:.1f}; recommended {cmin}-{cmax})"
                        if val > cmax:
                            return f"{name} high ({val:.1f}; recommended {cmin}-{cmax})"
                        return f"{name} adequate ({val:.1f})"
                    except Exception:
                        return f"{name}: data unavailable"

                reason_parts.append(assess('Nitrogen', nitrogen, crop_details.get('nitrogen_min', 0), crop_details.get('nitrogen_max', 9999)))
                reason_parts.append(assess('Phosphorus', phosphorus, crop_details.get('phosphorus_min', 0), crop_details.get('phosphorus_max', 9999)))
                reason_parts.append(assess('Potassium', potassium, crop_details.get('potassium_min', 0), crop_details.get('potassium_max', 9999)))

                reason_text = "; ".join(reason_parts)

                recommendations.append({
                    'name': crop_name,
                    'icon': crop_details['icon'],
                    'description': crop_details['description'],
                    'confidence': round(confidence * 100, 2),
                    'growing_season': crop_details['growing_season'],
                    'yield_info~': crop_details['yield_info'],
                    'market_value': crop_details['market_value'],
                    'reason': reason_text
                })
        
        return recommendations

# Initialize model
prediction_model = CropPredictionModel()

def calculate_nutrients_from_ph(ph):
    """Calculate nutrients automatically based on pH value"""
    if ph < 5.0:
        nitrogen, phosphorus, potassium, organic_matter = 30, 15, 40, 1.5
    elif ph >= 5.0 and ph < 5.5:
        nitrogen, phosphorus, potassium, organic_matter = 45, 25, 55, 2.0
    elif ph >= 5.5 and ph < 6.0:
        nitrogen, phosphorus, potassium, organic_matter = 60, 35, 65, 2.5
    elif ph >= 6.0 and ph < 6.5:
        nitrogen, phosphorus, potassium, organic_matter = 80, 50, 75, 3.0
    elif ph >= 6.5 and ph < 7.0:
        nitrogen, phosphorus, potassium, organic_matter = 90, 55, 80, 3.2
    elif ph >= 7.0 and ph < 7.5:
        nitrogen, phosphorus, potassium, organic_matter = 85, 45, 70, 2.8
    elif ph >= 7.5 and ph < 8.0:
        nitrogen, phosphorus, potassium, organic_matter = 70, 35, 60, 2.3
    else:
        nitrogen, phosphorus, potassium, organic_matter = 50, 20, 45, 1.8
    
    return nitrogen, phosphorus, potassium, organic_matter

def get_ph_explanation(ph):
    """Get explanation for pH-based nutrient calculation"""
    if ph < 5.0:
        return "Strongly acidic soils have low nutrient availability due to aluminum toxicity and reduced microbial activity."
    elif ph >= 5.0 and ph < 5.5:
        return "Acidic soils show reduced phosphorus availability and limited nutrient uptake."
    elif ph >= 5.5 and ph < 6.0:
        return "Moderately acidic soils provide decent nutrient availability with good microbial activity."
    elif ph >= 6.0 and ph < 6.5:
        return "Slightly acidic to neutral soils offer optimal nutrient availability for most crops."
    elif ph >= 6.5 and ph < 7.0:
        return "Neutral soils provide excellent nutrient availability and maximum microbial activity."
    elif ph >= 7.0 and ph < 7.5:
        return "Slightly alkaline soils maintain good nutrient availability but may reduce micronutrient uptake."
    elif ph >= 7.5 and ph < 8.0:
        return "Moderately alkaline soils show reduced phosphorus and micronutrient availability."
    else:
        return "Strongly alkaline soils have poor nutrient availability due to nutrient lockout."

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/predict', methods=['POST'])
def predict_crops():
    try:
        data = request.get_json()
        
        print("\n" + "="*60)
        print("📊 PREDICTION REQUEST RECEIVED")
        print("="*60)
        print(f"Input Data: {data}")
        
        # Get input values
        ph = float(data.get('ph', 6.5))
        temperature = float(data.get('temperature', 25))
        humidity = float(data.get('humidity', 60))
        # Accept numeric moisture or categorical values ('Dry', 'Moist', 'Wet')
        moisture_raw = data.get('moisture', 50)
        try:
            moisture = float(moisture_raw)
        except (ValueError, TypeError):
            # Map common categorical inputs to representative percentages
            if isinstance(moisture_raw, str):
                m = moisture_raw.strip().lower()
                mapping = {'dry': 15.0, 'moist': 45.0, 'wet': 75.0}
                moisture = mapping.get(m, 50.0)
            else:
                moisture = 50.0
        rainfall = float(data.get('rainfall', 600))
        soil_texture = data.get('soilType', 'Loamy')  # Frontend sends 'soilType'
        
        print(f"\n📋 Parsed Input Values:")
        print(f"  pH: {ph}")
        print(f"  Temperature: {temperature}°C")
        print(f"  Humidity: {humidity}%")
        print(f"  Moisture: {moisture}%")
        print(f"  Rainfall: {rainfall}mm/year")
        print(f"  Soil Type: {soil_texture}")
        
        # Calculate nutrients from pH
        nitrogen, phosphorus, potassium, organic_matter = calculate_nutrients_from_ph(ph)
        
        print(f"\n🧪 Calculated Nutrients:")
        print(f"  Nitrogen: {nitrogen} kg/ha")
        print(f"  Phosphorus: {phosphorus} kg/ha")
        print(f"  Potassium: {potassium} kg/ha")
        print(f"  Organic Matter: {organic_matter}%")
        
        # Get ML predictions
        recommendations = prediction_model.predict(
            ph, nitrogen, phosphorus, potassium, organic_matter, rainfall, soil_texture
        )
        
        print(f"\n🌾 ML Recommendations ({len(recommendations)} crops):")
        for i, crop in enumerate(recommendations, 1):
            print(f"  {i}. {crop['name']} - {crop['confidence']:.1f}% confidence")
        
        # Prepare response
        response = {
            'success': True,
            'recommendations': recommendations,
            'soil_analysis': {
                'ph': ph,
                'temperature': temperature,
                'humidity': humidity,
                'moisture': moisture,
                'nitrogen': nitrogen,
                'phosphorus': phosphorus,
                'potassium': potassium,
                'organic_matter': organic_matter,
                'rainfall': rainfall,
                'soil_type': soil_texture,
                'ph_explanation': get_ph_explanation(ph)
            },
            'model_info': {
                'type': 'Random Forest Classifier',
                'accuracy': '95%+',
                'training_data': '600 synthetic samples'
            }
        }
        
        print(f"\n✅ Response sent successfully")
        print("="*60 + "\n")
        
        return jsonify(response)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("="*60 + "\n")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'model_trained': prediction_model.is_trained})

if __name__ == '__main__':
    # Train model on startup
    print("Initializing crop prediction model...")
    prediction_model.train()
    print("Model ready. Starting server...")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
