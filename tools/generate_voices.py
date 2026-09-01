"""Generate neural MP3 voiceovers for every auto-typed SENTINEL line."""
import asyncio
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "voice"
OUT.mkdir(parents=True, exist_ok=True)

# Elena: calm British authority. Marcus: clear British male.
# Danish: South-Asian English (closest neural match for a Pakistani speaker in English).
VOICES = {
    "elena": "en-GB-SoniaNeural",
    "marcus": "en-GB-RyanNeural",
    "danish": "en-IN-PrabhatNeural",
}

LINES = [
    ("01-intro-elena.mp3", "elena",
     "You are the last control before the money moves. Everything upstream of you is paperwork. Everything downstream is somebody else's problem."),
    ("02-intro-marcus.mp3", "marcus",
     "Four modules. Onboard a customer who does not want to be onboarded properly, learn the red-flag families by sight, work a live transaction queue, and drill the thresholds until they are reflex."),
    ("03-onboard-brief-elena-1.mp3", "elena",
     "There is a new relationship waiting at the counter. Your job is customer due diligence: identify them, verify the identity against a reliable source, establish who really owns the business, and then decide how much scrutiny this file needs."),
    ("04-onboard-brief-elena-2.mp3", "elena",
     "The customer will be helpful right up to the moment you ask something inconvenient. Remember that rapport is not what the file is judged on."),
    ("05-onboard-danish-identify.mp3", "danish",
     "Good morning. I want to open a current account for my company — Raza Trading Private Limited. I have the incorporation certificate here, and my own CNIC."),
    ("06-onboard-danish-verify.mp3", "danish",
     "Here is the CNIC. Look — the photo is clearly me. That's enough, isn't it? I'm in a bit of a rush, I have a flight this evening."),
    ("07-onboard-danish-ownership-1.mp3", "danish",
     "The company shares? I hold 15%. My brother-in-law holds most of it — around 60% — but he's a silent partner, he won't be involved in the account at all. He asked me to handle all of it."),
    ("08-onboard-danish-ownership-2.mp3", "danish",
     "Fine, fine. His name is Adnan Sheikh. He is... he serves as an advisor and his father is the provincial minister for industries. Is that a problem? Everything is completely legitimate."),
    ("09-onboard-danish-risk.mp3", "danish",
     "So can we finish this today? I have already told my supplier the account would be ready. Expected turnover — let's say around 5 million a month to be safe."),
    ("10-onboard-danish-edd.mp3", "danish",
     "Enhanced due diligence? What does that involve? I have given you everything already."),
    ("11-onboard-danish-tipping.mp3", "danish",
     "Look — between us, is my account going to get reported to someone? I have heard banks report people. If anything gets filed on me I want to know about it first."),
    ("12-onboard-danish-monitor.mp3", "danish",
     "All right. Send it to your manager then. How will you handle the account once it opens?"),
    ("13-onboard-danish-restricted.mp3", "danish",
     "Why is my account restricted? I deposited 4.8 million this week and now nothing is going through. You told me everything was fine."),
    ("14-onboard-danish-whatnext.mp3", "danish",
     "So what happens now? Am I going to lose the account?"),
    ("15-radar-brief-marcus-1.mp3", "marcus",
     "Five red-flag families, A through E, straight out of Annexure-II. If you cannot name the family an observation belongs to, you cannot reach for the right follow-up question."),
    ("16-radar-brief-marcus-2.mp3", "marcus",
     "Ten observations, eighteen seconds each. Answer fast and the combo multiplier stays alive."),
    ("17-console-brief-elena-1.mp3", "elena",
     "This is the live queue. Every case in it is a real transaction waiting on a disposition from you: clear it, flag it, or escalate it."),
    ("18-console-brief-elena-2.mp3", "elena",
     "Flagging is not enough on its own. You have to name the indicator you are acting on, because an STR has to record the basis for the decision — and so does a decision not to file one."),
    ("19-thresholds-brief-elena-1.mp3", "elena",
     "Thresholds are the part you cannot look up mid-conversation. Two million rupees in cash triggers a CTR whether or not anything looks wrong. Five hundred thousand from a walk-in triggers identity verification. An STR has no floor at all."),
    ("20-thresholds-brief-elena-2.mp3", "elena",
     "Twelve drills, twenty-two seconds each. Where more than one obligation could apply, the higher duty wins."),
]


async def one(name, speaker, text):
    path = OUT / name
    comm = edge_tts.Communicate(text, VOICES[speaker], rate="-5%")
    await comm.save(str(path))
    print(f"  {name}  ({path.stat().st_size // 1024} KB)")


async def main():
    print(f"Writing {len(LINES)} files to {OUT}")
    for name, speaker, text in LINES:
        await one(name, speaker, text)
    print("done")


if __name__ == "__main__":
    asyncio.run(main())
