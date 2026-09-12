from agently import Agently

Agently.set_settings(
    "plugins.ModelRequester.OpenAICompatible",
    {
        "base_url": "https://api.example.com/v1",
        "model": "demo-model",
        "auth": "${ENV.DEMO_API_KEY}",
    },
)
