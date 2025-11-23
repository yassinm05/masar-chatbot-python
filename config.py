import os

class Config:
    # Try to get from Environment Variables (Production), or fallback to hardcoded (Development)
    GEMINI_API_KEY = os.environ.get("Masar-Skills", "AIzaSyDqxQbXQ86PZh17gi2cAMAfc2Q9JSY06KU")
    
    # The URL of your deployed .NET API
    # If testing locally, use http://localhost:5236 or your ngrok URL
    # If production, use your Azure URL: https://masarskillsapi-production...
    MASAR_API_URL = os.environ.get("MASAR_API_URL", "https://masarskillsapi-production-v1-ashfbxekhaeffba7.canadacentral-01.azurewebsites.net")
    
    # Security token to protect the /generate endpoint so only YOUR .NET app can call it
    # You will put this same key in your .NET appsettings.json
    INTERNAL_API_KEY = os.environ.get("INTERNAL_API_KEY", "my-super-secret-internal-key")

    GEMINI_MODEL = "gemini-2.0-flash"