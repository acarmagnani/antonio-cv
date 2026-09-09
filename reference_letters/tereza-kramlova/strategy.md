# Reference letter, Tereza Kramlova (Ramboll Management Consulting)

The shared rules (umbrella principle, four-paragraph shape, voice, truthfulness, process) live in `reference_letters/strategy.md` and are not repeated here. This file holds what is specific to Tereza.

## Status

Asked over LinkedIn on 2026-09-08. She said yes and asked for a draft, with one instruction: **make it as specific as possible to the roles I am applying to.** That instruction drives everything below.

The draft is written: `reference_letter.md` here is the source, and `reference_letter.docx` is what she receives, regenerated with `python system/make_reference_docx.py reference_letters/tereza-kramlova`. Her LinkedIn experience export is in this folder.

Decisions taken while drafting that are not obvious from the letter itself: **no client is named**, because `content_base.yaml` does not name them either ("a corporate client", "real estate investment managers") and asking her to put client names in writing is the kind of thing that makes a referee hesitate; and the letter was cut to **one page**, which is what removed the fuller version of the workshop, benchmark and Genesta material down to a single closing sentence.

## The umbrella

**Consulting, ESG and sustainability, data, supply chain, innovation.** That is the ESG-plus-data half of my search: sustainability advisory in consultancies (Ramboll, Sweco, NIRAS, COWI, Big 4), ESG and climate risk seats inside investors and banks, and analyst roles where the differentiator is being able to build the tooling rather than only consume its output.

She is the wrong referee for a pure real estate investment seat, and the letter should not try to be one. Real estate appears only as a clause of breadth (Genesta, a real estate investment manager), never as the thesis.

## Who she is

- **At Ramboll:** Associate Manager in Responsible Business Conduct, ESG & Sustainability Consulting, from April 2024 to September 2025. That is the title she held while she was my manager, and the one that goes in the letter.
- **Her Ramboll arc:** hired in November 2022 by Thomas Trier Hansen into Ramboll's newly established human rights team, first as Senior Consultant in Responsible Business Conduct, and one of a founding team of three that grew the practice past twenty experts. By the time I arrived she had four direct reports and was one of the team's key experts on business and human rights.
- **Today:** Associate Director at Control Risks in Dubai, since July 2026. She joined Control Risks in September 2025 as Senior Advisor in Business and Human Rights, advising companies, investors and project developers on human rights due diligence and worker welfare across the Middle East, Africa and Asia. Her LinkedIn headline reads "Business and Human Rights at Control Risks | Worker Welfare & Labour Rights | UNGPs & OECD Guidelines implementation".
- **Why this matters for the letter, beyond getting the titles right:** the signature carries weight. An Associate Director at Control Risks whose entire specialism is UNGP and OECD implementation is exactly the kind of person whose judgement about human rights due diligence work is not questioned, and the letter should open in a way that makes that authority visible rather than burying it.
- **Timing detail worth knowing:** she left Ramboll in September 2025, the month after my internship ended, so the work we did together sits at the end of her time there and is recent in her memory.
- **Settled:** she was my manager at **Ramboll**, not Sweco. Everything below is Ramboll work, May to August 2025, where my title was Intern in Responsible Business Conduct.

## What we actually did together

She was the manager over all three projects below, so the letter can speak in her first person about all of them. Attribution within them is not uniform, and that difference is handled explicitly in each case.

### 1. Nordzucker, Human Rights Impact Assessment (the volume and method piece)

**Her number one client, and she was fully involved.** Nordzucker is a large European sugar group with production and sourcing across several crops and several continents. The job was a Human Rights Impact Assessment: a screening of potential human rights and environmental risks for every combination of crop and sourcing geography, so the client could see where its exposure actually sat instead of treating the whole footprint as one undifferentiated risk.

Mechanically it was a very large structured assessment: roughly forty potential risks (rights and environmental issues drawn from the internationally recognised instruments, see the frameworks note below), scored one to five against each crop and each geography, with a scoring matrix deciding which combinations came out as salient. Forty risks across a handful of crops and a handful of geographies is several hundred scored judgements, each of which had to be defensible.

What made it work was the research underneath the scores: country and sector conditions, current reporting, NGO and institutional sources, read at a volume that would not have been possible by hand alone, which is where I used AI research tools to source and cite at scale. The deliverable had two halves, the underlying database and a client-facing dashboard that made the pattern legible: which crops in which geographies carry which salient risks, and therefore where the client should look first.

I built this alongside a colleague who had started it before I joined, and I carried a large share of the assessment work while the systems half was shared. **The letter says work I carried, never a system I invented.**

**Naming specifics, and the limit on it.** The geographies I am confident about are Brazil, Germany, South Africa and China, which is to say sourcing across South America, Europe, Africa and Asia. **The letter names the continents, not the countries**, because the continent statement is certainly true, it makes the same point about global footprint, and it cannot be corrected by anyone who knows the account better than I do. On crops, the wording is **"multiple crops including sugar cane and root crops"**: those two are confirmed, and apple stays out because I only think it was there.

### 2. Colt, salience assessment system (the innovation and data piece)

Colt is a telecommunications and network infrastructure company headquartered in London. Same underlying discipline as Nordzucker, far more sophisticated as a system.

**Attribution, which has to be exact here.** The engagement was run mainly with Russell, with Tereza above it and aware of the work throughout. Within that, the salience workbook itself was mine, built end to end. So the letter is written as a system I designed and built inside a project a colleague led, which is both true and stronger than a vaguer claim would be.

The design: one Excel workbook, many worksheets, one per category the assessment was structured by. In each worksheet the user selects a risk from the standard catalogue, describes it, and scores it. Those scores resolve automatically into a salience determination, salient or not salient, according to the convention rather than the user's judgement. The final worksheet is a dashboard consolidating every salient risk across every worksheet.

The hard part, and the reason it was worth building at all, is that the dashboard is live. Change a score in any worksheet and the dashboard updates itself. I built that with Power Query and VBA: the routine reads the current dashboard state, walks every worksheet, identifies which risks are newly salient, which were already there and which have dropped out of salience, matches them against what already exists using an ID I assigned to each risk in each worksheet, and rewrites the dashboard accordingly.

What that is worth to a consultancy is the sentence the letter has to land: the assessment stops being a document that is obsolete the moment a score changes and becomes a tool the client can keep using, which removes the manual reconsolidation this kind of workbook normally demands at every revision, exactly the work that eats junior hours and introduces errors. Russell was very happy with the result.

**What this paragraph is for, and the deliberate pivot in it.** Nordzucker carries the ESG and sustainability substance, and Colt carries the technical half: Excel, Power Query, VBA, and the design of a system somebody else has to operate. The letter should say that division outright, because it is also what she told me about my work, that the hard skills and the speed of learning were the strong part alongside the domain understanding. So the letter's claim is that I was solid on the ESG and sustainability substance and, separately, showed real aptitude on the technical side, with one example for each rather than one blurred example of both.

**Usability is part of the craft here and should be in the letter.** A large part of the work was not the automation but deciding how the thing would be used: what a consultant sees when they open a worksheet, what they have to decide and what the workbook decides for them, and what the final dashboard has to show for the client to act on it rather than merely read it. That is the difference between a clever workbook and a usable one, and it is the sort of thing a manager notices.

Alongside the tool I produced the workshop and training material on business and human rights for the same client, using real cases to show what the risks look like in practice and what mitigating them involves, and I ran a peer benchmark of its responsible business practices against competitors. Those work as a single clause showing the work was not only technical, and they are the evidence that I can present to a client, not only build for one.

### 3. Genesta, Code of Conduct review (the breadth clause)

**The first project I did there, and she was involved.** Genesta is a Nordic real estate investment manager. We reviewed its Code of Conduct against international human rights standards, found where it fell short (construction being a genuinely high-risk sector for worker safety, labour conditions and the reachability of a whistleblowing channel), and produced a supplier-facing resource mapping the Code to the underlying instruments (UDHR, ICESCR, ICCPR) so contractors and subcontractors could see what was actually expected of them on site.

**One clause, not a paragraph.** It buys two things cheaply: that the work covered investors and asset owners and not only corporates, and a quiet real estate signal for the half of my search Tereza does not otherwise cover.

**The microsite comes back, abstracted, and here is the reasoning.** I proposed and built a small web tool so that workers on site could reach the reporting channels from a phone through a QR code. It was never deployed, so it cannot appear as a client deliverable. It can appear as evidence of initiative, which is the better use of it anyway: the closing paragraph would otherwise call me proactive with nothing behind the word, and one concrete instance of proposing something nobody asked for and then building it is worth more than the adjective. So the letter says, without naming the client or the document, that I identified a practical gap in how a policy would actually reach the people it was written for and built a web tool to close it, on my own initiative. That is true whether or not it went live, and it does not assert that it did.

**Residual risk, worth naming:** if she does not remember it, she cuts one clause and nothing else moves. That is the test every sentence in this letter has to pass anyway.

### 4. Two Ramboll projects that stay OUT, and why

Cross-checked the Ramboll block of `content_base.yaml` against this file. Two bullets were missing here, and both are now deliberately excluded, because neither was Tereza's.

- **The Critical Raw Materials study** (mapping the supply chains of 20+ critical raw materials under the EU Critical Raw Materials Act) was done with **Joachim**, who is the next referee I plan to ask. It is his letter's material, not hers.
- **The real estate ESG due diligence service line** (building energy and decarbonisation assessments aligned with EU building performance regulation) was done with **Jonathan Martins**, who is in `reference/people/jonathan-martins.md`, Global Industry Lead for Buildings & Cities at Ramboll, MRICS and Board Chair of RICS Denmark.

The consequence for this letter has to be stated plainly, because it removes two things I would otherwise want: **decarbonisation and building energy are not available here**, and neither is the business development angle. Both belong to other referees, and asking Tereza to vouch for work she did not oversee is exactly the failure the general strategy forbids.

### 5. The general description of the work, which the letter needs alongside the two examples

The two projects are there to demonstrate specific things: Excel and systems building, innovation, speed of learning, rigour. They are not a complete description of what I did in that team. So the letter also needs one general statement of the territory, naming the frameworks and regulation the work sat inside, without a worked example for each.

The frameworks and instruments I am certain I worked with there, and which can be named: **UNGPs, OECD Guidelines, HRDD, Human Rights and Environmental Impact Assessment, due diligence, CSDDD, CSRD, EU Taxonomy, double materiality**.

**Why this is safe to name rather than a stretch.** When I applied for a role at Ramboll and Tereza helped me with my CV, she was the one who told me to put these on it. She is comfortable attesting to the territory, and it is her own vocabulary from her own profile, where she lists preparing clients for compliance with SFDR, CSDDD, Taxonomy, the Forced Labour Ban, CSRD, the Battery Regulation and LkSG.

**One correction that matters, because she would catch it instantly.** A double materiality assessment is not what Nordzucker was. Double materiality is the CSRD and ESRS exercise of testing each sustainability topic in two directions, the company's impact on people and environment, and the financial materiality of that topic for the company. An HRIA assesses actual and potential impacts on people across operations and supply chain. They share the severity logic, which is why they feel similar, and they are different instruments. So the acronyms go in the general sentence as territory I worked in, and **Nordzucker is never labelled a double materiality assessment**.

## Frameworks and vocabulary, so the letter uses the right words

The terms below are the professional conventions, not Ramboll inventions. Getting them right is most of what makes the letter read as written by someone senior in this field, and in her case the reader may well be someone who knows these instruments as well as she does.

- **HRDD, human rights due diligence,** and **HRIA, Human Rights Impact Assessment.** The second is the named deliverable for Nordzucker.
- **UNGPs, the UN Guiding Principles on Business and Human Rights** (2011). The foundational instrument and the source of the salience concept. The acronym is UNGP, not UNDP, which is the UN Development Programme and a different body entirely.
- **Salient human rights issues:** the rights at risk of the most severe negative impact through a company's activities or business relationships, a term that comes from the UNGP Reporting Framework. This is the word I could not remember, and it is the right one: what the Colt tool computes is salience.
- **The scoring convention.** Salience is built from **severity** and **likelihood**, and severity itself has three dimensions under the UNGPs: **scale** (how grave the impact is), **scope** (how many people it affects) and **irremediability** (how hard it is to put right), with severity outranking likelihood in prioritisation. That is the "two scores producing a third" I described, and because it is the standard rather than a house rule, the tool could compute the determination instead of leaving it to the user.
- **OECD Guidelines for Multinational Enterprises on Responsible Business Conduct** and the **OECD Due Diligence Guidance**, the other half of the standard pairing with the UNGPs, and the one that frames due diligence as an ongoing process rather than a report. Her own LinkedIn headline names UNGPs and OECD Guidelines together, so the letter should too.
- **The risk catalogue.** The roughly forty risks come from the internationally recognised rights: the International Bill of Human Rights (UDHR, ICCPR, ICESCR) and the ILO core conventions, plus the group-specific instruments that explain the examples I remember, **UNDRIP** for Indigenous peoples' rights and **CRPD** for the rights of persons with disabilities. Whether the specific catalogue came from the Danish Institute for Human Rights toolbox is unconfirmed and does not need to be: "internationally recognised human rights instruments" is correct either way.
- **The regulatory driver, worth one mention.** CSDDD and CSRD are why corporates buy this work at all, and her Ramboll profile lists preparing clients for SFDR, CSDDD, Taxonomy, the Forced Labour Ban, CSRD, the Battery Regulation and LkSG. One mention of that context signals that the author understands the market and not only the method.

## Open questions

- **Power BI: did I actually use it at Ramboll?** I mentioned it in passing, but what I remember building there is Excel, Power Query and VBA, and that is what the letter says unless you confirm otherwise. It is asked for by DNB, EY and CBRE, so it is worth a minute of thought, and it is not worth a sentence that will not survive an interview question about it.

## Her feedback on me, which is the raw material for the closing paragraph

What she said, in her words as I remember them: very strong hard skills, very good with technology, a very good understanding of things, learns very fast, very good people skills, very good soft skills, very good communication, and very proactive. She also said repeatedly that I did things with genuine appetite and enthusiasm.

The technical qualities belong in the body, where the Nordzucker and Colt examples demonstrate them rather than assert them, and the closing paragraph carries the human ones: communication, working with people, initiative, and the enthusiasm, which is the one that sounds most like her and least like a template.

## Per-paragraph plan

1. **Opening.** Control Risks and her role there, then Ramboll, her title as Associate Manager in Responsible Business Conduct and the period, the capacity in which she supervised me (Intern in Responsible Business Conduct, May to August 2025, in a team she helped build), and the explicit umbrella: ESG and human rights due diligence, supply chain risk, and the data and automation side of that work. This paragraph, or the sentence that opens paragraph two, also carries the general description of the territory with the frameworks named, so that the two examples that follow read as illustrations of a wider body of work rather than as its whole extent.
2. **Nordzucker, the ESG and sustainability half.** The assessment, its scale and method, the frameworks by name, and what it gave the client: a defensible view of where its exposure actually sits, by crop and geography, so that attention and remediation go where the risk is rather than everywhere at once.
3. **Colt, the technical half.** The system, what makes it different from a static assessment, the tooling by name (Excel, Power Query, VBA), the thought given to how it would be used, and what it meant for the team and the client. Genesta enters here as the single clause of breadth.
4. **Closing.** How I worked with the team and with clients, communication, speed of learning and enthusiasm, and initiative evidenced by the web tool clause rather than merely asserted, ending in a plain recommendation for the roles named in paragraph one.
