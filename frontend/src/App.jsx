import React, { useState, useEffect } from 'react';

const SAMPLE_CLAIMS = [
  "Drinking 5 liters of alkaline water daily completely prevents heart disease.",
  "James Webb Space Telescope found evidence of carbon-bearing molecules on exoplanet K2-18b",
  "Humans only use 10% of their brain.",
  "Eating garlic daily cures viral respiratory infections entirely.",
  "The Great Wall of China is visible from space with the naked eye."
];

const LOADING_STEPS = [
  { icon: "🌐", label: "1. Retrieve Web Evidence" },
  { icon: "🤖", label: "2. 4 Parallel AI Agents" },
  { icon: "⚖️", label: "3. Weighted Consensus" },
  { icon: "⛓️", label: "4. Anchor Proof On-Chain" },
];

const VERDICT_STYLES = {
  "True":       { short: "TRUE",        icon: "✓", pillBg: "bg-emerald-50", pillBorder: "border-emerald-200", pillText: "text-emerald-700", pillIcon: "bg-emerald-100 text-emerald-600", badge: "bg-emerald-50 text-emerald-600 border-emerald-200" },
  "Mostly True":{ short: "MOSTLY TRUE", icon: "✓", pillBg: "bg-sky-50",     pillBorder: "border-sky-200",     pillText: "text-sky-700",     pillIcon: "bg-sky-100 text-sky-600",         badge: "bg-sky-50 text-sky-600 border-sky-200" },
  "False":      { short: "FALSE",       icon: "✕", pillBg: "bg-red-50",     pillBorder: "border-red-200",     pillText: "text-red-600",     pillIcon: "bg-red-100 text-red-600",         badge: "bg-red-50 text-red-500 border-red-200" },
  "Contested":  { short: "CONTESTED",   icon: "⚠️", pillBg: "bg-amber-50",   pillBorder: "border-amber-200",   pillText: "text-amber-700",   pillIcon: "bg-amber-100 text-amber-600",     badge: "bg-amber-50 text-amber-600 border-amber-200" },
  "Uncertain":  { short: "UNCERTAIN",   icon: "?",  pillBg: "bg-gray-50",    pillBorder: "border-gray-200",    pillText: "text-gray-700",    pillIcon: "bg-gray-100 text-gray-600",       badge: "bg-gray-50 text-gray-600 border-gray-200" },
};

const CHALLENGE_STYLES = {
  "NO_SIGNIFICANT_CHALLENGE": { label: "No Challenge",   bg: "bg-emerald-50 text-emerald-700 border-emerald-200", icon: "✓" },
  "WEAK_CHALLENGE":           { label: "Weak Challenge", bg: "bg-sky-50 text-sky-700 border-sky-200",             icon: "↯" },
  "STRONG_CHALLENGE":         { label: "Strong Challenge", bg: "bg-orange-50 text-orange-700 border-orange-200",  icon: "⚡" },
  "VERDICT_INVALIDATED":      { label: "Invalidated",    bg: "bg-red-50 text-red-700 border-red-200",             icon: "✗" },
};

const getVerdictStyles = (v, contested) =>
  VERDICT_STYLES[contested ? "Contested" : (v in VERDICT_STYLES ? v : "Uncertain")];

const agentIcon = (name) =>
  name.includes("Science") ? "🔬" :
  name.includes("Health")  ? "🩺" :
  name.includes("Politics")? "🏛️" : "👤";

const displayAgentName = (name) => name.replace(/\bAgent\b/g, "Uncle");

export default function App() {
  const [claim, setClaim] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeStep, setActiveStep] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [activeTab, setActiveTab] = useState("checker");
  const [showProofDetails, setShowProofDetails] = useState(false);
  const [expandedCards, setExpandedCards] = useState({});
  const [daChallenges, setDaChallenges] = useState({});
  const [daLoading, setDaLoading] = useState({});

  useEffect(() => { fetchHistory(); }, []);

  const fetchHistory = async () => {
    try {
      const res = await fetch("/api/history");
      if (res.ok) setHistory(await res.json());
    } catch (e) { /* no-op */ }
  };

  const resetResultState = () => {
    setExpandedCards({});
    setDaChallenges({});
    setDaLoading({});
    setShowProofDetails(false);
  };

  const handleFactCheck = async (claimToTest) => {
    const text = (claimToTest || claim).trim();
    if (!text) return;

    setLoading(true);
    setError(null);
    setResult(null);
    setActiveTab("checker");
    resetResultState();

    setActiveStep(1);
    const timers = [1200, 2600, 3800].map((d, i) => setTimeout(() => setActiveStep(i + 2), d));

    try {
      const res = await fetch("/api/factcheck", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ claim: text }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Fact-check analysis failed.");
      setResult(data);
      fetchHistory();
    } catch (err) {
      setError(err.message);
    } finally {
      timers.forEach(clearTimeout);
      setLoading(false);
      setActiveStep(0);
    }
  };

  const toggleCard = (i) =>
    setExpandedCards(prev => ({ ...prev, [i]: !prev[i] }));

  const runDevilsAdvocate = async (agent) => {
    const key = agent.agent_name;
    setDaLoading(prev => ({ ...prev, [key]: true }));
    try {
      const res = await fetch("/api/challenge-agent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          claim: result.claim,
          agent_name: agent.agent_name,
          agent_verdict: agent.verdict,
          agent_confidence: agent.confidence,
          agent_reasoning: agent.reasoning,
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Devil's Advocate failed.");
      setDaChallenges(prev => ({ ...prev, [key]: data }));
    } catch (err) {
      setDaChallenges(prev => ({ ...prev, [key]: { error: err.message } }));
    } finally {
      setDaLoading(prev => ({ ...prev, [key]: false }));
    }
  };

  // ================ Sub-components ================
  const BadgePill = ({ verdict, contested, small }) => {
    const vs = getVerdictStyles(verdict, contested);
    return (
      <span className={`${small ? "text-[11px] px-2.5 py-0.5" : "text-xs px-3 py-1"} rounded-full border font-bold flex-shrink-0 ${vs.badge}`}>
        {vs.short}
      </span>
    );
  };

  const HistoryItem = ({ item }) => {
    const vs = getVerdictStyles(item.final_verdict, item.is_contested);
    return (
      <div
        onClick={() => { setResult(item); setActiveTab("checker"); resetResultState(); }}
        className="p-3.5 rounded-xl bg-white border border-slate-200 cursor-pointer hover:border-indigo-300 hover:shadow-sm transition space-y-2"
      >
        <div className="flex justify-between items-start gap-3">
          <p className="text-sm font-semibold text-slate-900 line-clamp-2">{item.claim}</p>
          <span className="text-[11px] font-bold px-2.5 py-0.5 rounded-full border flex-shrink-0"
                style={{ backgroundColor: vs.badge.split(" ")[0], color: vs.badge.split(" ")[1], borderColor: vs.badge.split(" ")[2] }}>
            {vs.short}
          </span>
        </div>
        <p className="text-xs text-slate-500">{new Date(item.timestamp).toLocaleString()}</p>
      </div>
    );
  };

  const GrandpaChallenge = ({ agent }) => {
    const key = agent.agent_name;
    const result = daChallenges[key];
    const isLoading = daLoading[key];
    const badge = result && !result.error ? (CHALLENGE_STYLES[result.challenge_status] || CHALLENGE_STYLES["NO_SIGNIFICANT_CHALLENGE"]) : null;

    return (
      <div className="bg-amber-50/80 border border-amber-200 rounded-2xl p-4 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-xl">�</span>
            <h5 className="text-sm font-bold text-amber-800">Grandpa — Independent Fact Check</h5>
          </div>
          {badge && !isLoading && (
            <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${badge.bg}`}>
              {badge.icon} {badge.label}
            </span>
          )}
        </div>

        {!result && !isLoading && (
          <button onClick={() => runDevilsAdvocate(agent)}
                  className="w-full text-xs font-semibold px-3 py-2.5 rounded-xl bg-amber-600 hover:bg-amber-500 text-white transition flex items-center justify-center gap-1.5 shadow-sm">
            🔍 Ask Grandpa to Double-Check
          </button>
        )}

        {isLoading && (
          <div className="text-xs text-amber-700 bg-amber-100/70 px-3 py-2.5 rounded-xl flex items-center gap-2 border border-amber-200">
            <span className="animate-spin text-sm">⏳</span>
            Grandpa is fact-checking the uncles' work...
          </div>
        )}

        {result && !isLoading && result.error && (
          <div className="text-xs text-red-700 bg-red-50 px-3 py-2.5 rounded-xl border border-red-200">
            Grandpa couldn't finish: {result.error}
          </div>
        )}

        {result && !isLoading && !result.error && (
          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-2.5">
              <div className="bg-white p-3 rounded-xl border border-amber-100">
                <div className="text-[9px] uppercase text-slate-500 font-semibold tracking-wide">Grandpa's Doubt</div>
                <div className="text-base font-bold text-amber-700 mt-0.5">{Math.round(result.challenge_confidence * 100)}%</div>
              </div>
              <div className="bg-white p-3 rounded-xl border border-amber-100">
                <div className="text-[9px] uppercase text-slate-500 font-semibold tracking-wide">Grandpa Says</div>
                <div className="text-sm font-bold text-slate-800 mt-0.5">{result.suggested_verdict}</div>
              </div>
            </div>

            <p className="text-xs text-slate-700 leading-relaxed bg-white p-3 rounded-xl border border-slate-100">
              {result.explanation}
            </p>

            {result.contradicting_evidence?.length > 0 && (
              <ul className="space-y-1.5">
                <div className="text-[10px] uppercase text-red-600 font-semibold mb-1 flex items-center gap-1">
                  <span>✗</span> Grandpa Found Holes Here
                </div>
                {result.contradicting_evidence.map((e, i) => (
                  <li key={i} className="text-xs text-red-700/90 bg-red-50 px-3 py-2 rounded-lg border border-red-100">• {e}</li>
                ))}
              </ul>
            )}

            {result.supporting_original?.length > 0 && (
              <ul className="space-y-1.5">
                <div className="text-[10px] uppercase text-emerald-600 font-semibold mb-1 flex items-center gap-1">
                  <span>✓</span> Grandpa Says the Uncles Were Right
                </div>
                {result.supporting_original.map((e, i) => (
                  <li key={i} className="text-xs text-emerald-800/90 bg-emerald-50 px-3 py-2 rounded-lg border border-emerald-100">• {e}</li>
                ))}
              </ul>
            )}

            {result.challenge_sources?.length > 0 && (
              <div>
                <div className="text-[10px] uppercase text-slate-500 font-semibold mb-1">
                  Grandpa's Sources ({result.challenge_sources.length})
                </div>
                {result.challenge_sources.slice(0, 3).map((src, i) => (
                  <a key={i} href={src.url} target="_blank" rel="noreferrer"
                     className="block text-xs text-indigo-600 hover:underline bg-white px-2.5 py-1.5 rounded-lg border border-slate-100 truncate mb-1">
                    ↗ {src.title}
                  </a>
                ))}
              </div>
            )}

            <button onClick={() => runDevilsAdvocate(agent)}
                    className="w-full text-xs font-semibold px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 transition">
              🔄 Ask Grandpa Again
            </button>
          </div>
        )}
      </div>
    );
  };

  const ExpertCard = ({ agent, idx }) => {
    const expanded = expandedCards[idx];
    return (
      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-5 sm:p-6 space-y-4 flex flex-col">
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-3 min-w-0 flex-1">
            <span className="text-2xl">{agentIcon(agent.agent_name)}</span>
            <h4 className="text-[15px] font-bold text-slate-900 truncate">{displayAgentName(agent.agent_name)}</h4>
          </div>
          <BadgePill verdict={agent.verdict} small />
        </div>

        <p className={`text-[14.5px] text-slate-700 leading-relaxed ${!expanded ? "line-clamp-3" : ""}`}>
          {agent.reasoning}
        </p>

        {expanded && (
          <div className="space-y-4 pt-1 border-t border-slate-200">
            <div className="grid grid-cols-2 gap-3 pt-3">
              <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
                <div className="text-[10px] uppercase text-slate-500 font-semibold tracking-wide">Confidence</div>
                <div className="text-lg font-bold text-slate-900 mt-0.5">{Math.round(agent.confidence * 100)}%</div>
              </div>
              {agent.model_id && (
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-200">
                  <div className="text-[10px] uppercase text-slate-500 font-semibold tracking-wide">Model</div>
                  <div className="text-sm font-bold text-slate-700 mt-0.5 truncate" title={agent.model_id}>
                    {agent.model_id}
                  </div>
                </div>
              )}
            </div>

            <div className="bg-slate-50/60 p-3 rounded-xl border border-slate-100">
              <div className="text-[10px] uppercase text-slate-500 font-semibold mb-1">Expert Persona</div>
              <p className="text-xs text-slate-600 leading-relaxed">{agent.persona}</p>
            </div>

            <GrandpaChallenge agent={agent} />
          </div>
        )}

        <button onClick={() => toggleCard(idx)}
                className="flex items-center gap-2 text-indigo-600 hover:text-indigo-700 text-sm font-semibold transition w-fit mt-auto">
          {expanded ? <>Read less <span className="text-xs">⌃</span></>
                    : <>Read more <span className="text-xs">⌄</span></>}
        </button>
      </div>
    );
  };

  // ================ RESULTS VIEW ================
  if (result) {
    const vs = getVerdictStyles(result.final_verdict, result.is_contested);
    const agents = result.agents || [];
    const agreeCount = agents.filter(a =>
      a.verdict === result.final_verdict ||
      (a.verdict === "True" && result.final_verdict === "Mostly True")
    ).length;
    const totalScore = agents.reduce((acc, a) => acc + (a.confidence || 0), 0);

    return (
      <div className="min-h-screen bg-white text-slate-900 flex flex-col antialiased">
        <div className="sticky top-0 z-50 bg-white/90 backdrop-blur-sm border-b border-slate-200">
          <div className="max-w-5xl mx-auto px-4 sm:px-6 py-3.5 flex items-center justify-between">
            <button
              onClick={() => { setResult(null); setClaim(""); resetResultState(); }}
              className="flex items-center gap-2 text-slate-900 hover:text-indigo-600 font-semibold text-[15px] transition">
              <span className="text-lg">←</span> New Check
            </button>
            <div className="flex items-center gap-3">
              <button
                onClick={() => setShowProofDetails(s => !s)}
                className={`flex items-center gap-1.5 px-4 py-2 rounded-xl border text-sm font-medium transition ${
                  showProofDetails
                    ? "bg-indigo-50 text-indigo-700 border-indigo-200"
                    : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50"
                }`}>
                📄 Proof Details
              </button>
              <button
                onClick={() => setActiveTab(activeTab === "history" ? "checker" : "history")}
                className="flex items-center gap-1.5 px-4 py-2 rounded-xl border border-slate-200 text-slate-700 text-sm font-medium hover:bg-slate-50 transition">
                📊 History
              </button>
            </div>
          </div>
        </div>

        <main className="max-w-5xl mx-auto w-full px-4 sm:px-6 py-6 sm:py-10 flex-1 space-y-6">
          {activeTab === "history" && (
            <div className="bg-slate-50 border border-slate-200 rounded-2xl p-5 space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-base font-bold text-slate-900">📜 Check History</h3>
                <button onClick={() => setActiveTab("checker")}
                        className="text-xs text-slate-500 hover:text-slate-700 font-medium">
                  Close ✕
                </button>
              </div>
              <div className="space-y-3 max-h-[400px] overflow-y-auto">
                {history.length === 0
                  ? <p className="text-sm text-slate-500 italic py-4 text-center">No history yet.</p>
                  : history.map(item => <HistoryItem key={item.id} item={item} />)}
              </div>
            </div>
          )}

          {/* Claim + Verdict */}
          <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6 sm:p-8 space-y-6">
            <div>
              <div className="text-sm font-medium text-slate-500 mb-1.5">Claim</div>
              <h2 className="text-xl sm:text-2xl font-bold text-slate-900 leading-snug">"{result.claim}"</h2>
            </div>

            <div className="flex flex-col md:flex-row md:items-center gap-5">
              <div className={`flex items-center gap-4 px-5 sm:px-6 py-4 sm:py-5 rounded-2xl border-2 ${vs.pillBg} ${vs.pillBorder} flex-1`}>
                <div className={`h-11 w-11 sm:h-12 sm:w-12 rounded-full ${vs.pillIcon} flex items-center justify-center flex-shrink-0`}>
                  <span className="text-xl sm:text-2xl font-black">{vs.icon}</span>
                </div>
                <div className={`text-2xl sm:text-3xl font-black tracking-tight ${vs.pillText}`}>{vs.short}</div>
              </div>

              <div className="md:w-64 space-y-2">
                <div className="flex items-end justify-between">
                  <span className="text-sm font-medium text-slate-600">Confidence</span>
                  <span className="text-2xl font-bold text-slate-900">{Math.round(result.overall_confidence * 100)}%</span>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-2.5 overflow-hidden">
                  <div className="h-2.5 rounded-full bg-indigo-500"
                       style={{ width: `${Math.round(result.overall_confidence * 100)}%` }}></div>
                </div>
              </div>
            </div>

            <div className="flex flex-wrap items-center justify-between gap-4 pt-2">
              <p className="text-base font-semibold text-slate-800">
                {agreeCount} out of {agents.length} experts say this is{" "}
                <span className={vs.pillText}>{result.final_verdict.toLowerCase()}</span>.
              </p>
              <p className="text-sm font-medium text-slate-600">
                Total Score: <span className="font-bold text-slate-900">{totalScore.toFixed(2)}</span> / {agents.length.toFixed(2)}
              </p>
            </div>

            {showProofDetails && (
              <div className="mt-4 pt-5 border-t border-slate-200">
                <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-3">
                  <p className="text-sm">
                    <span className="font-semibold text-slate-700">Executive Summary: </span>
                    <span className="text-slate-700">{result.consensus_summary}</span>
                  </p>
                  <div className="flex flex-wrap items-center gap-3 text-xs">
                    <div className="flex items-center gap-1.5 text-slate-600">
                      ⛓️ <span className="font-semibold">On-Chain Proof:</span>
                      <code className="bg-white px-2 py-0.5 rounded border border-slate-200 text-indigo-600">
                        {result.blockchain_tx
                          ? result.blockchain_tx.slice(0, 16) + "..." + result.blockchain_tx.slice(-10)
                          : "Local Proof"}
                      </code>
                    </div>
                    {result.blockchain_tx && (
                      <a href={`https://sepolia.etherscan.io/tx/${result.blockchain_tx}`}
                         target="_blank" rel="noreferrer"
                         className="px-2.5 py-1 rounded-lg bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 font-semibold transition">
                        Verify on Explorer ↗
                      </a>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Checklist */}
          <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6 sm:p-8 space-y-5">
            <div>
              <h3 className="text-lg font-bold text-slate-900">Agent Verification Checklist</h3>
              <div className="w-full h-px bg-slate-200 mt-3"></div>
            </div>

            <div className="space-y-4">
              {agents.map((a, i) => (
                <div key={i} className="flex items-center justify-between gap-3">
                  <div className="flex items-center gap-4 flex-1 min-w-0">
                    <div className="text-2xl flex-shrink-0">{agentIcon(a.agent_name)}</div>
                    <span className="text-[15px] font-semibold text-slate-800 truncate">{displayAgentName(a.agent_name)}</span>
                  </div>
                  <div className="flex items-center gap-2 flex-shrink-0">
                    <div className="h-6 w-6 rounded-full bg-emerald-500 flex items-center justify-center shadow-sm">
                      <span className="text-white text-[12px] font-black">✓</span>
                    </div>
                    <span className="text-sm font-semibold text-emerald-700">Completed</span>
                  </div>
                </div>
              ))}
            </div>

            <div className="w-full h-px bg-slate-200"></div>

            <div className="flex items-center justify-between gap-3 pt-1">
              <span className="text-base font-semibold text-slate-800">Overall Status</span>
              <span className="px-4 py-1.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-sm font-bold">
                All agents completed
              </span>
            </div>
          </div>

          {/* Expert cards */}
          <div className="space-y-5">
            <h3 className="text-xl font-bold text-slate-900">What the Experts Say</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              {agents.map((a, i) => <ExpertCard key={i} agent={a} idx={i} />)}
            </div>
          </div>

          {/* Bottom line */}
          <div className="bg-indigo-50/70 border-2 border-indigo-100 rounded-2xl p-5 sm:p-6 flex flex-col sm:flex-row items-start sm:items-center gap-4">
            <div className="h-10 w-10 rounded-full bg-white border-2 border-indigo-200 flex items-center justify-center flex-shrink-0 shadow-sm">
              <span className="text-indigo-600 text-lg font-black">ⓘ</span>
            </div>
            <div className="flex-1 min-w-0">
              <span className="text-[15px] font-bold text-slate-900">Bottom Line:&nbsp;&nbsp;</span>
              <span className="text-[15px] font-semibold text-indigo-700 leading-relaxed">
                {result.consensus_summary}
              </span>
            </div>
          </div>

          {/* Sources */}
          {result.sources?.length > 0 && (
            <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6 sm:p-8 space-y-4">
              <h3 className="text-base font-bold text-slate-900">
                📚 Grounding Sources ({result.sources.length})
              </h3>
              <div className="space-y-3">
                {result.sources.map((src, i) => (
                  <div key={i} className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                    <a href={src.url} target="_blank" rel="noreferrer"
                       className="text-sm font-semibold text-indigo-600 hover:underline">
                      [{i + 1}] {src.title} ↗
                    </a>
                    <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">{src.snippet}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </main>

        <footer className="border-t border-slate-100 bg-slate-50 py-5 text-center text-xs text-slate-500">
          VeritasNet Fact-Checking Network
        </footer>
      </div>
    );
  }

  // ================ INPUT / LOADING / ERROR VIEWS ================
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-indigo-50/40 text-slate-900 flex flex-col antialiased">
      <header className="border-b border-slate-200 bg-white/70 sticky top-0 z-50 backdrop-blur-md">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-3.5 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center shadow-md shadow-indigo-500/20">
              <span className="text-xl">🛡️</span>
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight text-slate-900 flex items-center gap-2">
                VeritasNet
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700 font-semibold border border-indigo-200">
                  Decentralized Fact-Check Network
                </span>
              </h1>
              <p className="text-xs text-slate-500">GenAI Consensus Engine & On-Chain Proof Registry</p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => setActiveTab("checker")}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition ${
                activeTab === "checker"
                  ? "bg-indigo-600 text-white shadow"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
              }`}>
              ⚡ New Check
            </button>
            <button
              onClick={() => setActiveTab(activeTab === "history" ? "checker" : "history")}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition flex items-center gap-1.5 ${
                activeTab === "history"
                  ? "bg-indigo-600 text-white shadow"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-100"
              }`}>
              📜 History
              {history.length > 0 && (
                <span className="ml-1 px-1.5 py-0.2 text-[10px] rounded-full bg-slate-200 text-slate-700">
                  {history.length}
                </span>
              )}
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 sm:px-6 py-8 sm:py-12 flex-1 w-full">
        {activeTab === "checker" ? (
          <div className="space-y-8">
            <div className="bg-white border border-slate-200 rounded-2xl shadow-sm p-6 sm:p-8">
              <div className="max-w-3xl">
                <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight mb-2">
                  Submit Claim for Multi-Agent Consensus
                </h2>
                <p className="text-sm text-slate-600 mb-6">
                  Our system retrieves live search evidence, queries 4 independent domain-specialized AI agents in parallel, computes a confidence-weighted consensus, and anchors a cryptographic proof.
                </p>
              </div>

              <form onSubmit={(e) => { e.preventDefault(); handleFactCheck(); }} className="space-y-4">
                <textarea
                  rows="3"
                  value={claim}
                  onChange={(e) => setClaim(e.target.value)}
                  placeholder="Paste a viral headline, claim, or policy statement to verify..."
                  className="w-full bg-white border border-slate-300 rounded-xl px-4 py-3 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                />

                <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
                  <div className="flex flex-wrap items-center gap-1.5">
                    <span className="text-xs text-slate-500 font-semibold mr-1">Quick Try:</span>
                    {SAMPLE_CLAIMS.slice(0, 3).map((sc, i) => (
                      <button
                        key={i} type="button"
                        onClick={() => { setClaim(sc); handleFactCheck(sc); }}
                        className="text-[11px] px-2.5 py-1 rounded-md bg-slate-100 hover:bg-indigo-50 text-slate-700 hover:text-indigo-700 border border-slate-200 transition truncate max-w-[220px]"
                        title={sc}>
                        {sc}
                      </button>
                    ))}
                  </div>

                  <button
                    type="submit"
                    disabled={loading || !claim.trim()}
                    className="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-sm font-bold shadow-lg shadow-indigo-600/20 transition flex items-center justify-center gap-2">
                    {loading ? "Analyzing Network..." : "⚡ Verify Claim"}
                  </button>
                </div>
              </form>
            </div>

            {loading && (
              <div className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 text-center space-y-5 shadow-sm">
                <div className="inline-flex items-center gap-2.5 px-4 py-2 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200 text-sm font-semibold">
                  <span className="animate-spin">⏳</span>
                  Decentralized Multi-Agent Consensus in Progress...
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 max-w-3xl mx-auto text-xs font-semibold">
                  {LOADING_STEPS.map((s, i) => (
                    <div key={i}
                         className={`p-3 rounded-xl border transition ${
                           activeStep > i
                             ? "bg-indigo-50 border-indigo-300 text-indigo-700 shadow-sm"
                             : "bg-slate-50 border-slate-200 text-slate-400"
                         }`}>
                      <div className="text-lg mb-1">{s.icon}</div>
                      {s.label}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {error && (
              <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm">
                {error}
              </div>
            )}
          </div>
        ) : (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-slate-900">Check History</h2>
              <button
                onClick={() => setActiveTab("checker")}
                className="px-4 py-2 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-sm font-semibold text-slate-700 transition">
                ← New Check
              </button>
            </div>
            <div className="space-y-4">
              {history.length === 0
                ? <div className="bg-white border border-slate-200 rounded-2xl p-10 text-center">
                    <p className="text-slate-500">No history yet. Verify your first claim!</p>
                  </div>
                : history.map(item => <HistoryItem key={item.id} item={item} />)}
            </div>
          </div>
        )}
      </main>

      <footer className="border-t border-slate-100 bg-white py-5 text-center text-xs text-slate-500">
        VeritasNet Fact-Checking Network
      </footer>
    </div>
  );
}
