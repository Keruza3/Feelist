## 🎧 Feelist

Feelist is a mood-based playlist generator that turns your emotional chaos into musical coherence.

Describe how you feel — no filters, no dropdowns.  
You'll get back a mood label, a relatable quote, and a playlist that slaps (or cries, depending on your vibe).  
Built with GPT, irony, and the slow-burning desire to avoid real problems.

Feel something. Hear something.

## Local usage

1. Install the backend dependencies:

```bash
cd backend
pip install -r requirements.txt
```

2. Create a `.env` file inside `backend/` and set the required environment variables:

```
OPENAI_API_KEY=your_key
GPT_MODEL=gpt-3.5-turbo
# PORT is optional (defaults to 5000)
```

3. Start the Flask server:

```bash
python app.py
```

The API will be available at `http://localhost:5000`.

4. Open the `frontend/` page in your browser:

Open `frontend/index.html` directly or serve the folder with any static server. Make sure `script.js` points to the backend URL.
