/*!
 * Public AI Utility Toolkit — app.js
 * Progressive enhancement: all content is present in index.html and readable without JavaScript.
 * This file adds preferences, navigation, search, filtering, the interactive tools and contact routing.
 * Licence: MIT (code) / Open Government Licence v3.0 (content).
 */
(function () {
  'use strict';

  /* ------------------------------------------------------------------
   * 1. CONFIGURATION — maintainers edit this block only.
   * ------------------------------------------------------------------ */
  var PAUT_CONFIG = {
    repo: 'cyberdudeuk/cyberdudeuk.github.io',
    // Team mailbox for direct messages. Leave empty to route everything through GitHub.
    // Displayed masked on screen and assembled only on request, to reduce automated harvesting.
    mailbox: '',
    maskMailbox: true,
    // Optional HTTPS endpoint if you later want server-side submission instead of mailto:
    formEndpoint: '',
    responseDays: 5
  };

  /* ------------------------------------------------------------------
   * 2. DATA — the corpus that powers filtering and the tools.
   * ------------------------------------------------------------------ */
  var PAUT = {"meta":{"version":"2.0.0","updated":"2026-08-08","nextReview":"2026-11-08","owner":"Public AI Utility Toolkit working group","licence":"Open Government Licence v3.0 (content) / MIT (code)"},"resources":[{"t":"Generative AI Framework for HMG","o":"DSIT / GDS","u":"https://www.gov.uk/government/publications/generative-ai-framework-for-hmg","c":"policy","tier":1,"tags":["governance","genai","uk"],"w":"Baseline principles and practical guardrails for building generative AI in government."},{"t":"AI Playbook for the UK Government","o":"DSIT","u":"https://www.gov.uk/government/publications/ai-playbook-for-the-uk-government","c":"policy","tier":1,"tags":["governance","delivery","uk"],"w":"Ten principles plus per-technology guidance for safe, effective public sector AI adoption."},{"t":"Algorithmic Transparency Recording Standard (ATRS)","o":"DSIT / CDDO","u":"https://www.gov.uk/government/collections/algorithmic-transparency-recording-standard-hub","c":"standard","tier":1,"tags":["transparency","governance","uk"],"w":"Mandatory-style template for publishing how an algorithmic tool is used in decision-making."},{"t":"Data Ethics Framework","o":"DSIT","u":"https://www.gov.uk/government/publications/data-ethics-framework","c":"policy","tier":1,"tags":["ethics","data","uk"],"w":"Structured ethical appraisal for public sector data and AI projects."},{"t":"Service Standard (14 points)","o":"GDS","u":"https://www.gov.uk/service-manual/service-standard","c":"standard","tier":1,"tags":["ucd","delivery","uk"],"w":"The assessment backbone for any public service — align AI features to each point."},{"t":"Government Service Manual","o":"GDS","u":"https://www.gov.uk/service-manual","c":"guidance","tier":1,"tags":["ucd","delivery","uk"],"w":"End-to-end practice guidance for user research, design, technology and operations."},{"t":"Government Design Principles","o":"GDS","u":"https://www.gov.uk/guidance/government-design-principles","c":"guidance","tier":1,"tags":["ucd","uk"],"w":"Ten principles — start with user needs, do less, design with data, do the hard work to make it simple."},{"t":"Technology Code of Practice","o":"CDDO","u":"https://www.gov.uk/guidance/the-technology-code-of-practice","c":"standard","tier":1,"tags":["delivery","governance","uk"],"w":"Criteria for technology spend approval — interoperability, open standards, security, sustainability."},{"t":"Digital, Data and Technology Capability Framework","o":"GDS","u":"https://ddat-capability-framework.service.gov.uk/","c":"toolkit","tier":1,"tags":["skills","people","uk"],"w":"Map AI-related skills to recognised roles and progression levels."},{"t":"Open source guidance (coding in the open)","o":"GDS","u":"https://www.gov.uk/government/publications/open-source-guidance","c":"guidance","tier":1,"tags":["engineering","openness","uk"],"w":"When code should be open or closed, and how to publish safely."},{"t":"GDS API technical and data standards","o":"GDS","u":"https://www.gov.uk/guidance/gds-api-technical-and-data-standards","c":"standard","tier":1,"tags":["engineering","interoperability","uk"],"w":"How to design, document and version APIs that agents and skills can call."},{"t":"WCAG 2.2","o":"W3C","u":"https://www.w3.org/TR/WCAG22/","c":"standard","tier":1,"tags":["accessibility","deia"],"w":"The normative success criteria — target AA as a minimum, AAA where feasible."},{"t":"ARIA Authoring Practices Guide (APG)","o":"W3C WAI","u":"https://www.w3.org/WAI/ARIA/apg/","c":"guidance","tier":1,"tags":["accessibility","engineering"],"w":"Accessible patterns for tabs, accordions, comboboxes, dialogs and more."},{"t":"EN 301 549 accessibility requirements","o":"ETSI/CEN/CENELEC","u":"https://www.etsi.org/deliver/etsi_en/301500_301599/301549/","c":"standard","tier":1,"tags":["accessibility","procurement"],"w":"The procurement-facing accessibility standard referenced by UK/EU regulations."},{"t":"Accessibility requirements for public sector websites and apps","o":"GOV.UK","u":"https://www.gov.uk/guidance/accessibility-requirements-for-public-sector-websites-and-apps","c":"guidance","tier":1,"tags":["accessibility","legal","uk"],"w":"What the 2018 regulations require, including the accessibility statement duty."},{"t":"Public Sector Bodies (Websites and Mobile Applications) Accessibility Regulations 2018","o":"legislation.gov.uk","u":"https://www.legislation.gov.uk/uksi/2018/952/contents/made","c":"law","tier":0,"tags":["accessibility","legal","uk"],"w":"The underlying legal duty."},{"t":"Equality Act 2010","o":"legislation.gov.uk","u":"https://www.legislation.gov.uk/ukpga/2010/15/contents","c":"law","tier":0,"tags":["deia","legal","uk"],"w":"Protected characteristics, reasonable adjustments and discrimination duties."},{"t":"Public Sector Equality Duty guidance","o":"EHRC","u":"https://www.equalityhumanrights.com/guidance/public-sector-equality-duty","c":"guidance","tier":1,"tags":["deia","legal","uk"],"w":"Due regard duty — evidence it in every AI-assisted decision or service change."},{"t":"Make your service accessible: an introduction","o":"GDS","u":"https://www.gov.uk/service-manual/helping-people-to-use-your-service/making-your-service-accessible-an-introduction","c":"guidance","tier":1,"tags":["accessibility","ucd","uk"],"w":"Practical starting point for teams new to accessibility duties."},{"t":"Publish an accessibility statement","o":"GOV.UK","u":"https://www.gov.uk/guidance/make-your-website-or-app-accessible-and-publish-an-accessibility-statement","c":"toolkit","tier":1,"tags":["accessibility","transparency","uk"],"w":"Model wording and required disclosures for non-accessible content."},{"t":"Research with people with disabilities and access needs","o":"GDS","u":"https://www.gov.uk/service-manual/user-research/running-research-sessions-with-people-with-disabilities","c":"guidance","tier":1,"tags":["research","deia","uk"],"w":"How to recruit and run inclusive sessions, including with assistive technology users."},{"t":"Helping people to use your service (assisted digital)","o":"GDS","u":"https://www.gov.uk/service-manual/helping-people-to-use-your-service","c":"guidance","tier":1,"tags":["deia","inclusion","uk"],"w":"Assisted digital support and digital inclusion planning."},{"t":"Inclusive Design Principles","o":"Paciello/TPGi et al.","u":"https://inclusivedesignprinciples.info/","c":"guidance","tier":2,"tags":["ucd","deia"],"w":"Seven principles: provide comparable experience, be consistent, give control, offer choice."},{"t":"Inclusive Design Toolkit","o":"Microsoft","u":"https://inclusive.microsoft.design/","c":"toolkit","tier":3,"tags":["ucd","deia"],"w":"Persona spectrum and exclusion-mapping activities for workshops."},{"t":"Home Office accessibility \"dos and don’ts\" posters","o":"UK Home Office","u":"https://github.com/UKHomeOffice/posters","c":"toolkit","tier":1,"tags":["accessibility","deia","uk"],"w":"Print-ready posters for autistic users, screen readers, dyslexia, low vision, D/deaf users."},{"t":"GOV.UK Design System","o":"GDS","u":"https://design-system.service.gov.uk/","c":"toolkit","tier":1,"tags":["ucd","engineering","uk"],"w":"Tested, accessible components and patterns — reuse before you invent."},{"t":"GOV.UK Prototype Kit","o":"GDS","u":"https://prototype-kit.service.gov.uk/","c":"toolkit","tier":1,"tags":["ucd","research","uk"],"w":"Rapid, realistic prototypes for usability testing without production risk."},{"t":"GOV.UK style guide (content design)","o":"GDS","u":"https://www.gov.uk/guidance/style-guide","c":"guidance","tier":1,"tags":["content","deia","uk"],"w":"Plain English, reading age, formatting and inclusive terminology."},{"t":"WebAIM contrast checker","o":"WebAIM","u":"https://webaim.org/resources/contrastchecker/","c":"tool","tier":3,"tags":["accessibility","tool"],"w":"Verify 4.5:1 text and 3:1 non-text contrast before shipping."},{"t":"Pa11y automated accessibility testing","o":"Pa11y","u":"https://pa11y.org/","c":"tool","tier":3,"tags":["accessibility","ci","tool"],"w":"Add automated WCAG checks to your pipeline — never as a substitute for manual testing."},{"t":"axe DevTools","o":"Deque","u":"https://www.deque.com/axe/devtools/","c":"tool","tier":3,"tags":["accessibility","tool"],"w":"Browser-based rule engine used widely for triage."},{"t":"Guidelines for secure AI system development","o":"NCSC + international partners","u":"https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development","c":"guidance","tier":1,"tags":["security","ai","uk"],"w":"Secure design, development, deployment and operation across the AI lifecycle."},{"t":"Secure by Design (UK government)","o":"Cabinet Office / GSG","u":"https://www.security.gov.uk/policy-and-guidance/secure-by-design/","c":"standard","tier":1,"tags":["security","delivery","uk"],"w":"Mandated activities and artefacts for digital service security in HMG."},{"t":"Cyber Assessment Framework (CAF)","o":"NCSC","u":"https://www.ncsc.gov.uk/collection/cyber-assessment-framework","c":"standard","tier":1,"tags":["security","assurance","uk"],"w":"Outcome-based objectives A–D for essential services and government systems."},{"t":"Post-quantum cryptography guidance and migration timeline","o":"NCSC","u":"https://www.ncsc.gov.uk/collection/post-quantum-cryptography","c":"guidance","tier":1,"tags":["pqc","security","uk"],"w":"Discovery by 2028, high-priority migration by 2031, complete by 2035."},{"t":"Post-Quantum Cryptography standards (FIPS 203/204/205)","o":"NIST","u":"https://csrc.nist.gov/projects/post-quantum-cryptography","c":"standard","tier":1,"tags":["pqc","security"],"w":"ML-KEM, ML-DSA and SLH-DSA — the algorithms your crypto inventory should target."},{"t":"OWASP Top 10 for LLM Applications","o":"OWASP","u":"https://owasp.org/www-project-top-10-for-large-language-model-applications/","c":"standard","tier":2,"tags":["security","ai","engineering"],"w":"Prompt injection, insecure output handling, supply chain and agency risks."},{"t":"MITRE ATLAS adversarial ML knowledge base","o":"MITRE","u":"https://atlas.mitre.org/","c":"toolkit","tier":2,"tags":["security","ai","threat"],"w":"Tactics and techniques for threat modelling AI systems."},{"t":"Secure Software Development Framework (SP 800-218)","o":"NIST","u":"https://csrc.nist.gov/pubs/sp/800/218/final","c":"standard","tier":2,"tags":["engineering","security"],"w":"Baseline secure SDLC practices to bind AI-generated code to."},{"t":"SLSA supply chain integrity framework","o":"OpenSSF","u":"https://slsa.dev/","c":"standard","tier":2,"tags":["engineering","supplychain"],"w":"Provenance levels for build artefacts — extend to model and skill artefacts."},{"t":"CycloneDX ML-BOM / AI-BOM","o":"OWASP CycloneDX","u":"https://cyclonedx.org/capabilities/mlbom/","c":"standard","tier":2,"tags":["metadata","supplychain"],"w":"Machine-readable bill of materials for models, datasets and AI components."},{"t":"Guidance on AI and data protection","o":"ICO","u":"https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/","c":"guidance","tier":1,"tags":["privacy","legal","uk"],"w":"Lawful basis, fairness, transparency and accountability for AI processing."},{"t":"AI and data protection risk toolkit","o":"ICO","u":"https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/ai-and-data-protection-risk-toolkit/","c":"toolkit","tier":1,"tags":["privacy","assurance","uk"],"w":"Risk statements and controls mapped to the AI lifecycle."},{"t":"Data protection impact assessments (DPIA)","o":"ICO","u":"https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-impact-assessments-dpias/","c":"toolkit","tier":1,"tags":["privacy","legal","uk"],"w":"When a DPIA is mandatory and what a defensible one contains."},{"t":"Data Protection Act 2018","o":"legislation.gov.uk","u":"https://www.legislation.gov.uk/ukpga/2018/12/contents","c":"law","tier":0,"tags":["privacy","legal","uk"],"w":"UK GDPR implementation, including automated decision-making safeguards."},{"t":"ISO/IEC 42001 AI management systems","o":"ISO/IEC","u":"https://www.iso.org/standard/81230.html","c":"standard","tier":1,"tags":["governance","certification"],"w":"Certifiable management system for responsible AI — useful for supplier assurance."},{"t":"ISO/IEC 23894 AI risk management","o":"ISO/IEC","u":"https://www.iso.org/standard/77304.html","c":"standard","tier":1,"tags":["risk","governance"],"w":"AI-specific application of ISO 31000 risk management."},{"t":"ISO/IEC 27001 information security management","o":"ISO/IEC","u":"https://www.iso.org/standard/27001","c":"standard","tier":1,"tags":["security","certification"],"w":"Control baseline most suppliers will already hold."},{"t":"AI Risk Management Framework (AI RMF 1.0) + GenAI Profile","o":"NIST","u":"https://www.nist.gov/itl/ai-risk-management-framework","c":"standard","tier":1,"tags":["risk","governance"],"w":"Govern, Map, Measure, Manage — pairs cleanly with UK assurance practice."},{"t":"EU AI Act (Regulation 2024/1689)","o":"EUR-Lex","u":"https://eur-lex.europa.eu/eli/reg/2024/1689/oj","c":"law","tier":0,"tags":["legal","risk","eu"],"w":"Risk tiers and obligations that may bind UK bodies operating in the EU market."},{"t":"OECD AI Principles","o":"OECD","u":"https://oecd.ai/en/ai-principles","c":"policy","tier":2,"tags":["ethics","international"],"w":"Internationally agreed values-based principles for trustworthy AI."},{"t":"Recommendation on the Ethics of AI","o":"UNESCO","u":"https://www.unesco.org/en/artificial-intelligence/recommendation-ethics","c":"policy","tier":2,"tags":["ethics","international"],"w":"Global normative instrument covering human rights and inclusion."},{"t":"Understanding AI ethics and safety","o":"The Alan Turing Institute","u":"https://www.turing.ac.uk/research/publications/understanding-artificial-intelligence-ethics-and-safety","c":"guidance","tier":2,"tags":["ethics","uk","research"],"w":"The SUM values and FAST Track principles used across UK public sector."},{"t":"AI Standards Hub","o":"BSI / NPL / Turing","u":"https://aistandardshub.org/","c":"toolkit","tier":2,"tags":["standards","uk"],"w":"Searchable database of AI standards in development and published."},{"t":"Ada Lovelace Institute research","o":"Ada Lovelace Institute","u":"https://www.adalovelaceinstitute.org/","c":"research","tier":3,"tags":["ethics","public","research"],"w":"Public attitudes, algorithmic impact assessment and deliberative methods."},{"t":"Open Data Institute","o":"ODI","u":"https://theodi.org/","c":"research","tier":3,"tags":["data","openness"],"w":"Data ethics canvas and data institution patterns."},{"t":"Model Cards for Model Reporting","o":"Mitchell et al.","u":"https://arxiv.org/abs/1810.03993","c":"research","tier":2,"tags":["metadata","transparency"],"w":"The reference format for documenting intended use and performance by group."},{"t":"Datasheets for Datasets","o":"Gebru et al.","u":"https://arxiv.org/abs/1803.09010","c":"research","tier":2,"tags":["metadata","data"],"w":"Provenance, composition and collection questions for training/eval data."},{"t":"PROV-O provenance ontology","o":"W3C","u":"https://www.w3.org/TR/prov-o/","c":"standard","tier":1,"tags":["metadata","provenance"],"w":"Entity–activity–agent model for machine-readable evidence chains."},{"t":"DCAT 3 data catalogue vocabulary","o":"W3C","u":"https://www.w3.org/TR/vocab-dcat-3/","c":"standard","tier":1,"tags":["metadata","interoperability"],"w":"Describe datasets and services so registries can federate."},{"t":"C2PA content provenance and authenticity","o":"C2PA","u":"https://c2pa.org/","c":"standard","tier":2,"tags":["provenance","genai"],"w":"Cryptographic manifests for AI-generated or edited media."},{"t":"Model Context Protocol","o":"MCP","u":"https://modelcontextprotocol.io/","c":"standard","tier":3,"tags":["agents","engineering","interoperability"],"w":"Open protocol for connecting assistants to tools and data with explicit scopes."},{"t":"Model cards on Hugging Face Hub","o":"Hugging Face","u":"https://huggingface.co/docs/hub/model-cards","c":"toolkit","tier":3,"tags":["metadata","engineering"],"w":"Practical templates and YAML front-matter conventions."},{"t":"alphagov on GitHub","o":"GDS","u":"https://github.com/alphagov","c":"toolkit","tier":1,"tags":["engineering","openness","uk"],"w":"Reference implementations, frontend, and publishing platform source."},{"t":"x-govuk community tools","o":"Cross-government community","u":"https://x-govuk.github.io/","c":"toolkit","tier":2,"tags":["engineering","community","uk"],"w":"Community-built plugins, design tooling and prototypes."},{"t":"Open Government Licence v3.0","o":"The National Archives","u":"https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/","c":"law","tier":0,"tags":["openness","legal","uk"],"w":"Default licence for publishing public sector content and guidance."},{"t":"Greening Government ICT and Digital Services Strategy","o":"Defra / GGC","u":"https://www.gov.uk/government/publications/greening-government-ict-and-digital-services-strategy-2020-2025","c":"policy","tier":1,"tags":["sustainability","uk"],"w":"Carbon, circular-economy and reporting expectations for digital estates."},{"t":"Web Sustainability Guidelines (WSG)","o":"W3C Community Group","u":"https://w3c.github.io/sustyweb/","c":"guidance","tier":3,"tags":["sustainability","engineering"],"w":"Practical efficiency criteria for pages, media, hosting and AI workloads."}],"toolkit":[{"id":"TK-01","t":"AI asset metadata standard","cat":"governance","w":"Machine-readable schemas for skills, agents, prompts, tools, model-use events, evidence packs and source provenance.","out":"JSON Schema + YAML template","eff":"M","links":[["PROV-O","https://www.w3.org/TR/prov-o/"],["CycloneDX ML-BOM","https://cyclonedx.org/capabilities/mlbom/"],["DCAT 3","https://www.w3.org/TR/vocab-dcat-3/"]]},{"id":"TK-02","t":"Skill registry","cat":"delivery","w":"Approved, draft and deprecated skills with owners, sources, risk ratings, compatibility and evidence rules.","out":"Register + lifecycle policy","eff":"L","links":[["Model cards","https://huggingface.co/docs/hub/model-cards"],["alphagov","https://github.com/alphagov"]]},{"id":"TK-03","t":"Agent registry and bounding","cat":"delivery","w":"Bounded agents by autonomy level, permissions, allowed skills, prohibited actions, model constraints and kill-switch owner.","out":"Register + autonomy policy","eff":"L","links":[["MCP","https://modelcontextprotocol.io/"],["OWASP LLM Top 10","https://owasp.org/www-project-top-10-for-large-language-model-applications/"]]},{"id":"TK-04","t":"Evidence pack builder","cat":"assurance","w":"Source consultation records, AI-use declarations, validation results, human acknowledgements and audit trails.","out":"Generator on this page","eff":"S","links":[["ATRS","https://www.gov.uk/government/collections/algorithmic-transparency-recording-standard-hub"]],"live":"#tool-evidence"},{"id":"TK-05","t":"DEIA impact screen","cat":"assurance","w":"Equality, accessibility, assisted digital, digital inclusion, protected characteristic and vulnerability screening.","out":"Screening tool on this page","eff":"S","links":[["PSED","https://www.equalityhumanrights.com/guidance/public-sector-equality-duty"],["WCAG 2.2","https://www.w3.org/TR/WCAG22/"]],"live":"#tool-deia"},{"id":"TK-06","t":"Quantum readiness assessor","cat":"future","w":"Inventory cryptography, identify long-life data, assess harvest-now-decrypt-later exposure and plan crypto-agility.","out":"Assessment tool on this page","eff":"M","links":[["NCSC PQC","https://www.ncsc.gov.uk/collection/post-quantum-cryptography"],["NIST PQC","https://csrc.nist.gov/projects/post-quantum-cryptography"]],"live":"#tool-pqc"},{"id":"TK-07","t":"Human review triage (H0–H5)","cat":"assurance","w":"Risk-based routing that decides how many eyes, which specialists and what evidence an AI-assisted output needs.","out":"Triage tool on this page","eff":"S","links":[["NIST AI RMF","https://www.nist.gov/itl/ai-risk-management-framework"]],"live":"#tool-triage"},{"id":"TK-08","t":"Prompt and context pattern library","cat":"delivery","w":"Reviewed prompt patterns with source-citation requirements, refusal conditions, data-handling rules and test cases.","out":"Pattern library + tests","eff":"M","links":[["GenAI Framework for HMG","https://www.gov.uk/government/publications/generative-ai-framework-for-hmg"]]},{"id":"TK-09","t":"Conformance packs","cat":"assurance","w":"Executable checks turning WCAG, Service Standard, Secure by Design and TCoP clauses into automated tests.","out":"CI pack","eff":"L","links":[["Pa11y","https://pa11y.org/"],["Secure by Design","https://www.security.gov.uk/policy-and-guidance/secure-by-design/"]]},{"id":"TK-10","t":"Transparency record generator","cat":"governance","w":"Produce an ATRS-shaped public record for any algorithmic or AI-assisted tool in use.","out":"Generator on this page","eff":"S","links":[["ATRS hub","https://www.gov.uk/government/collections/algorithmic-transparency-recording-standard-hub"]],"live":"#tool-atrs"},{"id":"TK-11","t":"Supplier and procurement assurance kit","cat":"governance","w":"Questions, evidence asks and contract clauses for AI suppliers: model provenance, evaluations, accessibility, exit.","out":"Question bank + clauses","eff":"M","links":[["ISO/IEC 42001","https://www.iso.org/standard/81230.html"],["EN 301 549","https://www.etsi.org/deliver/etsi_en/301500_301599/301549/"]]},{"id":"TK-12","t":"Incident, near-miss and drift reporting","cat":"assurance","w":"Report AI failures, hallucinations, bias incidents, prompt injection and source drift with learning loops.","out":"Process + register","eff":"M","links":[["MITRE ATLAS","https://atlas.mitre.org/"],["NCSC secure AI","https://www.ncsc.gov.uk/collection/guidelines-secure-ai-system-development"]]},{"id":"TK-13","t":"Model and data provenance ledger","cat":"future","w":"Signed, tamper-evident record of which model, version, prompt, source and human touched each artefact.","out":"Ledger spec","eff":"L","links":[["C2PA","https://c2pa.org/"],["SLSA","https://slsa.dev/"]]},{"id":"TK-14","t":"Sustainability and cost-to-serve calculator","cat":"future","w":"Estimate energy, carbon and unit cost of model calls, and test whether a non-AI option is proportionate.","out":"Calculator + reporting","eff":"M","links":[["Greening Government ICT","https://www.gov.uk/government/publications/greening-government-ict-and-digital-services-strategy-2020-2025"],["W3C WSG","https://w3c.github.io/sustyweb/"]]},{"id":"TK-15","t":"Inclusive research and co-design kit","cat":"delivery","w":"Recruitment, consent, reimbursement and session plans that reach disabled, digitally excluded and seldom-heard users.","out":"Research kit","eff":"M","links":[["Research with disabled people","https://www.gov.uk/service-manual/user-research/running-research-sessions-with-people-with-disabilities"],["Assisted digital","https://www.gov.uk/service-manual/helping-people-to-use-your-service"]]},{"id":"TK-16","t":"Plain-language and reading-age checker","cat":"delivery","w":"Test AI-drafted content against GOV.UK style, reading age 9, and inclusive terminology before publication.","out":"Checker on this page","eff":"S","links":[["GOV.UK style guide","https://www.gov.uk/guidance/style-guide"]],"live":"#tool-readability"},{"id":"TK-17","t":"Records, retention and FOI readiness","cat":"governance","w":"Classify AI interaction logs as records; set retention, disclosure and redaction rules ahead of FOI/SAR requests.","out":"Retention schedule","eff":"M","links":[["DPA 2018","https://www.legislation.gov.uk/ukpga/2018/12/contents"]]},{"id":"TK-18","t":"Capability and competence pathway","cat":"delivery","w":"Role-based learning paths, licence-to-operate checks and refreshers for anyone using AI on public work.","out":"Curriculum map","eff":"M","links":[["DDaT framework","https://ddat-capability-framework.service.gov.uk/"]]}],"hlevels":[{"h":"H0","n":"No review needed","d":"Personal, throwaway, non-published exploration with no personal or sensitive data.","ex":"Explaining a concept to yourself; drafting private notes.","ev":"None required."},{"h":"H1","n":"Self-check","d":"Author verifies facts, sources and accessibility before use. Low impact, easily reversible.","ex":"Internal meeting notes, first-draft ideas.","ev":"AI-use note in the document."},{"h":"H2","n":"Peer check","d":"A second competent person checks output before it leaves the team.","ex":"Internal reports, non-public analysis, low-risk code in a sandbox.","ev":"Reviewer name, date, issues found."},{"h":"H3","n":"Specialist review (4-eyes)","d":"A named specialist in the relevant discipline reviews. No self-approval.","ex":"Accessibility, security, legal, statistical or clinical content; production code.","ev":"Specialist sign-off + test results."},{"h":"H4","n":"Multi-specialist review (6-eyes)","d":"Two or more specialisms plus the accountable owner. Independent challenge required.","ex":"Public-facing decisions, casework support, anything affecting entitlements.","ev":"Panel record, dissent captured, residual risk stated."},{"h":"H5","n":"Governance board and publication","d":"Formal board approval, published transparency record and monitored deployment.","ex":"Automated or semi-automated decisions about people; national services.","ev":"ATRS record, DPIA, EQIA, monitoring plan, review date."}],"personas":[{"t":"New or occasional contributor","n":"\"I don’t want to get this wrong.\"","need":"Plain-language guidance, safe defaults, confidence prompts, buddying and clear role limits.","start":"#start-here","route":"Take the 5-minute triage, then use the declaration generator."},{"t":"Experienced practitioner","n":"\"Give me the fast, correct route.\"","need":"Direct links to standards, patterns, conformance packs, test scripts and evidence automation.","start":"#toolkit","route":"Jump to the toolkit and copy the metadata schema."},{"t":"Specialist reviewer","n":"\"Show me what to challenge.\"","need":"Source-linked evidence, issue triage, risk decisions and assurance history.","start":"#assurance","route":"Use the H-level table and reviewer checklist."},{"t":"Accountable owner / SRO","n":"\"What am I signing?\"","need":"Risk overview, approval gates, residual risk, maturity dashboard and public transparency records.","start":"#tool-atrs","route":"Generate the transparency record and check the MoSCoW roadmap."},{"t":"Supplier or delivery partner","n":"\"What will I be assessed against?\"","need":"Published expectations, evidence formats, accessibility and security obligations, exit terms.","start":"#resources","route":"Filter resources by procurement and security."},{"t":"Member of the public","n":"\"How is AI being used on my case?\"","need":"Plain-English explanation, published records, how to challenge a decision and get support.","start":"#transparency","route":"Read the transparency and redress commitments."}],"glossary":[["Agent","Software that plans and acts across multiple steps using tools, within explicit permissions and bounds."],["Autonomy level","How far an agent may act without a human decision, from suggest-only to bounded execution."],["Assisted digital","Support for people who cannot use a digital service independently."],["ATRS","Algorithmic Transparency Recording Standard — the UK format for publishing algorithmic tool use."],["Conformance pack","A bundle of automated checks that tests an artefact against a named standard."],["Crypto-agility","The ability to change cryptographic algorithms without redesigning the system."],["DEIA","Diversity, equity, inclusion and accessibility."],["DPIA","Data protection impact assessment, required for high-risk processing."],["Drift","Divergence between a cited source, a model version or a control and what is actually in use."],["EQIA","Equality impact assessment evidencing the public sector equality duty."],["Evidence pack","The bundle of records proving how an AI-assisted output was produced, checked and approved."],["Harvest now, decrypt later","Capturing encrypted data today to decrypt once quantum computers are capable."],["Human in the loop","A person who must act before an output takes effect."],["Human on the loop","A person who monitors and can intervene in an otherwise automated process."],["Least privilege","Granting only the minimum permissions needed for the shortest necessary time."],["Material AI assistance","AI involvement that a reasonable reader would want disclosed because it shaped the output."],["Prompt injection","Untrusted content that manipulates a model into unintended actions."],["Provenance","The verifiable record of where content, data or code came from and how it changed."],["PQC","Post-quantum cryptography — algorithms resistant to quantum attack."],["Skill","A packaged, versioned capability an assistant or agent can invoke, with defined inputs and limits."],["Source tiering","Ranking sources by authority so conflicts resolve predictably."],["4-eyes / 6-eyes","Two or three independent people involved in producing and approving an output."]],"faq":[["Do I have to declare every use of AI?","No. Declare material assistance — where AI shaped the substance, structure, analysis or code of an output. Trivial uses such as spell-checking do not need a declaration, but your local policy may set a lower threshold."],["Can AI approve my work?","No. AI can suggest, draft, check and explain. Approval is a human act by someone with the authority to make that decision. AI never grants authority a user does not already hold."],["What if the AI cites a source that does not exist?","Treat it as an incident. Do not publish. Verify every citation against the original, log the failure in the drift and incident register, and check whether the same prompt pattern has been used elsewhere."],["Is this a substitute for a DPIA, EQIA or security assurance?","No. This toolkit helps you prepare and evidence those assessments; it does not replace them or the professionals accountable for them."],["Can I paste official-sensitive information into a general assistant?","Not unless the tool is explicitly approved for that classification and the data-handling terms have been assured. When in doubt, do not paste — ask your information asset owner."],["How do I handle AI-generated code?","Treat it as untrusted third-party code: review it, test it, scan dependencies, record provenance and never merge without a human reviewer who understands it."],["What accessibility duties apply to AI-generated content?","The same ones that apply to everything else. WCAG 2.2 AA, plain language, alternative formats and the accessibility statement duty all apply regardless of who or what drafted the content."],["Who do I contact if something goes wrong?","Your service owner and the named AI assurance contact for your organisation. Report near-misses too — they are the cheapest form of learning."]],"moscow":[{"p":"M","t":"Named accountable owner and published contact route","w":"Nothing on this page is credible without a person who owns it and answers questions."},{"p":"M","t":"Accessibility statement, testing evidence and feedback route","w":"Legally required for UK public sector sites; also the fastest trust signal."},{"p":"M","t":"Version, last-reviewed and next-review dates on every artefact","w":"Freshness is the main failure mode of guidance portals."},{"p":"M","t":"Machine-readable metadata schema published openly","w":"Without a schema, registries cannot federate and evidence cannot be automated."},{"p":"M","t":"Risk-based human review model with no self-approval","w":"The core control that keeps accountability with people."},{"p":"M","t":"Source citation and provenance for every claim","w":"Prevents hallucination becoming policy."},{"p":"M","t":"DEIA screening built into the default workflow","w":"Equality duty is a due-regard duty — it must happen before decisions, not after."},{"p":"S","t":"Search across the whole corpus with filters and permalinks","w":"Findability is the top usability complaint for guidance sites."},{"p":"S","t":"Role-based entry points and task-first navigation","w":"Users arrive with a task, not an interest in your information architecture."},{"p":"S","t":"Downloadable, offline and printable formats","w":"Supports assisted digital, low bandwidth and audit contexts."},{"p":"S","t":"Worked examples and anti-patterns for each control","w":"Abstract principles do not change behaviour; examples do."},{"p":"S","t":"Change log and subscribe-to-updates","w":"Lets teams re-check work when guidance changes."},{"p":"S","t":"Multilingual and alternative-format provision (Welsh, Easy Read, BSL)","w":"Statutory in some contexts and essential for inclusion in all."},{"p":"S","t":"Automated link-health and freshness checking","w":"Broken authority links silently destroy trust."},{"p":"C","t":"API and JSON export of the registry and corpus","w":"Enables reuse by other departments and tooling."},{"p":"C","t":"Maturity self-assessment with benchmarking","w":"Helps organisations see where they are without a consultant."},{"p":"C","t":"Community contribution workflow with moderation","w":"Scales the corpus beyond a single team."},{"p":"C","t":"Interactive decision tree for tool selection","w":"Reduces the \"which tool may I use?\" support burden."},{"p":"C","t":"Carbon and cost telemetry per model call","w":"Makes proportionality measurable rather than rhetorical."},{"p":"W","t":"Automated approval of any high-risk output","w":"Out of scope by design — approval stays human."},{"p":"W","t":"Storing personal or official-sensitive data in this portal","w":"The portal is public and stateless; sensitive records belong in assured systems."},{"p":"W","t":"Vendor-specific lock-in to a single model provider","w":"Conflicts with interoperability and exit obligations."},{"p":"W","t":"Replacing professional assurance roles","w":"The toolkit supports specialists; it does not substitute for them."}]};
  window.PAUT = PAUT; window.PAUT_CONFIG = PAUT_CONFIG;
  /* ------------------------------------------------------------------
   * 3. HELPERS
   * ------------------------------------------------------------------ */
  var $ = function (id) { return document.getElementById(id); };
  var val = function (id) { var e = $(id); return e ? String(e.value).trim() : ''; };
  var esc = function (s) {
    return String(s == null ? '' : s).replace(/[<>&]/g, function (c) {
      return { '<': '&lt;', '>': '&gt;', '&': '&amp;' }[c];
    });
  };
  var today = function () { return new Date().toISOString().slice(0, 10); };
  var on = function (el, ev, fn) { if (el) el.addEventListener(ev, fn); };

  document.documentElement.classList.add('js');

  /* ------------------------------------------------------------------
   * 4. USER PREFERENCES — theme, contrast, text size. Stored locally only.
   * ------------------------------------------------------------------ */
  var store = {
    get: function (k, d) { try { return localStorage.getItem('paut.' + k) || d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem('paut.' + k, v); } catch (e) {} }
  };
  var root = document.documentElement;

  function buildHeaderTools() {
    var tools = document.querySelector('.hdr-tools');
    if (!tools) return;
    tools.innerHTML =
      '<button class="icon-btn" id="searchBtn" type="button" aria-expanded="false" aria-controls="searchPanel" title="Search this page">&#128269; Search</button>' +
      '<button class="icon-btn" id="themeBtn" type="button" aria-pressed="false" title="Switch between light and dark appearance">&#127768; Dark</button>' +
      '<button class="icon-btn" id="contrastBtn" type="button" aria-pressed="false" title="High contrast mode">&#9689; Contrast</button>' +
      '<button class="icon-btn" id="textBtn" type="button" aria-pressed="false" title="Larger text">A+ Text</button>' +
      '<button class="icon-btn no-print" id="printBtn" type="button" title="Print or save as PDF">&#128424; Print</button>';
  }

  function applyPrefs() {
    var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    var t = store.get('theme', prefersDark ? 'dark' : 'light');
    var c = store.get('contrast', 'normal');
    var d = store.get('density', 'normal');
    root.setAttribute('data-theme', t);
    root.setAttribute('data-contrast', c);
    root.setAttribute('data-density', d);
    var tb = $('themeBtn');
    if (tb) {
      tb.setAttribute('aria-pressed', String(t === 'dark'));
      tb.innerHTML = (t === 'dark' ? '&#9728;&#65039; ' : '&#127768; ') +
        '<span class="visually-hidden">Switch to </span>' + (t === 'dark' ? 'Light' : 'Dark');
    }
    if ($('contrastBtn')) $('contrastBtn').setAttribute('aria-pressed', String(c === 'high'));
    if ($('textBtn')) $('textBtn').setAttribute('aria-pressed', String(d === 'comfortable'));
  }

  function initPrefs() {
    buildHeaderTools();
    on($('themeBtn'), 'click', function () { store.set('theme', root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'); applyPrefs(); });
    on($('contrastBtn'), 'click', function () { store.set('contrast', root.getAttribute('data-contrast') === 'high' ? 'normal' : 'high'); applyPrefs(); });
    on($('textBtn'), 'click', function () { store.set('density', root.getAttribute('data-density') === 'comfortable' ? 'normal' : 'comfortable'); applyPrefs(); });
    on($('printBtn'), 'click', function () {
      var opened = [];
      Array.prototype.forEach.call(document.querySelectorAll('details'), function (d) { if (!d.open) { opened.push(d); d.open = true; } });
      window.print();
      setTimeout(function () { opened.forEach(function (d) { d.open = false; }); }, 800);
    });
    applyPrefs();
  }

  /* ------------------------------------------------------------------
   * 5. NAVIGATION — mobile menu, scroll spy, progress, back to top.
   * ------------------------------------------------------------------ */
  function initNav() {
    var toggle = $('navToggle'), nav = $('primary-nav');
    if (toggle && nav) {
      on(toggle, 'click', function () {
        var open = nav.classList.toggle('open');
        toggle.setAttribute('aria-expanded', String(open));
      });
      Array.prototype.forEach.call(nav.querySelectorAll('a'), function (a) {
        on(a, 'click', function () { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); });
      });
    }
    var bar = document.createElement('div');
    bar.id = 'read-progress'; bar.setAttribute('aria-hidden', 'true');
    document.body.insertBefore(bar, document.body.firstChild);
    var top = document.createElement('a');
    top.href = '#top'; top.className = 'btn btn-primary btn-sm back-to-top no-print';
    top.textContent = '↑ Top'; top.style.display = 'none';
    top.setAttribute('aria-label', 'Back to the top of the page');
    document.body.appendChild(top);
    var ids = nav ? Array.prototype.map.call(nav.querySelectorAll('a'), function (a) { return a.getAttribute('href').slice(1); }) : [];
    function onScroll() {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
      top.style.display = h.scrollTop > 600 ? 'inline-flex' : 'none';
      var cur = null;
      ids.forEach(function (id) { var el = $(id); if (el && el.getBoundingClientRect().top <= 140) cur = id; });
      if (nav) Array.prototype.forEach.call(nav.querySelectorAll('a'), function (a) {
        a.setAttribute('aria-current', a.getAttribute('href') === '#' + cur ? 'true' : 'false');
      });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* Deep links: open any <details> targeted by the URL hash or an internal link. */
  function initDeepLinks() {
    function openTarget() {
      var id = location.hash.slice(1);
      if (!id) return;
      var el = $(id);
      if (!el) return;
      var p = el;
      while (p) { if (p.tagName === 'DETAILS') p.open = true; p = p.parentElement; }
      if (el.tagName === 'DETAILS') el.open = true;
      setTimeout(function () { el.scrollIntoView({ block: 'start' }); }, 60);
    }
    window.addEventListener('hashchange', openTarget);
    openTarget();
    document.body.addEventListener('click', function (e) {
      var a = e.target.closest ? e.target.closest('a[href^="#"]') : null;
      if (!a) return;
      var href = a.getAttribute('href');
      if (href.length < 2) return;
      var el = $(href.slice(1));
      if (el && el.tagName === 'DETAILS') el.open = true;
    });
  }

  /* External links get rel hardening and a screen-reader hint. */
  function initExternalLinks() {
    Array.prototype.forEach.call(document.querySelectorAll('a[href^="http"]'), function (a) {
      if (a.hostname === location.hostname) return;
      a.setAttribute('rel', 'noopener noreferrer');
      if (!a.querySelector('.ext')) {
        var s = document.createElement('span');
        s.className = 'ext visually-hidden';
        s.textContent = ' (opens an external website)';
        a.appendChild(s);
      }
    });
  }
  /* ------------------------------------------------------------------
   * 6. PAGE SEARCH
   * ------------------------------------------------------------------ */
  function initSearch() {
    var header = document.querySelector('.site-header');
    if (!header) return;
    var panel = document.createElement('div');
    panel.className = 'wrap no-print js-only';
    panel.id = 'searchPanel';
    panel.hidden = true;
    panel.style.paddingBottom = '14px';
    panel.innerHTML =
      '<div class="field" style="margin:0">' +
      '<label for="siteSearch">Search this page</label>' +
      '<span class="hint" id="ssHint">Press <kbd>/</kbd> to jump here. Non-matching sections are hidden while you search.</span>' +
      '<input type="search" id="siteSearch" aria-describedby="ssHint" placeholder="Search all guidance, tools and resources on this page">' +
      '<p class="count-note" id="ssCount" role="status" aria-live="polite"></p></div>';
    header.appendChild(panel);
    var input = $('siteSearch'), btn = $('searchBtn');
    function runSearch() {
      var q = input.value.trim().toLowerCase();
      var secs = document.querySelectorAll('main > section');
      if (q.length < 2) {
        Array.prototype.forEach.call(secs, function (s) { s.hidden = false; });
        $('ssCount').textContent = '';
        return;
      }
      var hits = 0;
      Array.prototype.forEach.call(secs, function (s) {
        var match = s.textContent.toLowerCase().indexOf(q) !== -1;
        s.hidden = !match;
        if (match) hits++;
      });
      $('ssCount').textContent = hits + ' section' + (hits === 1 ? '' : 's') + ' match “' + input.value.trim() + '”.' +
        (hits ? ' Clear the box to show everything again.' : ' Try a shorter or more general term.');
    }
    on(input, 'input', runSearch);
    on(btn, 'click', function () {
      var open = panel.hidden;
      panel.hidden = !open;
      btn.setAttribute('aria-expanded', String(open));
      if (open) { input.focus(); } else { input.value = ''; runSearch(); }
    });
    document.addEventListener('keydown', function (e) {
      var tag = document.activeElement ? document.activeElement.tagName : '';
      if (e.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test(tag)) {
        e.preventDefault(); panel.hidden = false;
        if (btn) btn.setAttribute('aria-expanded', 'true');
        input.focus();
      }
      if (e.key === 'Escape' && document.activeElement === input) {
        input.value = ''; runSearch(); input.blur();
      }
    });
  }

  /* ------------------------------------------------------------------
   * 7. TOOLKIT AND RESOURCE FILTERING
   * ------------------------------------------------------------------ */
  var CAT = { governance: 'Governance', delivery: 'Delivery', assurance: 'Assurance', future: 'Future-ready' };
  var EFF = { S: 'Small effort', M: 'Medium effort', L: 'Large effort' };
  var TYPE = { law: 'Law', standard: 'Standard', policy: 'Policy', guidance: 'Guidance', toolkit: 'Toolkit', tool: 'Tool', research: 'Research' };

  function initToolkit() {
    var grid = $('tkGrid'), search = $('tkSearch'), cat = $('tkCat');
    if (!grid) return;
    function render() {
      var q = search ? search.value.toLowerCase().trim() : '';
      var c = cat ? cat.value : 'all';
      var items = PAUT.toolkit.filter(function (a) {
        var inCat = (c === 'all' || a.cat === c);
        var hay = (a.t + ' ' + a.w + ' ' + a.out + ' ' + a.links.map(function (l) { return l[0]; }).join(' ')).toLowerCase();
        return inCat && (!q || hay.indexOf(q) !== -1);
      });
      grid.innerHTML = items.map(function (a) {
        return '<article class="card">' +
          '<div class="tags"><span class="tag t-gov">' + a.id + '</span><span class="tag">' + CAT[a.cat] + '</span><span class="tag">' + EFF[a.eff] + '</span>' +
          (a.live ? '<span class="tag t-ok">Live tool</span>' : '') + '</div>' +
          '<h3>' + esc(a.t) + '</h3><p>' + esc(a.w) + '</p>' +
          '<p style="font-size:.85rem;margin:0"><strong>Output:</strong> ' + esc(a.out) + '</p>' +
          '<p style="font-size:.85rem;margin:0"><strong>Anchored to:</strong> ' + a.links.map(function (l) {
            return '<a href="' + l[1] + '" rel="noopener noreferrer">' + esc(l[0]) + '</a>';
          }).join(', ') + '</p>' +
          (a.live ? '<p style="margin-top:6px"><a class="btn btn-secondary btn-sm" href="' + a.live + '">Open the tool</a></p>' : '') +
          '</article>';
      }).join('');
      if ($('tkCount')) $('tkCount').textContent = 'Showing ' + items.length + ' of ' + PAUT.toolkit.length + ' toolkit assets.';
      if ($('tkEmpty')) $('tkEmpty').hidden = items.length > 0;
    }
    on(search, 'input', render);
    on(cat, 'change', render);
    render();
  }

  function initResources() {
    var body = $('resBody');
    if (!body) return;
    var topic = 'all';
    function tierClass(t) { return t === 0 ? 't-risk' : t === 1 ? 't-gov' : t === 2 ? 't-ok' : ''; }
    function render() {
      var q = $('resSearch') ? $('resSearch').value.toLowerCase().trim() : '';
      var ty = $('resType') ? $('resType').value : 'all';
      var rows = PAUT.resources.filter(function (r) {
        var okType = (ty === 'all' || r.c === ty);
        var okTopic = (topic === 'all' || r.tags.indexOf(topic) !== -1);
        var hay = (r.t + ' ' + r.o + ' ' + r.w + ' ' + r.tags.join(' ')).toLowerCase();
        return okType && okTopic && (!q || hay.indexOf(q) !== -1);
      });
      body.innerHTML = rows.length ? rows.map(function (r) {
        return '<tr><td><a href="' + r.u + '" rel="noopener noreferrer">' + esc(r.t) + '</a>' +
          '<div class="tags" style="margin-top:5px">' + r.tags.slice(0, 3).map(function (t) { return '<span class="tag">' + esc(t) + '</span>'; }).join('') + '</div></td>' +
          '<td>' + esc(r.o) + '</td><td>' + TYPE[r.c] + '</td>' +
          '<td><span class="tag ' + tierClass(r.tier) + '">Tier ' + r.tier + '</span></td>' +
          '<td>' + esc(r.w) + '</td></tr>';
      }).join('') : '<tr><td colspan="5">No resources match. Try a broader search or reset the filters.</td></tr>';
      if ($('resCount')) $('resCount').textContent = 'Showing ' + rows.length + ' of ' + PAUT.resources.length + ' resources.';
    }
    on($('resSearch'), 'input', render);
    on($('resType'), 'change', render);
    Array.prototype.forEach.call(document.querySelectorAll('.chip[data-topic]'), function (b) {
      on(b, 'click', function () {
        Array.prototype.forEach.call(document.querySelectorAll('.chip[data-topic]'), function (x) { x.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true');
        topic = b.getAttribute('data-topic');
        render();
      });
    });
    render();
  }

  function initRoadmap() {
    var grid = $('mosGrid');
    if (!grid) return;
    var NAME = { M: 'Must have', S: 'Should have', C: 'Could have', W: "Won't have (this time)" };
    var filter = 'all';
    function render() {
      var items = PAUT.moscow.filter(function (m) { return filter === 'all' || m.p === filter; });
      grid.innerHTML = items.map(function (m) {
        var cls = m.p === 'M' ? 't-risk' : m.p === 'S' ? 't-warn' : m.p === 'C' ? 't-gov' : '';
        return '<article class="card moscow-' + m.p + '"><span class="tag ' + cls + '">' + NAME[m.p] + '</span>' +
          '<h3>' + esc(m.t) + '</h3><p>' + esc(m.w) + '</p></article>';
      }).join('');
    }
    Array.prototype.forEach.call(document.querySelectorAll('.chip.mos'), function (b) {
      on(b, 'click', function () {
        Array.prototype.forEach.call(document.querySelectorAll('.chip.mos'), function (x) { x.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true');
        filter = b.getAttribute('data-mos');
        render();
      });
    });
    render();
  }

  function initGlossary() {
    var list = $('glList'), search = $('glSearch');
    if (!list) return;
    function render() {
      var q = search ? search.value.toLowerCase().trim() : '';
      var items = PAUT.glossary.filter(function (g) { return !q || (g[0] + ' ' + g[1]).toLowerCase().indexOf(q) !== -1; });
      list.innerHTML = items.length ? items.map(function (g) {
        return '<div><dt style="font-weight:700">' + esc(g[0]) + '</dt>' +
          '<dd style="margin:2px 0 0;color:var(--c-text-muted);font-size:.93rem">' + esc(g[1]) + '</dd></div>';
      }).join('') : '<p>No matching terms.</p>';
    }
    on(search, 'input', render);
    render();
  }
  /* ------------------------------------------------------------------
   * 8. INTERACTIVE TOOLS — all client-side. Nothing is transmitted.
   * ------------------------------------------------------------------ */
  function initTriage() {
    var go = $('triageGo');
    if (!go) return;
    on(go, 'click', function () {
      var score = Number(val('tr-audience')) + Number(val('tr-impact')) + Number(val('tr-data')) + Number(val('tr-rev'));
      var flags = [];
      var checks = [
        ['tr-c1', 'informs or automates a decision about a person'],
        ['tr-c2', 'will be published or is disclosable under freedom of information law'],
        ['tr-c3', 'reaches production code or infrastructure'],
        ['tr-c4', 'contains specialist statistical, legal, clinical, financial or safety content'],
        ['tr-c5', 'involves autonomous agent action using tools or credentials'],
        ['tr-c6', 'is outside your professional competence']
      ];
      checks.forEach(function (c) {
        var el = $(c[0]);
        if (el && el.checked) { score += Number(el.value); flags.push(c[1]); }
      });
      var level = score <= 1 ? 0 : score <= 4 ? 1 : score <= 8 ? 2 : score <= 13 ? 3 : score <= 18 ? 4 : 5;
      // Hard floors: some factors cannot be scored away.
      if ($('tr-c1') && $('tr-c1').checked && level < 4) level = 4;
      if ($('tr-c5') && $('tr-c5').checked && level < 3) level = 3;
      if (Number(val('tr-data')) >= 3 && level < 3) level = 3;
      var L = PAUT.hlevels[level];
      var extra = [];
      if ($('tr-c3').checked) extra.push('Security review and dependency scanning before merge (Secure by Design, NIST SSDF).');
      if ($('tr-c2').checked) extra.push('Accessibility check to WCAG 2.2 AA and plain-language review before publication.');
      if (Number(val('tr-data')) >= 2) extra.push('Confirm the lawful basis and whether a DPIA is required (ICO guidance).');
      if (Number(val('tr-data')) >= 3) extra.push('Special category data: a DPIA is almost certainly mandatory. Consult your DPO before proceeding.');
      if ($('tr-c1').checked) extra.push('Publish an ATRS transparency record and complete an equality impact assessment.');
      if ($('tr-c4').checked) extra.push('A named subject-matter specialist must sign off. Do not rely on generalist review.');
      if ($('tr-c5').checked) extra.push('Bound the agent: least-privilege credentials, an allow-list of tools, explicit prohibited actions and a named kill-switch owner.');
      if ($('tr-c6').checked) extra.push('Pair with someone competent in the subject, or route the task to them entirely.');
      $('triageOut').innerHTML =
        '<p><span class="badge-h">' + L.h + '</span> <strong>' + esc(L.n) + '</strong> &nbsp;<span class="tag">score ' + score + '</span></p>' +
        '<p>' + esc(L.d) + '</p>' +
        '<p><strong>Typical examples:</strong> ' + esc(L.ex) + '<br><strong>Evidence to keep:</strong> ' + esc(L.ev) + '</p>' +
        (flags.length ? '<p><strong>Escalating factors:</strong> ' + flags.map(esc).join('; ') + '.</p>' : '') +
        (extra.length ? '<p><strong>Additional required actions</strong></p><ul class="clean">' + extra.map(function (e) { return '<li>&bull; ' + esc(e) + '</li>'; }).join('') + '</ul>' : '') +
        '<p class="count-note">Triage sets a floor, not a ceiling. If you are uneasy, raise the level. Never self-approve at H3 or above.</p>' +
        '<p class="count-note"><em>Artefact: ' + esc(val('tr-what') || 'unnamed') + ' · Assessed ' + today() + '</em></p>';
    });
  }

  function initEvidence() {
    var go = $('evGo');
    if (!go) return;
    on(go, 'click', function () {
      var sources = val('ev-sources').split('\n').filter(Boolean);
      var hl = PAUT.hlevels.filter(function (x) { return x.h === val('ev-h'); })[0];
      var md = [
        '## AI-use declaration and evidence record', '',
        '- **Artefact / reference:** ' + (val('ev-art') || '[add reference]'),
        '- **Declared by:** ' + (val('ev-role') || '[your role]'),
        '- **Date:** ' + today(),
        '- **Tool and model version:** ' + (val('ev-tool') || '[tool and version]'),
        '- **Human review level applied:** ' + val('ev-h') + ' — ' + (hl ? hl.n : ''), '',
        '### Extent of AI assistance',
        val('ev-extent') || '[Describe precisely what AI did and what you did.]', '',
        '### Sources consulted and verified',
        sources.length ? sources.map(function (s) { return '- ' + s; }).join('\n') : '- [List every source you opened and confirmed]', '',
        '### Checks performed',
        val('ev-checks') || '[List the verification steps you actually carried out.]', '',
        '### Human review',
        '- **Reviewer(s):** ' + (val('ev-rev') || '[Named reviewer and role — must not be the author at H3 and above]'),
        '- **Residual risk / limitations:** ' + (val('ev-res') || '[State what remains unverified]'), '',
        '### Accountability statement',
        'I remain accountable for this output. AI assistance did not confer any authority I do not hold. All factual claims have been traced to a cited source, and no unauthorised personal or sensitive data was entered into the tool.'
      ].join('\n');
      $('evOut').innerHTML = '<div class="code-block"><pre>' + esc(md) + '</pre></div>';
    });
  }

  function initDeia() {
    var go = $('deiaGo');
    if (!go) return;
    var MAP = {
      de1: ['Differential impact by protected characteristic', 'Complete a full equality impact assessment and record your due regard under the Public Sector Equality Duty before the change goes live.', 'https://www.equalityhumanrights.com/guidance/public-sector-equality-duty'],
      de2: ['Representation gap in data or sources', 'Document known data gaps, test outputs across affected groups, and state the limitation publicly. Do not present outputs as universally valid.', 'https://arxiv.org/abs/1803.09010'],
      de3: ['Public or assistive technology audience', 'Test to WCAG 2.2 AA with real assistive technology, and publish an accessibility statement covering the change.', 'https://www.w3.org/TR/WCAG22/'],
      de4: ['Digital exclusion', 'Provide and resource an assisted digital route. Measure its use — do not assume nobody needs it.', 'https://www.gov.uk/service-manual/helping-people-to-use-your-service'],
      de5: ['Vulnerability and safeguarding', 'Add a safeguarding review, a human escalation route that cannot be bypassed, and staff guidance on recognising crisis signals.', 'https://www.gov.uk/service-manual/user-research'],
      de6: ['Language and literacy barrier', 'Target reading age 9, use the GOV.UK style guide, and offer Easy Read and translated formats.', 'https://www.gov.uk/guidance/style-guide'],
      de7: ['Reduced human contact', 'Retain a non-digital contact route and evidence that removing it would not disadvantage any group.', 'https://www.gov.uk/service-manual/service-standard'],
      de8: ['No route to challenge', 'Design and publish a redress route before launch. An unchallengeable automated outcome is a legal and ethical failure.', 'https://www.gov.uk/government/collections/algorithmic-transparency-recording-standard-hub'],
      de9: ['Alternative formats and Welsh language', 'Plan and budget for Welsh, Easy Read, BSL and large print from the start, not as a retrofit.', 'https://www.gov.uk/guidance/style-guide'],
      de10: ['Untested with disabled users', 'Recruit disabled participants and assistive technology users now. Automated tools find under a third of real barriers.', 'https://www.gov.uk/service-manual/user-research/running-research-sessions-with-people-with-disabilities']
    };
    on(go, 'click', function () {
      var hits = Object.keys(MAP).filter(function (k) { return $(k) && $(k).checked; });
      var n = hits.length;
      var verdict = n === 0 ? ['No flags raised', 'ok', 'Record that you screened this and found no impact. Re-screen if scope, data or audience changes.']
        : n <= 2 ? ['Targeted mitigation needed', 'warn', 'Address the flagged items and record the decision. A full assessment may not be needed if no protected characteristic is engaged.']
        : n <= 5 ? ['Full equality impact assessment required', 'warn', 'Engage your equality, accessibility and inclusion specialists now, before build decisions harden.']
        : ['High DEIA risk — do not proceed without specialist sign-off', 'risk', 'Escalate to the accountable owner. This change should not go live on a self-assessment.'];
      $('deiaOut').innerHTML =
        '<div class="callout ' + verdict[1] + '" style="margin-bottom:14px"><p><strong>' + verdict[0] + '</strong> — ' + verdict[2] + '</p></div>' +
        '<p><strong>Change screened:</strong> ' + esc(val('de-what') || '[unnamed change]') + ' · ' + n + ' of 10 flags raised · ' + today() + '</p>' +
        (n ? '<ol class="steps">' + hits.map(function (k) {
          return '<li><strong>' + esc(MAP[k][0]) + '</strong><br>' + esc(MAP[k][1]) + '<br><a href="' + MAP[k][2] + '" rel="noopener noreferrer">Guidance &rarr;</a></li>';
        }).join('') + '</ol>' : '') +
        '<p class="count-note">Screening evidences due regard; it does not discharge it. Keep this record with the change.</p>';
    });
  }

  function initAtrs() {
    var go = $('atGo');
    if (!go) return;
    on(go, 'click', function () {
      var md = [
        '# Algorithmic transparency record', '',
        '## Tier 1 — summary',
        '- **Name:** ' + (val('at-name') || '[tool name]'),
        '- **Organisation and accountable owner:** ' + (val('at-org') || '[organisation, named owner]'),
        '- **Published:** ' + today(),
        '- **What it does:** ' + (val('at-purpose') || '[plain-English description]'),
        '- **Role in decision-making:** ' + val('at-role'),
        '- **Scale of use:** ' + (val('at-scale') || '[volume and frequency]'), '',
        '## Tier 2 — detail',
        '### Why we use it',
        '[Problem it solves, alternatives considered, why an algorithmic approach is proportionate.]', '',
        '### How it works',
        '[Model or logic type, inputs, outputs, key limitations, how outputs are presented to staff.]', '',
        '### Data',
        val('at-data') || '[Data categories, sources, personal or special category status, retention, DPIA reference.]', '',
        '### Human oversight',
        '- Review level applied: [H0-H5 from the triage tool]',
        '- Who reviews, what they can change, and how an override is recorded',
        '- No self-approval for material or high-risk outputs', '',
        '### Risks and mitigations',
        val('at-risk') || '[Bias, accuracy, accessibility, security, prompt injection, over-reliance — and what you do about each.]', '',
        '### Equality and accessibility',
        '[Equality impact assessment reference, accessibility conformance, assisted digital provision, alternative formats.]', '',
        '### How to question or challenge an outcome',
        val('at-redress') || '[Contact route, timescales, escalation and appeal rights.]', '',
        '### Review',
        '- Next review date: [date]',
        '- Contact: [team inbox]', '',
        '*Prepared using the Public AI Utility Toolkit. Align the final wording to the current ATRS template before publication.*'
      ].join('\n');
      $('atOut').innerHTML = '<div class="code-block"><pre>' + esc(md) + '</pre></div>' +
        '<p class="count-note">Check the current template at the <a href="https://www.gov.uk/government/collections/algorithmic-transparency-recording-standard-hub" rel="noopener noreferrer">ATRS hub</a> before publishing.</p>';
    });
  }
  function initPqc() {
    var go = $('pqGo');
    if (!go) return;
    on(go, 'click', function () {
      var score = Number(val('pq-life'));
      var factors = [];
      ['pq1', 'pq2', 'pq3', 'pq4', 'pq5', 'pq6'].forEach(function (id) {
        var el = $(id);
        if (el && el.checked) {
          score += Number(el.value);
          var lab = document.querySelector('label[for="' + id + '"]');
          factors.push(lab ? lab.textContent : id);
        }
      });
      var band = score <= 2 ? ['Low exposure', 'ok'] : score <= 6 ? ['Moderate exposure', 'warn'] : score <= 11 ? ['High exposure', 'warn'] : ['Critical exposure', 'risk'];
      var actions = [
        'Build a cryptographic inventory: algorithms, key sizes, certificates, protocols, libraries, hardware and suppliers.',
        'Identify long-life data now — anything that must stay confidential past 2035 is already exposed to harvest-now-decrypt-later.',
        'Design for crypto-agility: no hard-coded algorithms, centralised crypto services and tested rotation procedures.',
        'Set supplier expectations: ask for post-quantum roadmaps and contractually require migration support.',
        'Align to NCSC milestones: discovery and plan by 2028, highest-priority migration by 2031, full migration by 2035.',
        'Target NIST-standardised algorithms (ML-KEM for key establishment, ML-DSA or SLH-DSA for signatures).'
      ];
      $('pqOut').innerHTML =
        '<div class="callout ' + band[1] + '"><p><strong>' + band[0] + '</strong> — score ' + score + '. ' +
        (score > 6 ? 'Start migration planning this financial year.' : 'Maintain awareness and re-assess annually, or whenever data lifetimes change.') + '</p></div>' +
        (factors.length ? '<p><strong>Contributing factors</strong></p><ul class="clean">' + factors.map(function (f) { return '<li>&bull; ' + esc(f) + '</li>'; }).join('') + '</ul>' : '') +
        '<p><strong>Recommended actions</strong></p><ol class="steps">' + actions.map(function (a) { return '<li>' + esc(a) + '</li>'; }).join('') + '</ol>' +
        '<p class="count-note">Sources: <a href="https://www.ncsc.gov.uk/collection/post-quantum-cryptography" rel="noopener noreferrer">NCSC post-quantum collection</a> · ' +
        '<a href="https://csrc.nist.gov/projects/post-quantum-cryptography" rel="noopener noreferrer">NIST PQC standards</a>. Assessed ' + today() + '.</p>';
    });
  }

  function initReadability() {
    var go = $('rdGo');
    if (!go) return;
    var JARGON = ['utilise', 'leverage', 'facilitate', 'commence', 'endeavour', 'in order to', 'going forward', 'stakeholder', 'synergy', 'robust', 'deliverable', 'ring-fenced', 'deep dive', 'key learnings', 'moving forward', 'onboarding', 'touch base', 'best practice', 'holistic', 'paradigm', 'streamline', 'optimise', 'granular', 'proactive', 'cascade', 'landscape', 'ecosystem', 'aforementioned', 'notwithstanding', 'pursuant to', 'prior to', 'in the event that'];
    var NON_INCLUSIVE = [['the disabled', 'disabled people'], ['suffers from', 'has'], ['wheelchair-bound', 'wheelchair user'], ['the elderly', 'older people'], ['able-bodied', 'non-disabled'], ['man hours', 'person hours'], ['manpower', 'workforce'], ['blacklist', 'blocklist'], ['whitelist', 'allowlist'], ['sanity check', 'quick check'], ['guys', 'everyone'], ['chairman', 'chair'], ['handicapped', 'disabled'], ['confined to a wheelchair', 'wheelchair user'], ['grandfathered', 'legacy'], ['normal people', 'people without a disability']];
    function syllables(w) {
      w = w.toLowerCase().replace(/[^a-z]/g, '');
      if (w.length <= 3) return 1;
      w = w.replace(/(?:[^laeiouy]es|ed|[^laeiouy]e)$/, '').replace(/^y/, '');
      return (w.match(/[aeiouy]{1,2}/g) || ['x']).length;
    }
    on(go, 'click', function () {
      var t = $('rdText').value.trim();
      if (!t) { $('rdOut').innerHTML = '<p style="margin:0">Paste some content first.</p>'; return; }
      var sents = t.split(/[.!?]+(?:\s|$)/).filter(function (x) { return x.trim().length > 1; });
      var words = t.match(/[A-Za-z’'\-]+/g) || [];
      var syl = words.reduce(function (a, w) { return a + syllables(w); }, 0);
      var W = words.length || 1, S = sents.length || 1;
      var fre = 206.835 - 1.015 * (W / S) - 84.6 * (syl / W);
      var fk = 0.39 * (W / S) + 11.8 * (syl / W) - 15.59;
      var raw = Math.max(5, Math.round(fk + 5));
      var ageTxt = raw >= 21 ? '21+' : String(raw);
      var longS = sents.filter(function (x) { return (x.match(/[A-Za-z’'\-]+/g) || []).length > 25; }).length;
      var lc = t.toLowerCase();
      var jHits = JARGON.filter(function (j) { return lc.indexOf(j) !== -1; });
      var nHits = NON_INCLUSIVE.filter(function (p) { return lc.indexOf(p[0]) !== -1; });
      var passive = (t.match(/\b(?:is|are|was|were|be|been|being)\s+\w+(?:ed|en)\b/gi) || []).length;
      var acronyms = (t.match(/\b[A-Z]{2,6}\b/g) || []).filter(function (a, i, arr) {
        return arr.indexOf(a) === i && ['AI', 'UK', 'EU', 'US', 'IT', 'OK'].indexOf(a) === -1;
      });
      var grade = raw <= 9 ? ['ok', 'Meets the GOV.UK target of reading age 9.']
        : raw <= 12 ? ['warn', 'Above the GOV.UK target. Shorten sentences and replace long words.']
        : ['risk', 'Too difficult for a general public audience. Rewrite before publishing.'];
      $('rdOut').innerHTML =
        '<div class="callout ' + grade[0] + '"><p><strong>Estimated reading age ' + ageTxt + '</strong> — ' + grade[1] + '</p></div>' +
        '<div class="table-scroll"><table><caption>Content metrics</caption><thead><tr><th scope="col">Measure</th><th scope="col">Value</th><th scope="col">Target</th></tr></thead><tbody>' +
        '<tr><td>Words / sentences</td><td>' + W + ' / ' + S + '</td><td>&mdash;</td></tr>' +
        '<tr><td>Average sentence length</td><td>' + (W / S).toFixed(1) + ' words</td><td>Under 20</td></tr>' +
        '<tr><td>Flesch reading ease</td><td>' + Math.max(0, Math.round(fre)) + '</td><td>60 or above</td></tr>' +
        '<tr><td>Sentences over 25 words</td><td>' + longS + '</td><td>0</td></tr>' +
        '<tr><td>Possible passive constructions</td><td>' + passive + '</td><td>Minimise</td></tr>' +
        '<tr><td>Unexplained acronyms</td><td>' + (acronyms.length ? esc(acronyms.join(', ')) : 'none found') + '</td><td>Expand on first use</td></tr>' +
        '</tbody></table></div>' +
        (jHits.length ? '<p style="margin-top:14px"><strong>Jargon and officialese to replace:</strong> ' + jHits.map(esc).join(', ') + '.</p>' : '<p style="margin-top:14px">No common officialese detected.</p>') +
        (nHits.length ? '<div class="callout risk"><p><strong>Non-inclusive language found.</strong> ' + nHits.map(function (p) { return '“' + esc(p[0]) + '” → use “' + esc(p[1]) + '”'; }).join('; ') + '.</p></div>' : '<p>No flagged non-inclusive phrases detected.</p>') +
        '<p class="count-note">Automated readability is an indicator only. Test real content with real users, and follow the <a href="https://www.gov.uk/guidance/style-guide" rel="noopener noreferrer">GOV.UK style guide</a>.</p>';
    });
  }

  /* Copy and reset buttons shared across all tools. */
  function initCopyReset() {
    document.addEventListener('click', function (e) {
      if (!e.target.closest) return;
      var copy = e.target.closest('[data-copy]');
      var reset = e.target.closest('[data-reset]');
      if (copy) {
        var box = $(copy.getAttribute('data-copy'));
        if (!box) return;
        var text = box.innerText;
        var label = copy.textContent;
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(function () {
            copy.textContent = '✓ Copied';
            setTimeout(function () { copy.textContent = label; }, 1800);
          }, function () { copy.textContent = 'Select and copy manually'; });
        }
      }
      if (reset) {
        var out = $(reset.getAttribute('data-reset'));
        if (!out) return;
        var scope = out.closest('.details-body') || out.parentElement;
        Array.prototype.forEach.call(scope.querySelectorAll('input, textarea, select'), function (i) {
          if (i.type === 'checkbox' || i.type === 'radio') i.checked = false;
          else if (i.tagName === 'SELECT') i.selectedIndex = 0;
          else i.value = '';
        });
        out.innerHTML = '<p style="margin:0;color:var(--c-text-muted)">Cleared. Your result will appear here.</p>';
      }
    });
  }
  /* ------------------------------------------------------------------
   * 9. CONTACT AND FEEDBACK ROUTING
   * Nothing is transmitted from this page. The form composes a message and
   * hands it to the user's own mail client, clipboard, or GitHub.
   * ------------------------------------------------------------------ */
  function maskEmail(addr) {
    if (!addr) return '';
    var parts = addr.split('@');
    if (parts.length !== 2) return addr;
    var u = parts[0], d = parts[1];
    var mu = u.length <= 2 ? u.charAt(0) + '•' : u.slice(0, 2) + new Array(Math.max(2, u.length - 3) + 1).join('•') + u.slice(-1);
    var seg = d.split('.');
    seg[0] = seg[0].length <= 2 ? seg[0] : seg[0].slice(0, 2) + new Array(Math.max(2, seg[0].length - 2) + 1).join('•');
    return mu + '@' + seg.join('.');
  }

  function initContact() {
    var repoUrl = 'https://github.com/' + PAUT_CONFIG.repo;
    var mailbox = PAUT_CONFIG.mailbox || '';

    if ($('a11ySla')) $('a11ySla').textContent = 'Target first response: ' + PAUT_CONFIG.responseDays + ' working days.';
    if ($('secLink')) $('secLink').href = repoUrl + '/security/policy';
    if ($('discussLink')) $('discussLink').href = repoUrl + '/issues';
    Array.prototype.forEach.call(document.querySelectorAll('[data-issue]'), function (a) {
      a.href = repoUrl + '/issues/new?template=' + a.getAttribute('data-issue');
      a.setAttribute('rel', 'noopener noreferrer');
    });

    var state = $('mailboxState');
    if (state) {
      if (mailbox) {
        state.className = 'callout ok';
        state.innerHTML = '<p><strong>Team mailbox:</strong> <span id="mbMask">' +
          (PAUT_CONFIG.maskMailbox ? maskEmail(mailbox) : mailbox) + '</span> ' +
          '<button type="button" class="btn btn-secondary btn-sm js-only" id="revealMb">Reveal full address</button> ' +
          'The address is masked on screen and assembled only when you ask for it, to reduce automated harvesting.</p>';
        document.addEventListener('click', function (e) {
          if (e.target && e.target.id === 'revealMb') {
            $('mbMask').textContent = mailbox;
            e.target.parentNode.removeChild(e.target);
          }
        });
      } else {
        state.className = 'callout warn';
        state.innerHTML = '<p><strong>The team mailbox is not configured yet.</strong> Until it is set, this form will prepare your message so you can copy it, or route it to GitHub. ' +
          'Maintainers: set <code>PAUT_CONFIG.mailbox</code> at the top of <code>app.js</code>.</p>';
      }
    }

    var form = $('contactForm');
    if (!form) return;

    function build() {
      return {
        subject: '[Public AI Utility Toolkit] ' + (val('cf-cat') || 'Enquiry') + (val('cf-subject') ? ' — ' + val('cf-subject') : ''),
        body: [
          'Category: ' + val('cf-cat'),
          'Subject: ' + (val('cf-subject') || '(not given)'),
          'Page or section: ' + (val('cf-page') || '(not given)'),
          'Assistive technology: ' + (val('cf-at') || '(not given)'),
          '', 'Message:', (val('cf-msg') || '(no message entered)'), '',
          '---',
          'From: ' + (val('cf-name') || '(anonymous)'),
          'Organisation: ' + (val('cf-org') || '(not given)'),
          'Reply to: ' + (val('cf-email') || '(no reply address given)'),
          'Sent from: ' + location.href,
          'Date: ' + today()
        ].join('\n')
      };
    }
    function validate() {
      var errs = [];
      if (!val('cf-subject')) errs.push('Enter a subject.');
      if (!val('cf-msg')) errs.push('Enter your message.');
      var em = val('cf-email');
      if (em && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)) errs.push('Check the email address — it does not look valid.');
      if (!$('cf-consent').checked) errs.push('Tick the confirmation box before sending.');
      return errs;
    }
    function showErrors(errs) {
      $('cfOut').innerHTML = '<div class="callout risk"><p><strong>There is a problem</strong></p><ul class="clean">' +
        errs.map(function (e) { return '<li>&bull; ' + esc(e) + '</li>'; }).join('') + '</ul></div>';
      $('cfOut').scrollIntoView({ block: 'nearest' });
    }
    function preview(m, note) {
      $('cfOut').innerHTML = (note ? '<div class="callout ok"><p>' + note + '</p></div>' : '') +
        '<p><strong>Subject:</strong> ' + esc(m.subject) + '</p><div class="code-block"><pre>' + esc(m.body) + '</pre></div>';
    }

    on($('cfSend'), 'click', function () {
      var errs = validate();
      if (errs.length) return showErrors(errs);
      var m = build();
      if (mailbox) {
        preview(m, 'Your email client is opening with this message. Nothing has been sent from this page — you send it yourself.');
        window.location.href = 'mailto:' + mailbox + '?subject=' + encodeURIComponent(m.subject) + '&body=' + encodeURIComponent(m.body);
      } else {
        preview(m, 'No mailbox is configured yet. Copy the message below, or open it as a GitHub issue.');
      }
    });
    on($('cfCopy'), 'click', function () {
      var m = build();
      preview(m);
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText('Subject: ' + m.subject + '\n\n' + m.body).then(function () {
          var b = $('cfCopy'), label = b.textContent;
          b.textContent = '✓ Copied';
          setTimeout(function () { b.textContent = label; }, 1800);
        }, function () {});
      }
    });
    on($('cfIssue'), 'click', function () {
      var errs = validate().filter(function (e) { return e.indexOf('confirmation box') === -1; });
      if (errs.length) return showErrors(errs);
      var m = build();
      var body = m.body.replace(/^Reply to: .*$/m, 'Reply to: (removed — do not post contact details in a public issue)');
      preview({ subject: m.subject, body: body }, 'Opening GitHub. Remember: issues are public. Remove anything you would not want indexed.');
      window.open(repoUrl + '/issues/new?title=' + encodeURIComponent(m.subject) + '&body=' + encodeURIComponent(body), '_blank', 'noopener');
    });
    on($('cfReset'), 'click', function () {
      ['cf-name', 'cf-email', 'cf-org', 'cf-subject', 'cf-page', 'cf-msg', 'cf-at'].forEach(function (i) { if ($(i)) $(i).value = ''; });
      if ($('cf-consent')) $('cf-consent').checked = false;
      if ($('cf-cat')) $('cf-cat').selectedIndex = 0;
      $('cfOut').innerHTML = '<p style="margin:0;color:var(--c-text-muted)">A preview of your message will appear here before anything is sent.</p>';
    });
  }

  /* ------------------------------------------------------------------
   * 10. STRUCTURE — label regions for assistive technology.
   * ------------------------------------------------------------------ */
  function initRegions() {
    var n = 0;
    Array.prototype.forEach.call(document.querySelectorAll('main > section'), function (s) {
      var h = s.querySelector('h1, h2');
      if (!h) return;
      if (!h.id) h.id = 'sec-h-' + (++n);
      s.setAttribute('aria-labelledby', h.id);
    });
    if ($('main')) $('main').setAttribute('tabindex', '-1');
  }

  /* ------------------------------------------------------------------
   * 11. BOOTSTRAP
   * ------------------------------------------------------------------ */
  function init() {
    initRegions();
    initPrefs();
    initNav();
    initSearch();
    initDeepLinks();
    initToolkit();
    initResources();
    initRoadmap();
    initGlossary();
    initTriage();
    initEvidence();
    initDeia();
    initAtrs();
    initPqc();
    initReadability();
    initCopyReset();
    initContact();
    initExternalLinks();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
