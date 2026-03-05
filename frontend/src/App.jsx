import { useState } from 'react'
import { verifyArticle } from './api'
import './App.css'

function App() {
  const [inputText, setInputText] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const data = await verifyArticle(inputText);
      setResults(data);
    } catch (err) {
      setError('Failed to verify article. Please ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const getVerdictColor = (verdict) => {
    switch (verdict.toLowerCase()) {
      case 'supported': return 'bg-success-500 text-white';
      case 'refuted': return 'bg-danger-500 text-white';
      case 'unverifiable': return 'bg-warning-500 text-white';
      default: return 'bg-slate-500 text-white';
    }
  };

  return (
    <div className="min-h-screen p-8 max-w-5xl mx-auto">
      <header className="mb-10 text-center">
        <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight mb-4">
          AI Misinformation Detector
        </h1>
        <p className="text-lg text-slate-600">
          Paste an article below to extract and verify factual claims.
        </p>
      </header>

      <main className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Section */}
        <section className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 flex flex-col">
          <h2 className="text-xl font-bold mb-4 text-slate-800">Article Input</h2>
          <form onSubmit={handleSubmit} className="flex flex-col flex-grow">
            <textarea
              className="flex-grow min-h-[300px] w-full p-4 border border-slate-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none resize-none transition-shadow text-slate-700 bg-slate-50"
              placeholder="Enter text to analyze..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !inputText.trim()}
              className="mt-4 w-full bg-primary-600 hover:bg-primary-500 text-white font-semibold py-3 px-6 rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Analyzing...
                </>
              ) : 'Verify Article'}
            </button>
          </form>
          {error && <div className="mt-4 p-3 bg-red-100 text-red-700 rounded-xl text-sm">{error}</div>}
        </section>

        {/* Results Section */}
        <section className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 flex flex-col max-h-[800px] overflow-hidden">
          <h2 className="text-xl font-bold mb-4 text-slate-800">Verification Results</h2>

          <div className="flex-grow overflow-y-auto pr-2 space-y-4">
            {!loading && !results && !error && (
              <div className="flex flex-col items-center justify-center h-full text-slate-400">
                <svg className="w-16 h-16 mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                <p>Results will appear here</p>
              </div>
            )}

            {results && results.claims && results.claims.length === 0 && (
              <div className="p-4 bg-slate-100 rounded-xl text-slate-600 text-center">
                No verifiable claims found in the text.
              </div>
            )}

            {results && results.claims && results.claims.map((claimObj, idx) => (
              <div key={idx} className="border border-slate-200 rounded-xl p-4 transition-all hover:shadow-md bg-white">
                <div className="flex justify-between items-start gap-4 mb-3">
                  <p className="font-semibold text-slate-800 leading-snug">"{claimObj.claim}"</p>
                  <span className={`px-3 py-1 text-xs font-bold uppercase tracking-wider rounded-full shrink-0 ${getVerdictColor(claimObj.verdict)}`}>
                    {claimObj.verdict}
                  </span>
                </div>

                <div className="mb-3 text-sm text-slate-600 bg-slate-50 p-3 rounded-lg border border-slate-100">
                  <span className="font-semibold block mb-1">Reasoning:</span>
                  {claimObj.reasoning}
                </div>

                <div className="flex items-center justify-between text-xs text-slate-500">
                  <span>Confidence: {(claimObj.confidence * 100).toFixed(1)}%</span>
                  {claimObj.evidence && claimObj.evidence.length > 0 && (
                    <span className="text-primary-600 cursor-pointer hover:underline" onClick={() => alert(JSON.stringify(claimObj.evidence, null, 2))}>
                      View {claimObj.evidence.length} Evidence Sources
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>

          {results && (
            <div className="mt-4 pt-4 border-t border-slate-200 text-sm text-slate-500 flex justify-between">
              <span>Extracted {results.claims_extracted} claims from {results.total_sentences} sentences.</span>
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export default App
