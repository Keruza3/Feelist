import { useState } from 'react';

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:5000/api/mood/ai", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Error:", err);
      setResult({ mood: "error", quote: "Algo falló 😵", tracks: [] });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-zinc-900 text-white flex flex-col items-center justify-center p-4 gap-4">
      <h1 className="text-3xl font-bold text-purple-400">Feelist 🎧</h1>
      <textarea
        className="w-full max-w-xl h-32 p-3 rounded bg-zinc-800 text-white resize-none"
        placeholder="¿Cómo te sentís hoy?"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button
        className="bg-purple-600 px-6 py-2 rounded hover:bg-purple-500 disabled:opacity-50"
        onClick={handleGenerate}
        disabled={loading || !text.trim()}
      >
        {loading ? "Sintiendo cosas..." : "Generar"}
      </button>

      {result && (
        <div className="mt-6 text-center">
          <h2 className="text-xl font-bold text-purple-300">{result.mood}</h2>
          <p className="italic text-zinc-300 mb-2">"{result.quote}"</p>
          <ul className="list-disc list-inside text-zinc-200">
            {result.tracks.map((track, i) => (
              <li key={i}>
                {track.title} — <span className="text-purple-400">{track.artist}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
