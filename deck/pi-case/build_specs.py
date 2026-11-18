import json, os
SRC = "Source: case study brief (Nov 2026); P&I proposal."
T = "executive"
slides = []
def add(name, spec):
    spec.setdefault("theme", T)
    slides.append((name, spec))

add("01-cover", {"pattern":"cover","title":"Performance & Intelligence","subtitle":"Turning domain data into decisions: the first six months of Level Up Advisory","presenter":"PM proposal, P&I squad","date":"November 2026","classification":"Internal — case study",
 "notes":"I'll walk you through how I would run P&I from 1 December: what we start with, why, how we measure success, and how we make it stick. Ten minutes, then questions."})

add("02-users", {"pattern":"summary_strip","headline":"P&I serves three users, and one is AI",
 "subline":"Who P&I serves, what they need, and which product serves them",
 "blocks":[
  {"metric":"Decide","claim":"Squads, leadership, Finance, council","proof":"Need one truth, new opportunities and proof of value.","implication":"Reporting, insights, opportunities"},
  {"metric":"Act","claim":"Clients in George, bankers in FIT+","proof":"Need the right next step and the right message.","implication":"Brain, segments, at-risk list, personas"},
  {"metric":"AI","claim":"Brain, agentic CRM, AI assistants","proof":"Need data and rules they can read, plus guardrails.","implication":"Metric API, decision log, evaluation harness"}],
 "annotation":"Design principle: one truth for people and machines, and any model can be swapped.",
 "page_number":2,"source":"Source: case study brief; P&I proposal.",
 "notes":["Before priorities, who are we building for? Three users.","First, people who decide: the squads, domain leadership, Finance and the concept council. They need one truth, opportunities and proof of value. We serve them with reporting, insights and regular opportunity finding.","Second, people who act: clients in George and bankers in FIT+ and at branches. They need the right next step and the right message. That is Brain, the segments, the at-risk list, and personas, which test the message before it reaches real clients.","Third, and new: AI itself. Brain, agentic CRM and AI assistants consume our data too. So everything we build must be readable by machines: metric definitions available through an API, every recommendation and its outcome logged, and an evaluation harness so we can test quality and compliance and switch models without rebuilding. These are design principles for how we build the top 5, not an extra workstream."]})

add("03-metrics", {"pattern":"kpi_scorecard","headline":"North Star must grow 4.5x, clients only 2.1x",
 "subline":"Key metrics from the brief · today vs target",
 "columns":2,
 "metrics":[
  {"label":"NORTH STAR: NET LEVEL-UPS","value":"28k","target":"125k by 30 Jun","trend":"x4.5","status":"risk"},
  {"label":"CLIENTS IN PROGRAMME","value":"598k","target":"1.25M by 30 Jun","trend":"x2.1"},
  {"label":"LEVEL DROPS SINCE 1 OCT","value":"22.6k","trend":"balance-driven","status":"risk"},
  {"label":"CM3 PROFITABILITY","value":"Not yet","trend":"per Finance","status":"risk"}],
 "annotation":"Growth must come from existing clients climbing faster and dropping less.",
 "page_number":3,"source":"Source: case study brief; North Star counted since the silent launch.",
 "notes":["The key numbers from the brief. The North Star must grow 4.5 times, from 28 thousand to 125 thousand net level-ups, while the client base only doubles. So the share of clients who level up must more than double, from about 5 to 10 percent.","22.6 thousand clients dropped a level since October, largely because points follow account balances, and the savings rate moves with the level.","And Finance says the programme is not yet profitable. For share of wallet and value-for-money NPS we have targets but no baseline, which is why one source of truth comes first."]})

add("04-pilot-gap", {"pattern":"before_after","headline":"Rollout gets half of the pilot's results",
 "subline":"Pilot with targeted communication vs rollout today, % of clients",
 "before_label":"Pilot","after_label":"Rollout",
 "unit":"%",
 "pairs":[
  {"label":"Enrolled","before":24.6,"after":13.0,"before_text":"24.6%","after_text":"13%","delta_text":"−11.6 pp (53% of pilot)"},
  {"label":"Chose a reward","before":63.0,"after":34.3,"before_text":"63%","after_text":"34.3%","delta_text":"−28.7 pp (54% of pilot)"}],
 "annotation":"The pilot playbook is the cheapest Go Big lever; P2 finds what made the difference.",
 "page_number":4,"source":"Source: case study brief; rollout enrolment = silent start (13%), reward choice = rollout today (34.3%).",
 "notes":["Same programme, two very different results. With targeted communication in the Hradec Králové pilot, 24.6 percent of clients enrolled; with the silent start only 13. In the pilot 63 percent chose a reward; in the rollout today 34.","On both measures the rollout gets about half of what the pilot did. That is not a product problem, it is execution: communication, timing, how the reward is presented.","So the cheapest lever for Go Big is to understand exactly what made the pilot work and copy it. That is priority 3. One caveat I will check: whether pilot clients were selected differently."]})

add("04-criteria", {"pattern":"benchmark_table","headline":"Five criteria decide what P&I does first",
 "subline":"Q2 · Gate first: does P&I own it? Then score each area 1–3 per criterion",
 "columns":["Question","Information"],
 "rows":[
  {"label":"North Star","values":["Lifts net level-ups?","Level, drop and pilot data"]},
  {"label":"Proof of value","values":["Helps prove SoW and CM3?","Finance CM3 method"]},
  {"label":"Cost of delay","values":["Does delay hurt Go Big?","Go Big plan and calendar"]},
  {"label":"Unlocks others","values":["Does other work need it?","Dependency map, squads"]},
  {"label":"Feasibility","values":["Can we deliver it now?","Team skills, partner plans"]}],
 "annotation":"The same criteria rank every new request, not just these 30 areas.",
 "page_number":5,"source":"Source: P&I prioritisation framework; scores validated with squads in week 3.",
 "notes":["How I decided. First one gate: does P&I own the outcome? If another squad or the concept council owns it, like the savings calculator or new scoring rules, P&I supplies evidence but does not lead.","Then every area is scored one to three on five criteria. North Star impact: does it add net level-ups or stop drops? Proof of value: does it help us show SoW and CM3 to Finance? Cost of delay: does waiting past Go Big cost us? Unlocks others: does other work depend on it? And feasibility: can our team and our partner teams deliver it now?","Each criterion has a source: the level and drop data, Finance's CM3 method, the Go Big plan, interviews with the squads, and partner capacity plans. I validate the scores with the squads in week three.","And this is not a one-off: the same criteria rank every new request that comes to P&I."]})

add("02-answer", {"pattern":"benchmark_table","headline":"Four building blocks, with Brain built on top",
 "subline":"Q1 · Five areas from the brief: P1–P4 feed Brain (P5)",
 "columns":["Why","Delivers","Depends on","Ready"],
 "rows":[
  {"label":"P1 Metric truth (1)","values":["No baseline, noisy drops","One clean North Star","Finance, all squads","Jan"]},
  {"label":"P2 Pilot lessons (18)","values":["Rollout at half of pilot","What made pilot work","Pilot owners","Dec"]},
  {"label":"P3 Segments (10)","values":["Go Big needs targets","Targets and triggers","DG&E campaigns","Mid-Jan"]},
  {"label":"P4 At-risk list (3)","values":["Drops cut savings rate","Weekly list for bankers","Bankéř squad, branches","Jan"]},
  {"label":"P5 Brain v1 (7)","values":["Longest lead time","One next step per client","Bankéř squad, George","FIT+ Mar"]}],
 "annotation":"P1–P4 are Brain's data and first rules; each ships with a holdout.",
 "page_number":6,"source":"Source: case study brief; numbers in brackets are the areas from the brief's list of 30.",
 "notes":["My five areas from the list: 1, 18, 10, 3 and 7. Four building blocks, and Brain built on top of them.","Area 1, one metric truth, because today we have targets for SoW and NPS but no baseline, and part of the 22.6 thousand drops is balance noise. It delivers one clean North Star, and the evidence the concept council needs to fix the rules. It needs Finance and all squads to agree.","Area 18, pilot lessons, because the rollout gets half of what the pilot did. Ready in December, so it shapes Go Big, and it is the first evidence of what actually moves clients.","Area 10, segments and triggers for Go Big, through Digital Growth and Engagement's campaigns. These become Brain's first rules.","Area 3, a weekly at-risk list for bankers: Brain's first next-best-action use case.","And area 7, Brain v1 itself, because it has the longest lead time: George goes through Vienna. We design it and the decision log in December, and it goes live in FIT+ in March, built from the four blocks. Every segment and list carries a holdout group, so we prove impact from day one."]})

add("07-roadmap", {"pattern":"gantt","headline":"Blocks land before Go Big, Brain in March",
 "subline":"P&I roadmap, December 2026 to June 2027",
 "periods":["Dec","Jan","Feb","Mar","Apr","May","Jun"],
 "bars":[
  {"label":"P1 Metric truth","start":0,"end":1,"highlight":True,"note":"foundation"},
  {"label":"P2 Pilot lessons","start":0,"end":0},
  {"label":"P3 Go Big segments","start":0,"end":1},
  {"label":"P4 At-risk list","start":1,"end":6,"note":"weekly, with holdout"},
  {"label":"P5 Brain v1","start":0,"end":6,"note":"design, FIT+ in Mar, then George"},
  {"label":"Rules evidence","start":0,"end":1,"note":"to council"},
  {"label":"Finance SoW / CM3","start":2,"end":6,"note":"monthly"},
  {"label":"Personas: Go Big test","start":0,"end":1,"note":"pre-test"},
  {"label":"Personas: validation","start":2,"end":3,"note":"vs holdouts"}],
 "gates":[{"label":"Go Big 1 Feb","period":1},{"label":"30 Jun","period":6}],
 "annotation":"P1 rests on one reporting lead and one data engineer; their time is the critical path.",
 "page_number":7,"source":"Source: P&I plan; dates depend on partner-team capacity.",
 "notes":["The four building blocks land before Go Big on 1 February. Pilot lessons in December feed the Go Big segments in January.","Brain v1 starts in December with design and the decision log, goes live in FIT+ in March on the rules from the segments and the at-risk model, then moves to George once Vienna capacity is secured. The rules evidence from P1 goes to the concept council in January. After Go Big the Finance report runs monthly. Personas pre-test the Go Big messages in January and are validated against the holdouts in February and March.","The critical path is P1: it rests on one reporting lead and one data engineer. Protecting their time is my first ask."]})

add("08-team", {"pattern":"benchmark_table","headline":"Six people cover the top 5 as personas wrap up",
 "subline":"P&I team allocation · AI engineers move from personas to modelling",
 "columns":["Dec–Jan","From Feb"],
 "rows":[
  {"label":"Data eng. + reporting","values":["P1 truth, dashboard","Finance report, Brain data"]},
  {"label":"AI engineer A","values":["P1 noise analysis, P2 pilot","Holdouts, experiments"]},
  {"label":"AI engineer B","values":["P3 segments (Klient)","P5 Brain rules"]},
  {"label":"AI engineer C","values":["P4 at-risk (Bankéř), P5","P5 Brain in FIT+"]},
  {"label":"AI engineer D","values":["Personas: Go Big pre-test","Persona validation"]}],
 "annotation":"Reporting is the thinnest skill; AI engineers learn the reporting stack in Q1.",
 "page_number":8,"source":"Source: planned team of six; personas project closing in the coming weeks.",
 "notes":["This is the real team: four AI engineers from the synthetic personas project, one reporting lead from financial health and one data engineer from Level Up.","The persona tool is nearly finished, so the AI engineers move onto the modelling work in the top 5: the noise analysis, pilot uplift, segments, the at-risk model and Brain itself. They are building Brain from day one.","One engineer finishes personas and uses them on Go Big. The thinnest skill is reporting: one person. That is a single point of failure, so the AI engineers learn the reporting stack in Q1."]})

add("09-missing", {"pattern":"bullet_list","headline":"The list lacks a way to prove what P&I changes",
 "subline":"Q3 · What I would add to the list, and why",
 "bullets":[
  {"text":"Experimentation framework with holdout groups","sub":["Without it, SoW and CM3 gains cannot be attributed"],"emphasis":True},
  {"text":"North Star driver tree and forecast","sub":["Enrolment x level-up rate minus drops: is 125k reachable?"]},
  {"text":"AI foundations: metric API, decision log, testing","sub":["Includes GDPR and AI Act checks before Brain scales"]},
  {"text":"Go Big monitoring in the first weeks","sub":["Volume doubles; data and drops must be watched daily"]}],
 "annotation":"All four run inside the top 5; none needs a separate team.",
 "page_number":9,"source":SRC,
 "notes":["Four things I would add to the list. First and most important: a way to prove impact. Holdout groups for every campaign and list; without them we will never convince Finance that SoW and CM3 moved because of us.","Second, a North Star driver tree: enrolment, level-up rate and drops. It tells us whether 125 thousand is reachable and which lever gets us there.","Third, the AI foundations from the users slide: metrics available through an API, every recommendation and its outcome logged, and testing, including GDPR and the AI Act, before Brain scales.","Fourth, monitoring in the first weeks of Go Big, when volume doubles. None of these needs a separate team; they are built into the top 5."]})

add("10-info", {"pattern":"benchmark_table","headline":"Five unknowns close within three weeks",
 "subline":"Q4 · What I still need to know, and how I will get it",
 "columns":["How I get it","By"],
 "rows":[
  {"label":"Balance drops","values":["Split drops by point type","Week 2"]},
  {"label":"Partner capacity","values":["Data eng., George, CRM planning","Week 2"]},
  {"label":"CM3 method","values":["Workshop with Finance","Week 3"]},
  {"label":"Pilot design","values":["Pilot owners and data","Week 3"]},
  {"label":"Squad needs","values":["Interviews: squads, council","Week 2"]}],
 "annotation":"Answers go back into the scoring; priorities are re-checked at the end of week 3.",
 "page_number":10,"source":SRC,
 "notes":["What I do not know yet, and how I close it. The biggest is how much of the drops is balance movement: that is a data decomposition my team can do in two weeks.","Then partner capacity: George in Vienna, FIT+, CRM, data engineering. I need their planning cycles, because our dependencies sit there.","Finance's CM3 method, the pilot design to check for selection bias, and what squads and branches actually need. By week 3 I re-run the scoring with real data."]})

add("11-kpis", {"pattern":"kpi_scorecard","headline":"P&I is judged by what others do with its output",
 "subline":"Squad KPIs per user type · targets set after the December baseline",
 "columns":3,
 "metrics":[
  {"label":"DECIDE: OUTPUTS ACTED ON","value":"≥70%","target":"decided within 2 weeks"},
  {"label":"ACT: EXTRA LEVEL-UPS","value":"≥10k","target":"vs holdout, by 30 Jun"},
  {"label":"AI: METRICS VIA API","value":"100%","target":"North Star, SoW, CM3"},
  {"label":"DECIDE: SQUAD SATISFACTION","value":"≥8/10","target":"quarterly survey"},
  {"label":"ACT: DROPS PREVENTED","value":"≥5k","target":"vs holdout, at-risk list"},
  {"label":"AI: MODEL SWAP TIME","value":"<1 week","target":"with tests passing"}],
 "annotation":"P&I contributes to the North Star; these KPIs measure that contribution.",
 "page_number":11,"source":"Source: proposed targets; illustrative until baselined in December.",
 "notes":["How I know if P&I succeeds. We recommend and squads decide, so we are judged on what others do with our work, not on how many reports we ship. One pair of KPIs per user type.","People who decide: at least 70 percent of our outputs lead to a decision within two weeks, and squads rate us 8 out of 10 or better.","People who act: extra level-ups and prevented drops, always measured against holdout groups, so we only claim what we caused. My proposal is at least 10 thousand and 5 thousand by 30 June.","AI: the North Star, SoW and CM3 are available through an API, and we can swap a model in under a week with tests passing.","Targets are proposals; I set them after the December baseline."]})

add("12-governance", {"pattern":"benchmark_table","headline":"Explicit rules keep the priorities alive",
 "subline":"Q5 · How the priorities happen and hold with many stakeholders",
 "columns":["How it works","Rhythm"],
 "rows":[
  {"label":"Stakeholders","values":["Domain lead sets order; council owns logic","Monthly forum"]},
  {"label":"Requests","values":["One intake, scored on the five criteria","Weekly triage"]},
  {"label":"Capacity","values":["60/25/15 split; partner capacity booked early","Quarterly planning"]},
  {"label":"Adoption","values":["Named contact per squad; outputs co-built","Ongoing"]},
  {"label":"Sustaining","values":["Track % capacity on top 5 and outputs used","Quarterly re-score"]}],
 "annotation":"New requests are welcome, but each one openly displaces another.",
 "page_number":12,"source":SRC,
 "notes":["How I make sure the priorities happen and hold. Five mechanisms, one for each part of the problem.","Many stakeholders: clear decision rights. The domain lead sets the order in a monthly forum, the concept council owns the logic of levels and points, and P&I recommends. So conflicts have a place to be decided, not argued in corridors.","Different requests: one intake, and every request is scored on the same five criteria as the top 5, in a weekly triage. The backlog is public, so everyone sees why something waits.","Limited capacity: 60 percent of our time on the priorities, 25 on requests, 15 buffer. What we need from George, FIT+ and CRM goes into their quarterly planning early, as agreed commitments.","Getting it used: each squad has a named contact in P&I, and we build outputs together with the squads, so they own them. Early wins by January earn the credibility to say no later.","Keeping it going: I track how much capacity really goes to the top 5 and how many outputs are acted on, and we re-score the priorities every quarter. A new request is always welcome, but it openly displaces something else."]})

add("06-loop", {"pattern":"process_flow","headline":"The top 5 is the first turn of a learning loop",
 "subline":"Beyond the brief · P&I vision: every turn makes the next decision better",
 "steps":[
  {"label":"Measure","detail":"One truth for people and AI","owner":"P1","duration":"Dec–Jan"},
  {"label":"Find","detail":"Pilot, segments, risks","owner":"P2–P4","duration":"Dec–Jan"},
  {"label":"Decide","detail":"Brain picks one next step","owner":"P5 Brain","duration":"From Mar"},
  {"label":"Act","detail":"Squads, bankers, campaigns","owner":"Squads","duration":"Feb+"},
  {"label":"Prove & learn","detail":"Holdouts feed back","owner":"P&I, Finance","duration":"By 30 Jun"}],
 "annotation":"After 30 June: Brain learns from its results, and the loop moves to other domains.",
 "page_number":13,"source":SRC,
 "notes":["Where this is heading. P&I is not a reporting team; it is a learning loop. Measure, find, decide, act, prove, and back to measure.","The top 5 builds the first turn: P1 measures, P2 to P4 find, and P5, Brain, decides from March. The squads, bankers and campaigns act; P&I recommends, they decide. Holdouts prove what worked and feed back into the next turn.","By 30 June the first full turn is complete. After that, Brain learns from the results of its own recommendations, and because the loop is built on one truth that people and AI can read, it can be copied to other domains of the bank."]})

add("13-closing", {"pattern":"closing","headline":"Three decisions let P&I start on 1 December",
 "takeaways":["Trusted numbers first: remove balance noise","Act before Go Big with pilot-proven segments","Holdouts let P&I prove value to Finance"],
 "next_steps":[
  {"action":"Confirm the top 5 priorities","owner":"Domain lead","timing":"This week"},
  {"action":"Protect P1 reporting and data eng.","owner":"Head of Product","timing":"By 1 Dec"},
  {"action":"Put balance rules on council agenda","owner":"Domain lead","timing":"January"}],
 "call_to_action":"Decision requested: confirm the top 5 and the capacity behind them.",
 "page_number":13,"source":SRC,
 "notes":"To wrap up: trusted numbers first, learn from the pilot, act before Go Big, and prove every step. I need three things from you: confirm the five priorities, protect the reporting lead and the data engineer for P1 while Level Up hands over their routine work, and put the balance-linked rules on the council agenda in January. Thank you, happy to take questions."})


add("14-backup-personas", {"pattern":"process_flow","headline":"Personas earn a wider role only if they predict Go Big",
 "subline":"Backup · Persona validation plan",
 "steps":[
  {"label":"Finish","detail":"Final touches on the tool","owner":"Eng. D","duration":"Dec"},
  {"label":"Build","detail":"Personas for P4 segments","owner":"Eng. D","duration":"Jan"},
  {"label":"Pre-test","detail":"Go Big messages","owner":"Eng. D, DG&E","duration":"Jan"},
  {"label":"Compare","detail":"Predicted vs holdout results","owner":"Eng. A, D","duration":"Feb–Mar"},
  {"label":"Decide","detail":"Scale to all campaigns?","owner":"Domain lead","duration":"End Mar"}],
 "highlight":3,
 "annotation":"Personas complement real client interviews; they never replace them.",
 "page_number":14,"source":SRC,
 "notes":["If asked about personas: the tool is nearly finished. We build personas for the Go Big segments, pre-test the messages in January, then compare what they predicted with what actually happened in the holdout groups.","Only if the predictions are close do we use personas to pre-test every campaign. Either way, they complement real client interviews, never replace them."]})

add("05-scoring", {"pattern":"heatmap","headline":"The top 5 score highest on the criteria",
 "subline":"Backup · leading areas scored 1 (low) to 3 (high) per criterion",
 "unit":"",
 "rows":["P1 Truth (1)","P2 Pilot (18)","P3 Segments (10)","P4 At-risk (3)","P5 Brain v1 (7)","New rules (9)","Finance report (5)","Personas (12)"],
 "columns":["North Star","Proof","Delay cost","Unlocks","Feasibility"],
 "values":[[2,3,3,3,3],[2,1,3,3,3],[3,1,3,2,2],[3,2,2,1,3],[3,2,3,2,2],[3,1,2,1,1],[1,3,1,1,2],[1,1,2,1,3]],
 "annotation":"New rules are the council's call; P1 gives it the evidence.",
 "page_number":16,"source":"Source: P&I judgement based on the brief; to be validated with squad leads in week 3.",
 "notes":["The leading areas scored on the five criteria. The top five are strongest on cost of delay and feasibility.","Brain scores high on cost of delay because George releases go through Vienna; with four AI engineers, it is feasible to start the design now.","New rules, area 9, would have big impact, but the concept council owns that decision, so P&I feeds it evidence through P1. The Finance report needs the one metric truth first, so it follows in February."]})

import re
slides=[(f"{i+1:02d}-"+re.sub(r"^\d+-","",n), s) for i,(n,s) in enumerate(slides)]
for i,(n,sp) in enumerate(slides):
    if "page_number" in sp: sp["page_number"]=i+1
os.makedirs("specs", exist_ok=True)
paths=[]
for n,s in slides:
    p=f"specs/{n}.json"; json.dump(s, open(p,"w"), ensure_ascii=False, indent=2); paths.append(p)
json.dump({"title":"Performance & Intelligence — P&I proposal","description":"P&I squad PM case study, Level Up Advisory","slides":paths}, open("deck.json","w"), indent=2)
