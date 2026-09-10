# 🛡️ Uncle-Factz

> *"Beta, I read it on WhatsApp, so it must be true."*
> — every family group, probably

We've all got one. The uncle who forwards a 480p video at 11pm captioned
"BREAKING NEWS 🚨🚨" and refuses to believe it's fake even when Google
disagrees with him. **Uncle-Factz** is what happens when you actually
give that uncle a team of AI relatives who go check the facts before he
hits forward.

Solving the *"Decentralized
Fact-Checking Network with GenAI Consensus"* problem statement, minus
the part where it takes six months and a research lab to build.

---

## 🤔 The Problem, Minus the Jargon

A claim shows up online. Something like:

> "This new government policy will reduce electricity prices by 50%."

Is it true? Nobody knows. A human fact-checker *could* look into it, but
by the time they do, it's already been forwarded to 40 WhatsApp groups
and become "common knowledge." Uncle-Factz exists to close that gap —
give a claim, get a fast, evidence-backed, honestly-uncertain-when-it-
should-be verdict, with a paper trail nobody can quietly edit later.

---

## 👨‍👩‍👧‍👦 Meet the Family

Instead of trusting one AI's opinion (risky — even AI has blind spots),
Uncle-Factz sends every claim to a family meeting. Four uncles
specialize in different topics, argue it out, and Grandpa has the final
say on whether they actually agree.

| Family Member | Real Job | Personality |
|---|---|---|
| 🔬 **Scientific Uncle** | Science & research claims | The one who actually reads the study instead of just the headline |
| 🏛️ **Political Uncle** | Political & policy claims | Debates everything, trusts nothing, cites sources anyway |
| 🩺 **Health Uncle** | Medical & health claims | Will not let a home remedy claim slide without evidence |
| 🧠 **General Uncle** | Everything else | The reasonable one who handles what nobody else specializes in |
| 👴 **Grandpa** | Fact-checker & devil's advocate | Has seen every trend come and go. If the family agrees too easily, Grandpa gets suspicious. If the evidence is thin, Grandpa says so — loudly, and honestly |

Each uncle independently researches the claim and gives their
own verdict — True, Mostly True, False, or "I don't have enough to say."
**Grandpa's job is different**: he doesn't just vote, he checks whether
the *rest of the family's votes actually hold up together*. If they're
united, the claim gets a clean verdict. If they're split, Grandpa isn't
going to pretend there's a consensus that doesn't exist — the claim
gets marked **Contested**, honestly, instead of forcing a fake agreement.

---

## ⚙️ How a Claim Actually Gets Checked

1. **You submit a claim** — paste a headline, a forward, whatever's bugging you.
2. **The family does its homework** — real sources get pulled from the
   web so nobody's just guessing from memory.
3. **Enough evidence?** If not, Grandpa stops the meeting early and says
   so — no evidence, no verdict pretending to be confident.
4. **The four relatives weigh in** — independently, in parallel, each
   from their own angle.
5. **Grandpa checks if they actually agree.** Majority + confidence
   score = a real verdict. Split opinions = **Contested**, said out loud.
6. **The verdict gets written to the blockchain** — a Solidity smart
   contract on a public testnet stores a hash of the claim, verdict, and
   evidence, so once Grandpa's said it, nobody — not even us — can
   quietly go back and change it.
7. **You see the result** — the verdict in plain English, what each
   family member thought, the sources, and a link to the public,
   tamper-proof record.

---

## 🧰 Built With

| Layer | Tech |
|---|---|
| Frontend | React (Vite) + Tailwind |
| Backend | Python, FastAPI |
| AI reasoning | Groq (LLM API) — one model, four personas |
| Evidence retrieval | Tavily Search API (RAG-style grounding) |
| Blockchain | Solidity + Hardhat → deployed to a public testnet (Sepolia / Polygon Amoy) |
| Database | SQLite |

---

## 🚀 Running It Locally

```bash
cd Uncle-Factz
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

You'll need API keys for your LLM provider and Tavily — drop them in a
`.env` file (see `.env.example`). Don't commit that file. Grandpa will
find out and he will not be happy.

---

## 🧪 Why It's a Simplified Version (Being Honest About It)

The original problem statement asks for four *separately trained and
fine-tuned* models — one real specialist per family member — plus full
blockchain infrastructure. That's genuinely a research-lab-scale
project. Uncle-Factz keeps the *spirit* of it achievable for a
hackathon:

- **One LLM (via Groq) playing all four family members**, switched
  between personas with different prompts, instead of four separately
  fine-tuned models. Groq's speed is what makes running four "agents"
  per claim feel instant instead of a long wait.
- A minimal Solidity contract storing verdict hashes on a testnet —
  real tamper-evidence, not yet a fully distributed network of
  independent validators.
- Consensus logic that's simple enough to explain in one sentence, on
  purpose, so nobody has to just trust a black box.

### Where we'd take it next

**The AI side:** swap the single-LLM-with-personas setup for genuinely
separate, fine-tuned models per uncle — a Scientific Uncle that's
actually trained on scientific literature, a Health Uncle trained on
medical corpora, and so on. That's what turns this from "one generalist
wearing four hats" into what the original problem statement actually
asked for, and it's the difference between a hackathon demo and
something ready for the masses to rely on daily.

**The blockchain side:** right now, Uncle-Factz proves a verdict
*hasn't been quietly changed* — but it doesn't yet prove the verdict was
*fair* in the first place. A few upgrades worth exploring:
- **Move from testnet to a real, low-fee chain** (like Polygon mainnet)
  so verdicts are permanently public, not just for the demo.
- **Let the family "vote" on-chain**, not just store the final result —
  so anyone can independently verify that Scientific Uncle and Health
  Uncle actually said what the app claims they said, not just trust the
  backend's word for it.
- **A reputation system for each uncle**, stored on-chain,
  tracking how often each one has been right over time — so if
  Political Uncle turns out to be consistently biased, that's visible
  and can be weighted down in future consensus rounds, publicly and
  transparently, not quietly patched in a private database.
- **Decentralize who runs the fact-checking itself** — right now, one
  team's backend calls the LLMs and writes to the chain. A more mature
  version would let multiple independent operators run the same
  pipeline and cross-check each other, which is what "decentralized"
  really means in the original problem statement, not just "the storage
  happens to be on a blockchain."

Grandpa's already convinced that in this future version, he'd still be
right most often. We'll let the reputation system decide that one.

---

*Uncle-Factz — because someone in the family has to check before it gets forwarded.*
