import React, { useState, useEffect } from 'react';

const SAMPLE_CLAIMS = [
  "Drinking 5 liters of alkaline water daily completely prevents heart disease.",
  "James Webb Space Telescope found evidence of carbon-bearing molecules on exoplanet K2-18b",
  "Humans only use 10% of their brain.",
  "Eating garlic daily cures viral respiratory infections entirely.",
  "The Great Wall of China is visible from space with the naked eye."
];

export default function App() {
  const [claim, setClaim] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeStep, setActiveStep] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [activeTab, setActiveTab] = useState("checker");

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const res = await fetch("/api/history");
      if (res.ok) {
        const data = await res.json();
        setHistory(data);
      }
    } catch (e) {
      console.error("Failed to load history:", e);
    }
  };

  const handleFactCheck = async (claimToTest) => {
    const text = claimToTest || claim;
    if (!text.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);
    setActiveTab("checker");

    setActiveStep(1);
    const t1 = setTimeout(() => setActiveStep(2), 1200);
    const t2 = setTimeout(() => setActiveStep(3), 2600);
    const t3 = setTimeout(() => setActiveStep(4), 3800);

    try {
      const response = await fetch("/api/factcheck", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ claim: text.trim() }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Fact-check analysis failed.");
      }

      setResult(data);
      fetchHistory();
    } catch (err) {
      setError(err.message);
    } finally {
      clearTimeout(t1);
      clearTimeout(t2);
      clearTimeout(t3);
      setLoading(false);
      setActiveStep(0);
    }
  };

  const getVerdictBadge = (verdict, isContested) => {
    if (isContested || verdict === "Contested") {
      return {
        label: "CONTESTED CLAIM",
        bg: "bg-amber-500/10 text-amber-400 border-amber-500/30",
        glow: "border-amber-500/50 shadow-amber-500/20",
        icon: "⚠️"
      };
    }
    if (verdict === "False") {
      return {
        label: "FALSE / DEBUNKED",
        bg: "bg-red-500/10 text-red-400 border-red-500/30",
        glow: "border-red-500/50 shadow-red-500/20",
        icon: "❌"
      };
    }
    if (verdict === "True") {
      return {
        label: "VERIFIED TRUE",
        bg: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
        glow: "border-emerald-500/50 shadow-emerald-500/20",
        icon: "✅"
      };
    }
    if (verdict === "Mostly True") {
      return {
        label: "MOSTLY TRUE",
        bg: "bg-sky-500/10 text-sky-400 border-sky-500/30",
        glow: "border-sky-500/50 shadow-sky-500/20",
        icon: "✔️"
      };
    }
    return {
      label: "INSUFFICIENT EVIDENCE",
      bg: "bg-gray-500/10 text-gray-400 border-gray-500/30",
      glow: "",
      icon: "❓"
    };
  };

  const getAgentIcon = (name) => {
    if (name.includes("Science")) return "🔬";
    if (name.includes("Health")) return "🩺";
    if (name.includes("Politics")) return "🏛️";
    return "🧠";
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col antialiased">
      {/* Top Navigation */}
      <header className="border-b border-slate-800 bg-slate-900/60 sticky top-0 z-50 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3.5 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <span className="text-xl">🛡️</span>
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight text-white flex items-center gap-2">
                VeritasNet
                <span className="text-xs px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 font-semibold border border-indigo-500/30">
                  Decentralized Fact-Check Network
                </span>
              </h1>
              <p className="text-xs text-slate-400">GenAI Consensus Engine & On-Chain Proof Registry</p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => setActiveTab("checker")}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
                activeTab === "checker"
                  ? "bg-indigo-600 text-white shadow"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
              }`}
            >
              ⚡ Live Fact-Checker
            </button>
            <button
              onClick={() => setActiveTab("history")}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
                activeTab === "history"
                  ? "bg-indigo-600 text-white shadow"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
              }`}
            >
              📜 On-Chain Ledger
              {history.length > 0 && (
                <span className="ml-1 px-1.5 py-0.2 text-[10px] rounded-full bg-indigo-900 text-indigo-200 border border-indigo-700">
                  {history.length}
                </span>
              )}
            </button>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-8 flex-1 w-full">
        {activeTab === "checker" ? (
          <div className="space-y-8">
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
              <div className="max-w-3xl">
                <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight mb-2">
                  Submit Claim for Multi-Agent Consensus
                </h2>
                <p className="text-sm text-slate-400 mb-6">
                  Our system retrieves live search evidence, queries 4 independent domain-specialized AI agents in parallel, computes a confidence-weighted consensus, and anchors a cryptographic proof.
                </p>
              </div>

              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleFactCheck();
                }}
                className="space-y-4"
              >
                <textarea
                  rows="3"
                  value={claim}
                  onChange={(e) => setClaim(e.target.value)}
                  placeholder="Paste a viral headline, claim, or policy statement to verify..."
                  className="w-full bg-slate-950/90 border border-slate-800 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                />

                <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
                  <div className="flex flex-wrap items-center gap-1.5">
                    <span className="text-xs text-slate-400 font-medium mr-1">Quick Try:</span>
                    {SAMPLE_CLAIMS.slice(0, 3).map((sc, idx) => (
                      <button
                        key={idx}
                        type="button"
                        onClick={() => {
                          setClaim(sc);
                          handleFactCheck(sc);
                        }}
                        className="text-[11px] px-2.5 py-1 rounded-md bg-slate-800 hover:bg-indigo-950 text-slate-300 hover:text-indigo-200 border border-slate-700/50 transition truncate max-w-[200px]"
                        title={sc}
                      >
                        {sc}
                      </button>
                    ))}
                  </div>

                  <button
                    type="submit"
                    disabled={loading || !claim.trim()}
                    className="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-sm font-bold shadow-lg shadow-indigo-600/30 transition flex items-center justify-center gap-2"
                  >
                    {loading ? "Analyzing Network..." : "⚡ Verify Claim"}
                  </button>
                </div>
              </form>
            </div>

            {loading && (
              <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 text-center space-y-4 animate-pulse">
                <h3 className="text-sm font-semibold text-indigo-300">
                  Decentralized Multi-Agent Consensus in Progress...
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 max-w-3xl mx-auto text-xs font-medium">
                  <div className={`p-2 rounded-lg border ${activeStep >= 1 ? 'bg-indigo-950/60 border-indigo-500/50 text-indigo-200' : 'bg-slate-950/40 border-slate-800 text-slate-500'}`}>
                    🌐 1. Retrieve Web Evidence
                  </div>
                  <div className={`p-2 rounded-lg border ${activeStep >= 2 ? 'bg-indigo-950/60 border-indigo-500/50 text-indigo-200' : 'bg-slate-950/40 border-slate-800 text-slate-500'}`}>
                    🤖 2. 4 Parallel AI Agents
                  </div>
                  <div className={`p-2 rounded-lg border ${activeStep >= 3 ? 'bg-indigo-950/60 border-indigo-500/50 text-indigo-200' : 'bg-slate-950/40 border-slate-800 text-slate-500'}`}>
                    ⚖️ 3. Weighted Consensus
                  </div>
                  <div className={`p-2 rounded-lg border ${activeStep >= 4 ? 'bg-indigo-950/60 border-indigo-500/50 text-indigo-200' : 'bg-slate-950/40 border-slate-800 text-slate-500'}`}>
                    ⛓️ 4. Anchor Proof On-Chain
                  </div>
                </div>
              </div>
            )}

            {error && (
              <div className="p-4 rounded-xl bg-red-950/40 border border-red-500/40 text-red-300 text-sm">
                {error}
              </div>
            )}

            {result && (
              <div className="space-y-6">
                {(() => {
                  const badge = getVerdictBadge(result.final_verdict, result.is_contested);
                  return (
                    <div className={`bg-slate-900/80 border rounded-2xl p-6 sm:p-8 ${badge.glow}`}>
                      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
                        <div>
                          <span className="text-xs uppercase tracking-wider text-slate-400 font-semibold">
                            Network Consensus Verdict
                          </span>
                          <div className="flex items-center gap-3 mt-1.5">
                            <span className={`text-sm sm:text-base font-extrabold px-3.5 py-1.5 rounded-xl border ${badge.bg}`}>
                              {badge.icon} {badge.label}
                            </span>
                          </div>
                        </div>

                        <div className="flex items-center gap-4 bg-slate-950/70 px-4 py-2.5 rounded-xl border border-slate-800">
                          <div className="text-right">
                            <div className="text-xs text-slate-400">Consensus Confidence</div>
                            <div className="text-lg font-bold text-white">
                              {Math.round(result.overall_confidence * 100)}%
                            </div>
                          </div>
                          <div className="w-16 bg-slate-800 rounded-full h-2.5 overflow-hidden">
                            <div
                              className="bg-indigo-500 h-2.5 rounded-full"
                              style={{ width: `${Math.round(result.overall_confidence * 100)}%` }}
                            ></div>
                          </div>
                        </div>
                      </div>

                      <div className="mt-5 space-y-2">
                        <h3 className="text-sm font-semibold text-slate-300">Executive Summary:</h3>
                        <p className="text-sm text-slate-200 bg-slate-950/60 p-4 rounded-xl border border-slate-800/80 leading-relaxed">
                          {result.consensus_summary}
                        </p>
                      </div>

                      <div className="mt-6 pt-5 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-3 text-xs">
                        <div className="flex items-center gap-2 text-slate-400">
                          <span className="text-indigo-400">⛓️</span>
                          <span className="font-semibold text-slate-300">On-Chain Proof:</span>
                          <code className="bg-slate-950 px-2 py-0.5 rounded text-[11px] text-indigo-300 border border-slate-800">
                            {result.blockchain_tx ? result.blockchain_tx.slice(0, 14) + "..." + result.blockchain_tx.slice(-8) : "Local Proof"}
                          </code>
                        </div>

                        <a
                          href={`https://sepolia.etherscan.io/tx/${result.blockchain_tx}`}
                          target="_blank"
                          rel="noreferrer"
                          className="px-3 py-1 rounded-lg bg-indigo-950 hover:bg-indigo-900 text-indigo-300 border border-indigo-800/60 font-medium transition"
                        >
                          Verify Proof On Explorer ↗
                        </a>
                      </div>
                    </div>
                  );
                })()}

                {/* 4 Specialized Agents Breakdown */}
                <div>
                  <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                    <span>🤖</span> 4 Specialized AI Agents Breakdown
                  </h3>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {result.agents.map((agent, i) => {
                      const badge = getVerdictBadge(agent.verdict, false);
                      return (
                        <div key={i} className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2.5">
                              <span className="text-xl">{getAgentIcon(agent.agent_name)}</span>
                              <div>
                                <h4 className="text-sm font-bold text-white">{agent.agent_name}</h4>
                                <p className="text-[11px] text-slate-400">{agent.persona.slice(0, 45)}...</p>
                              </div>
                            </div>
                            <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded-lg border ${badge.bg}`}>
                              {agent.verdict}
                            </span>
                          </div>

                          <p className="text-xs text-slate-300 leading-relaxed bg-slate-950/40 p-3 rounded-lg border border-slate-800/40">
                            {agent.reasoning}
                          </p>
                          {agent.model_id && (
                            <p className="text-[10px] text-indigo-300">
                              Model: {agent.model_id}
                            </p>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Retrieved Sources */}
                {result.sources && result.sources.length > 0 && (
                  <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 space-y-4">
                    <h3 className="text-base font-bold text-white">
                      📚 Retrieved Grounding Sources ({result.sources.length})
                    </h3>
                    <div className="space-y-3">
                      {result.sources.map((src, i) => (
                        <div key={i} className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800">
                          <a
                            href={src.url}
                            target="_blank"
                            rel="noreferrer"
                            className="text-xs font-semibold text-indigo-300 hover:underline"
                          >
                            [{i + 1}] {src.title} ↗
                          </a>
                          <p className="text-[11px] text-slate-400 mt-1">{src.snippet}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        ) : (
          /* History View */
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-white">Immutable Fact-Check Ledger</h2>
            <div className="space-y-4">
              {history.map((item) => {
                const badge = getVerdictBadge(item.final_verdict, item.is_contested);
                return (
                  <div key={item.id} className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-slate-400">{new Date(item.timestamp).toLocaleString()}</span>
                      <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded-lg border ${badge.bg}`}>
                        {badge.icon} {item.final_verdict} ({Math.round(item.overall_confidence * 100)}%)
                      </span>
                    </div>
                    <h3 className="text-sm font-bold text-white">{item.claim}</h3>
                    <p className="text-xs text-slate-300 bg-slate-950/60 p-3 rounded-lg">{item.consensus_summary}</p>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </main>

      <footer className="border-t border-slate-900 bg-slate-950/80 py-6 text-center text-xs text-slate-500">
        VeritasNet Fact-Checking Network • Built for Hackathon Demo
      </footer>
    </div>
  );
}
