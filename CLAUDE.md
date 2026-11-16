# Daily Lecture: nightly runbook

This repo is Ronan's private podcast feed. Every night a scheduled task writes one lecture, renders it to audio, and publishes it here. GitHub Pages serves it at https://ronan-schultz.github.io/daily-lectures/feed.xml, and his podcast app downloads it before he wakes at about 4:30 AM Mountain.

This is a personal project. Never put any of it in SOF repos, buckets, or domains.

## The listener
Ronan is a QAMO (quantitative finance) undergrad at the University of Utah and co-founder of a quant fund. Assume a sophisticated, technical listener: don't over-explain basics, and go technical. Don't do lectures on trading or modelling internals; he does that daily. When explaining a formula, say variables out in words ("the speed squared over the speed of light squared"), never one-letter names. That is his explicit rule, and it matters even more in audio.

## Nightly steps
1. `sh tools/setup.sh` (installs Kokoro TTS and downloads the model from GitHub releases; Hugging Face is blocked).
2. Read `log.md`: feedback, backlog, past episodes and weak spots. Choose a topic that has not been done, honoring any feedback. Every few episodes, open with a 1-2 minute callback that re-teaches a weak spot from an earlier quiz before the new topic. Rotate categories so consecutive episodes differ.
3. Write the script to `scripts/NNN-slug.txt` (three-digit number, next in sequence).
   - About 3,000 words, which is about 20 minutes. 2,500 words came out at 17 minutes.
   - Spoken lecture style: a hook, a roadmap, 4-6 parts, a recap, then exactly 5 quiz questions read aloud at the end. Questions should test mechanisms and "why", not recall of numbers.
   - Write for the ear: spell out units and symbols ("microseconds", "ten to the minus nine"), keep numbers sparse and rounded, no lists or markdown, and separate paragraphs with blank lines (each paragraph is rendered separately).
   - Accuracy matters more than color. Only state specific figures or history you are confident in, and look up anything uncertain with web search. If a popular claim is oversimplified, say so and explain the real version; he liked that in episode 1.
4. Render: `python3 -I tools/render.py scripts/NNN-slug.txt episodes/NNN-slug.mp3 am_michael`. This takes about 1.7x real time on CPU (~35 min for 20 min of audio), so run it in the foreground with long timeouts, or in the background while polling, but do not end the turn before it finishes.
5. Add the entry to `episodes.json` (number, slug, title, date = today's date in Mountain time, a 1-2 sentence summary, and the 5 questions), then `python3 -I tools/build_feed.py`.
6. Add a row to the Episodes table in `log.md` (quiz result: "pending").
7. Commit and push to `main`: `git add -A && git commit -m "Episode NNN: title" && git -c push.negotiate=true push origin main`.
8. Send one short message with the title and the 5 questions, telling him he can reply here with his answers.

## When he replies with quiz answers (in that night's session)
Grade each answer honestly: right, half, or missed. Give the correct mechanism for anything incomplete, with no padding or flattery. Then update that episode's row in `log.md` (score and weak spots), add any feedback he gives to the Listener feedback section, and commit and push.

## Storage
MP3s are 48 kbps mono, about 7 MB each. When `episodes/` holds more than 30 MP3s, `git rm` the oldest ones (their scripts and log rows stay). The feed skips missing files automatically.
