#!/usr/bin/env python3
"""
Test script for the prediction service
"""

import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from app.services.prediction_service import prediction_service
    print("✅ Successfully imported prediction service")
    
    # Test model loading
    print(f"📊 Loaded {len(prediction_service.player_models)} player models")
    print(f"🏆 Goals against model: {'✅' if prediction_service.goals_against_model else '❌'}")
    
    # List available models
    if prediction_service.player_models:
        print("🎯 Available player models:")
        for player_name in prediction_service.player_models.keys():
            print(f"   - {player_name}")
    
    print("\n🚀 Prediction service is ready!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the project root directory")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
