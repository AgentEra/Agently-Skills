from agently import Agently

Agently.set_settings(
    "OpenAICompatible",
    {
        "base_url": "https://api.example.com/v1",
        "model": "demo-model",
        "auth": "YOUR_API_KEY",
    },
)
