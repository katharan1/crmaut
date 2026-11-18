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
 "subline":"Every metric in the brief · today vs 30 June 2027",
 "columns":3,
 "metrics":[
  {"label":"NORTH STAR: NET LEVEL-UPS","value":"28k","target":"125k by 30 Jun","trend":"x4.5","status":"risk"},
  {"label":"CLIENTS IN PROGRAMME","value":"598k","target":"1.25M by 30 Jun","trend":"x2.1"},
  {"label":"NORTH STAR / CLIENTS","value":"4.7%","target":"10% by 30 Jun","trend":"x2.1","status":"risk"},
  {"label":"LEVEL DROPS SINCE 1 OCT","value":"22.6k","trend":"balance-driven","status":"risk"},
  {"label":"ENROLMENT: PILOT","value":"24.6%","trend":"vs 13% silent"},
  {"label":"REWARD CHOSEN: ROLLOUT","value":"34.3%","trend":"vs 63% pilot","status":"risk"},
  {"label":"CM3 PROFITABILITY","value":"Not yet","trend":"per Finance","status":"risk"},
  {"label":"SHARE OF WALLET","value":"n/a","trend":"no baseline"},
  {"label":"VALUE-FOR-MONEY NPS","value":"n/a","trend":"no baseline"}],
 "annotation":"Growth must come from existing clients climbing faster and dropping less.",
 "page_number":3,"source":"Source: case study brief; North Star counted since the silent launch; share = North Star / clients.",
 "notes":["All the numbers from the brief on one page. Top row is the target: the North Star must grow 4.5 times, from 28 thousand to 125 thousand net level-ups, while the client base only doubles. So the share of clients who level up must more than double, from 4.7 to 10 percent.","Middle row is behaviour. 22.6 thousand clients dropped a level since October, largely because points follow account balances. The targeted pilot enrolled 24.6 percent against 13 percent at the silent start, and reward choice fell from 63 percent in the pilot to 34 in the rollout.","Bottom row is value. Finance says the programme is not yet profitable, and for share of wallet and value-for-money NPS the brief gives no baseline. That is exactly why one source of truth is my first priority."]})

add("02-answer", {"pattern":"summary_strip","headline":"P&I should make the numbers trustworthy before scaling AI",
 "subline":"The proposal in one page · Five priorities in three moves",
 "blocks":[
  {"metric":"Clarity","claim":"One truth, minus the noise","proof":"P1 One metric truth. P2 Evidence on balance-driven drops.","implication":"Everyone steers on the same, honest number."},
  {"metric":"Learn","claim":"Copy what already worked","proof":"P3 Why the pilot nearly doubled enrolment.","implication":"Go Big starts from a proven playbook."},
  {"metric":"Act","claim":"Give squads targets for Go Big","proof":"P4 Go Big segments. P5 Weekly at-risk list.","implication":"Every list carries a holdout, so impact is proven."}],
 "focus_block":0,"page_number":2,"source":SRC,
 "notes":"Here is the answer up front. Five priorities, grouped into three moves: clarity, learn, act. The thread through all of them: we cannot grow a North Star 4.5 times if we do not trust what it measures. Brain comes right after, on top of trusted data. Personas are already nearly finished; we use Go Big to validate them."})

add("03-situation", {"pattern":"summary_strip","headline":"The North Star must grow 4.5x on a base that is partly noise",
 "subline":"Three signals from the brief",
 "blocks":[
  {"metric":"4.5x","claim":"North Star gap","proof":"28k to 125k net level-ups by 30 June, while clients grow only 2.1x (598k to 1.25M).","implication":"Existing clients must climb faster and drop less."},
  {"metric":"22.6k","claim":"Level drops since 1 Oct","proof":"Balance-linked points make clients bounce across levels.","implication":"Part of the North Star is noise."},
  {"metric":"2x","claim":"Pilot vs silent start","proof":"Targeted communication: 24.6% vs 13% enrolment; 63% vs 34% reward choice.","implication":"Execution, not product, made the gap."}],
 "focus_block":1,"annotation":"Finance does not yet see CM3 value, so proving impact matters as much as growth.","page_number":3,"source":"Source: case study brief; 28k counted since the silent launch.",
 "notes":["The North Star has to grow 4.5x while the client base only doubles. So growth cannot come from enrolment alone; existing clients must level up faster and drop less.","The most important signal is the drops. Because points depend on balances, every 500k CZK or a closed term deposit moves points. Clients near a threshold bounce up and down without changing behaviour, and their savings rate bounces with them. So part of our North Star is balance noise.","The pilot shows execution matters: targeted communication almost doubled enrolment. And Finance does not yet see the value, which makes proof a survival issue for the programme."]})

add("04-filter", {"pattern":"funnel","headline":"Five filters narrow 30 areas to 5 priorities",
 "subline":"Number of areas left after each filter",
 "unit":"",
 "stages":[
  {"label":"All areas in the brief","value":30},
  {"label":"P&I owns the outcome","value":25},
  {"label":"Needed before 30 June","value":14},
  {"label":"After merging overlaps","value":9},
  {"label":"Top impact x feasibility","value":5}],
 "annotation":"Out first: UX and rule decisions owned by others (4, 9, 14, 19, 30); later: 2, 6, 13, 17, 21-23, 25, 27-29.",
 "page_number":4,"source":"Source: P&I assessment of the 30 areas; merges listed on the next page.",
 "notes":["Criteria, in knock-out order. One: does P&I own the outcome? The savings calculator, reward selection and native entry are squad Klient's; new scoring rules are the council's decision; CRM implementation is the CRM team's. P&I feeds them evidence.","Two: cost of delay. What must exist before Go Big or 30 June? Fénix has a floating deadline, agentic CRM and the self-learning Brain need foundations first.","Three: merge overlaps. Segment definitions and new money vs transfers are part of one metric truth; the dashboard is its output; young clients are one segment.","Four: impact on North Star and CM3, times feasibility with five analysts and our dependency on other teams."]})

add("05-scoring", {"pattern":"heatmap","headline":"The top 5 score highest on impact and feasibility",
 "subline":"Leading workstreams scored 1 (low) to 3 (high) per criterion",
 "unit":"",
 "rows":["P1 Metric truth","P2 Volatility","P3 Pilot learnings","P4 Segments","P5 At-risk list","Finance report","Brain v1","Personas"],
 "columns":["North Star","Proof / CM3","Time-critical","Unlocks others","Feasible now"],
 "values":[[2,3,3,3,3],[3,2,3,2,3],[2,1,3,3,3],[3,1,3,2,2],[3,2,2,1,3],[1,3,1,1,2],[3,2,1,2,1],[1,1,2,1,3]],
 "annotation":"Personas run alongside: the tool is nearly finished and Go Big validates it.",
 "page_number":5,"source":"Source: P&I judgement based on the brief; to be validated with squad leads in week 2.",
 "notes":["These are the nine workstreams after merging, scored on five criteria. The top five are all three-heavy on time-criticality and feasibility.","Brain v1 has the highest potential North Star impact, but nothing is in development and George releases depend on Vienna, so it scores low on feasibility before Go Big. It starts in February in FIT+, on the segments we build now.","The Finance report needs the one metric truth first, so it follows in Q1. The collaboration model is how we work, which I cover in the governance part."]})

add("06-loop", {"pattern":"process_flow","headline":"The top 5 build the P&I loop from the bottom up",
 "subline":"The P&I loop · P&I recommends, squads decide",
 "steps":[
  {"label":"Measure","detail":"P1 Metric truth, P2 Volatility","owner":"P&I","duration":"Dec–Jan"},
  {"label":"Find","detail":"P3 Pilot, P4 Segments, P5 At-risk","owner":"P&I","duration":"Dec–Jan"},
  {"label":"Decide","detail":"Brain v1 + personas","owner":"P&I","duration":"From Feb"},
  {"label":"Act","detail":"Campaigns, branches, George","owner":"Squads, DG&E","duration":"Go Big"},
  {"label":"Prove & learn","detail":"Holdouts on level-ups, SoW, CM3","owner":"P&I, Finance","duration":"From Feb"}],
 "highlight":0,
 "annotation":"Results flow back into Measure; one full turn of the loop is complete before 30 June.",
 "page_number":6,"source":SRC,
 "notes":["This is how the three pillars fit together: a loop. Measure, find, decide, act, prove, and back.","The top 5 deliberately sit at the start: you cannot close the loop without trusted measurement. Act belongs to the squads; P&I recommends, they decide.","Prove is not a separate project: every segment and every at-risk list ships with a holdout group. That is the experimentation framework missing from the list, built in from day one. The same loop can later be copied to other domains."]})

add("07-roadmap", {"pattern":"gantt","headline":"The top 5 land before Go Big; Brain follows",
 "subline":"P&I roadmap, December 2026 to June 2027",
 "periods":["Dec","Jan","Feb","Mar","Apr","May","Jun"],
 "bars":[
  {"label":"P1 Metric truth","start":0,"end":1,"highlight":True,"note":"foundation"},
  {"label":"P2 Volatility","start":0,"end":1,"note":"to council"},
  {"label":"P3 Pilot learnings","start":0,"end":0},
  {"label":"P4 Go Big segments","start":0,"end":1},
  {"label":"P5 At-risk list","start":1,"end":6,"note":"weekly, with holdout"},
  {"label":"Finance SoW / CM3","start":2,"end":6,"note":"monthly"},
  {"label":"Brain v1 in FIT+","start":2,"end":6,"note":"rules first, then George"},
  {"label":"Personas: Go Big test","start":0,"end":1,"note":"pre-test"},
  {"label":"Personas: validation","start":2,"end":3,"note":"vs holdouts"}],
 "gates":[{"label":"Go Big 1 Feb","period":1},{"label":"30 Jun","period":6}],
 "annotation":"P1 rests on one reporting lead and one data engineer; their time is the critical path.",
 "page_number":7,"source":"Source: P&I plan; dates depend on partner-team capacity.",
 "notes":["Everything in the top 5 lands before Go Big on 1 February. Pilot learnings in December feed the Go Big segments in January.","After Go Big, the Finance report runs monthly on the new definitions, and Brain v1 starts in FIT+ with rules from the Go Big segments, then moves to George once Vienna capacity is secured. Personas are nearly finished: in January we pre-test the Go Big messages on them, and in February and March we compare their predictions with the real holdout results. Only if they predict well do we use them to pre-test every campaign.","The critical path is P1: it rests on one reporting lead and one data engineer. Protecting their time is my first ask."]})

add("08-team", {"pattern":"benchmark_table","headline":"Six people cover the top 5 as personas wrap up",
 "subline":"P&I team allocation · AI engineers move from personas to modelling",
 "columns":["Dec–Jan","From Feb"],
 "rows":[
  {"label":"Data eng. + reporting","values":["P1 truth, dashboard, P2 data","Finance report, Brain data"]},
  {"label":"AI engineer A","values":["P2 volatility, P3 pilot","Holdouts, experiments"]},
  {"label":"AI engineer B","values":["P4 segments (Klient)","Brain v1 rules"]},
  {"label":"AI engineer C","values":["Personas, then P5 (Bankéř)","Brain v1 in FIT+"]},
  {"label":"AI engineer D","values":["Personas: Go Big pre-test","Persona validation"]}],
 "annotation":"Reporting is the thinnest skill; AI engineers learn the reporting stack in Q1.",
 "page_number":8,"source":"Source: planned team of six; personas project closing in the coming weeks.",
 "notes":["This is the real team: four AI engineers from the synthetic personas project, one reporting lead from financial health and one data engineer from Level Up.","The persona tool is nearly finished, so the AI engineers move onto the modelling work in the top 5: volatility simulation, pilot uplift, segments and the at-risk model. P4 and P5 are the first building blocks of Brain, so they are building Brain from day one.","One engineer finishes personas and uses them on Go Big. The thinnest skill is reporting: one person. That is a single point of failure, so the AI engineers learn the reporting stack in Q1."]})

add("09-missing", {"pattern":"bullet_list","headline":"The list lacks a way to prove what P&I changes",
 "bullets":[
  {"text":"Experimentation framework with holdout groups","sub":["Without it, SoW and CM3 gains cannot be attributed to the programme"],"emphasis":True},
  {"text":"North Star driver tree and forecast","sub":["Enrolment x activation x level-up rate minus drops: is 125k reachable?"]},
  {"text":"Analysis of level volatility, not just data quality","sub":["How much of the 22.6k drops is balance movement, not behaviour"]},
  {"text":"AI compliance: GDPR and the AI Act","sub":["Banker notes, Brain and personas need a legal basis before scale"]}],
 "annotation":"I would add the first three to P&I's scope now; compliance runs alongside Brain v1.",
 "page_number":9,"source":SRC,
 "notes":["Four things I would add. First and most important: a way to prove impact. Holdout groups for every campaign and list. Without that, we will never convince Finance.","Second, a driver tree that shows whether 125k is reachable and which lever gets us there.","Third, the list has data quality and new rules, but not the question in between: how much of the drops is pure balance movement. That is the evidence the council needs.","Fourth, AI compliance. Banker notes in particular are personal data."]})

add("10-info", {"pattern":"benchmark_table","headline":"Five unknowns close within three weeks",
 "subline":"What I still need to know, and how I will get it",
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
 "subline":"Proposed squad KPIs; targets set after the December baseline",
 "columns":3,
 "metrics":[
  {"label":"ONE NORTH STAR NUMBER","value":"100%","target":"squads + Finance by Feb","trend":"Measure"},
  {"label":"NOISE IN LEVEL DROPS","value":"−50%","target":"after rule change","trend":"Measure"},
  {"label":"OUTPUTS ACTED ON","value":"≥70%","target":"decided within 2 weeks","trend":"Find"},
  {"label":"INCREMENTAL LEVEL-UPS","value":"≥10k","target":"vs holdout, by 30 Jun","trend":"Prove"},
  {"label":"DROPS PREVENTED","value":"≥5k","target":"vs holdout, at-risk list","trend":"Prove"},
  {"label":"SQUAD SATISFACTION","value":"≥8/10","target":"quarterly survey","trend":"Trust"}],
 "annotation":"P&I contributes to the North Star; it does not own it. These KPIs measure that contribution.",
 "page_number":11,"source":"Source: proposed targets; illustrative until baselined.",
 "notes":["P&I recommends and squads decide, so we are judged on what others do with our work, not on how many reports we ship.","Measure: one number for the North Star used by everyone, and less noise in level drops. Find: share of our outputs that lead to a decision. Prove: incremental level-ups and prevented drops, measured against holdouts. Trust: how satisfied the squads are with us.","Targets are proposals; I would set them after the December baseline."]})

add("12-governance", {"pattern":"bullet_list","headline":"Shared rules for capacity keep the priorities from eroding",
 "columns":2,
 "bullets":[
  {"text":"One domain priority forum","sub":["Monthly; public P&I backlog"],"emphasis":True},
  {"text":"Explicit capacity rule","sub":["60% plan, 25% requests, 15% buffer"]},
  {"text":"Named contacts per squad","sub":["Klient and Bankéř; one intake"]},
  {"text":"Book partner capacity early","sub":["George, FIT+, CRM planning"]},
  {"text":"One metric tree in all OKRs","sub":["Squads and Finance steer alike"]},
  {"text":"Early wins build credibility","sub":["Pilot learnings, at-risk list"]}],
 "annotation":"New requests are welcome; they compete openly for the same capacity.",
 "page_number":12,"source":SRC,
 "notes":["How the priorities survive many stakeholders. One forum with the domain lead decides the order; the P&I backlog is public, so a new request visibly displaces something else.","Capacity is explicit: 60% on priorities, 25% on requests, 15% buffer. Two AI engineers are named contacts: the one on segments for squad Klient, the one on the at-risk list for squad Bankéř. They take requests and work on priorities for that squad.","Every permanent report needs an owner and the decision it serves. Our needs from George, FIT+ and CRM go into their planning early. All squads use the same metric tree in their OKRs. And early wins buy credibility to say no later."]})

add("13-closing", {"pattern":"closing","headline":"Three decisions let P&I start on 1 December",
 "takeaways":["Trusted numbers first: remove balance noise","Act before Go Big with pilot-proven segments","Holdouts let P&I prove value to Finance"],
 "next_steps":[
  {"action":"Confirm the top 5 priorities","owner":"Domain lead","timing":"This week"},
  {"action":"Protect reporting and data eng. for P1","owner":"Head of Product","timing":"By 1 Dec"},
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

import re
slides=[(f"{i+1:02d}-"+re.sub(r"^\d+-","",n), s) for i,(n,s) in enumerate(slides)]
for i,(n,sp) in enumerate(slides):
    if "page_number" in sp: sp["page_number"]=i+1
os.makedirs("specs", exist_ok=True)
paths=[]
for n,s in slides:
    p=f"specs/{n}.json"; json.dump(s, open(p,"w"), ensure_ascii=False, indent=2); paths.append(p)
json.dump({"title":"Performance & Intelligence — P&I proposal","description":"P&I squad PM case study, Level Up Advisory","slides":paths}, open("deck.json","w"), indent=2)
