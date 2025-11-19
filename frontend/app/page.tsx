"use client";
import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);
    try {
      // Replace URL with your Render Backend URL when deployed
      const res = await fetch(`http://127.0.0.1:8000/recommend?song=${query}`);
      const data = await res.json();
      setResults(data);
    } catch (error) {
      console.error(error);
    }
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-zinc-900 text-white p-10 flex flex-col items-center">
      <h1 className="text-5xl font-bold bg-gradient-to-r from-green-400 to-blue-500 text-transparent bg-clip-text mb-4">
        TuneTexture
      </h1>
      <p className="mb-8 text-zinc-400">Discover music by texture, not popularity.</p>

      <div className="flex gap-2 w-full max-w-md mb-10">
        <input
          type="text"
          placeholder="Enter a song you love..."
          className="flex-1 p-3 rounded bg-zinc-800 border border-zinc-700 focus:outline-none focus:border-green-500"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          className="bg-green-500 text-black font-bold px-6 rounded hover:bg-green-400 transition"
        >
          {loading ? "Analyzing..." : "Find Gems"}
        </button>
      </div>

      {results && (
        <div className="w-full max-w-4xl grid md:grid-cols-2 gap-8">
          {/* Input Song Stats */}
          <div className="bg-zinc-800 p-6 rounded-xl border border-zinc-700">
            <h2 className="text-xl font-bold mb-2">Analyzed Texture</h2>
            <p className="text-2xl text-green-400 font-bold">{results.searched_song.name}</p>
            <p className="text-zinc-400 mb-4">{results.searched_song.artist}</p>
            
            <div className="space-y-2">
                {Object.entries(results.searched_song.features).map(([key, val]: any) => (
                    <div key={key} className="flex justify-between text-sm">
                        <span className="capitalize">{key}</span>
                        <div className="w-32 bg-zinc-700 rounded-full h-2 mt-1.5">
                            {/* Simple bar chart visualization */}
                            <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${Math.min(val * 100, 100)}%` }}></div>
                        </div>
                    </div>
                ))}
            </div>
          </div>

          {/* Recommendations */}
          <div className="bg-zinc-800 p-6 rounded-xl border border-zinc-700">
            <h2 className="text-xl font-bold mb-4">Hidden Gems Found</h2>
            <ul className="space-y-3">
              {results.recommendations.map((rec: any, i: number) => (
                <li key={i} className="flex items-center justify-between p-3 bg-zinc-700/50 rounded hover:bg-zinc-700 transition cursor-pointer">
                  <div>
                    <p className="font-semibold">{rec.name}</p>
                    <p className="text-sm text-zinc-400">{rec.artist}</p>
                  </div>
                  <a 
                    href={`https://open.spotify.com/track/${rec.id}`} 
                    target="_blank" 
                    className="text-green-400 text-sm hover:underline"
                  >
                    Play
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </main>
  );
}
