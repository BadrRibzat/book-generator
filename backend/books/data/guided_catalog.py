from typing import List, Dict
from django.utils.text import slugify


def _clean_description(text: str) -> str:
    stripped = (text or "").strip()
    return stripped[:-1] if stripped.endswith('.') else stripped


def build_prompt(domain_name: str, niche_name: str, description: str) -> str:
    focus = _clean_description(description)
    return (
        f"You are a strategist guiding operators through {niche_name} within the {domain_name} domain. "
        f"Focus on {focus} with actionable frameworks, tooling checklists, and KPI checkpoints."
    )


BASE_STAGES: List[Dict[str, str]] = [
    {
        "title": "Opportunity Snapshot",
        "summary_template": "Assess market demand, adoption drivers, and trend signals for {niche}.",
        "slug_suffix": "opportunity",
    },
    {
        "title": "Audience & Use Cases",
        "summary_template": "Define target segments, pain points, and high-value scenarios enabled by {niche}.",
        "slug_suffix": "audience-use-cases",
    },
    {
        "title": "Solution Architecture",
        "summary_template": "Lay out the systems, workflows, and tooling required to deliver {niche} successfully.",
        "slug_suffix": "solution-architecture",
    },
    {
        "title": "Implementation Roadmap",
        "summary_template": "Break the work into phased sprints, ownership roles, and operational checklists for {niche}.",
        "slug_suffix": "implementation-roadmap",
    },
    {
        "title": "Tool Stack & Enablement",
        "summary_template": "Curate platforms, integrations, templates, and enablement assets that accelerate {niche}.",
        "slug_suffix": "tool-stack",
    },
    {
        "title": "Metrics & Iteration Plan",
        "summary_template": "Track KPIs, feedback loops, and iteration opportunities to keep {niche} improving.",
        "slug_suffix": "metrics-iteration",
    },
]


def build_skeleton(niche_name: str) -> List[Dict[str, str]]:
    base_slug = slugify(niche_name)[:60]
    skeleton = []
    for stage in BASE_STAGES:
        slug = f"{base_slug}-{stage['slug_suffix']}" if base_slug else stage['slug_suffix']
        if len(slug) > 90:
            slug = slug[:90]
        skeleton.append(
            {
                "title": stage["title"],
                "summary": stage["summary_template"].format(niche=niche_name),
                "slug": slug,
            }
        )
    return skeleton


def make_niche(domain_name: str, niche_title: str, description: str) -> Dict[str, object]:
    slug = slugify(niche_title)[:90]
    return {
        "slug": slug,
        "name": niche_title,
        "description": description,
        "prompt_template": build_prompt(domain_name, niche_title, description),
        "content_skeleton": build_skeleton(niche_title),
        "is_active": True,
    }


def make_domain(slug: str, name: str, description: str, icon: str, niches: List[Dict[str, str]]) -> Dict[str, object]:
    return {
        "slug": slug,
        "name": name,
        "description": description,
        "icon": icon,
        "niches": [make_niche(name, n["title"], n["description"]) for n in niches],
    }


GUIDED_CATALOG: List[Dict[str, object]] = [
    make_domain(
        slug="artificial_intelligence_machine_learning",
        name="Artificial Intelligence & Machine Learning",
        description="Launch AI and machine learning initiatives with curated playbooks for builders and operators.",
        icon="fa-brain",
        niches=[
            {"title": "Generative AI Tools and Applications", "description": "Design and deploy generative AI solutions spanning content, product innovation, and productivity workflows."},
            {"title": "AI Prompt Engineering and Optimization", "description": "Build reusable prompt systems, guardrails, and evaluation loops for large language models."},
            {"title": "AI Safety and Alignment Research", "description": "Implement responsible AI policies, alignment frameworks, and risk mitigation experiments for production teams."},
            {"title": "Custom GPT Development", "description": "Create bespoke GPT agents with persona design, retrieval augmentation, and lifecycle management."},
            {"title": "AI-Powered Automation Solutions", "description": "Automate cross-functional processes by orchestrating AI agents, integrations, and human-in-the-loop checkpoints."},
            {"title": "Machine Learning Operations (MLOps)", "description": "Operationalize models with CI/CD, monitoring, data quality pipelines, and governance practices."},
            {"title": "Computer Vision Applications", "description": "Launch computer vision products with data labeling, model selection, deployment, and performance tuning."},
            {"title": "Natural Language Processing Tools", "description": "Deliver NLP capabilities such as search, summarization, and conversational assistants with robust evaluation."},
        ],
    ),
    make_domain(
        slug="health_wellness_technology",
        name="Health & Wellness Technology",
        description="Build tech-enabled health experiences that combine evidence-based care with scalable digital delivery.",
        icon="fa-heartbeat",
        niches=[
            {"title": "Mental Health Apps and Teletherapy Platforms", "description": "Build digital mental health offerings with evidence-based programs, clinical workflows, and compliance."},
            {"title": "Wearable Health Device Integration", "description": "Connect wearable data into patient journeys, coaching programs, and personalized interventions."},
            {"title": "Personalized Nutrition and Meal Planning", "description": "Deliver tailored nutrition roadmaps using data-driven assessments and adaptive meal planning."},
            {"title": "Sleep Optimization Technology", "description": "Design sleep optimization systems integrating tracking hardware, behavioral science, and coaching loops."},
            {"title": "Fitness Tracking and Virtual Coaching", "description": "Launch virtual fitness programs that combine sensors, content, and adaptive coaching experiences."},
            {"title": "Preventive Healthcare Solutions", "description": "Create preventive care platforms focusing on risk scoring, education, and remote monitoring."},
            {"title": "Biohacking and Longevity Tech", "description": "Guide users through responsible biohacking, longevity metrics, and protocols grounded in science."},
        ],
    ),
    make_domain(
        slug="sustainable_tech_green_energy",
        name="Sustainable Technology & Green Energy",
        description="Accelerate sustainable innovation with platforms that measure impact and drive climate-positive change.",
        icon="fa-leaf",
        niches=[
            {"title": "Carbon Footprint Tracking Software", "description": "Build carbon accounting products with data pipelines, dashboards, and reduction playbooks."},
            {"title": "Renewable Energy Management Systems", "description": "Orchestrate solar, wind, and storage assets with forecasting, dispatch, and ROI analytics."},
            {"title": "Electric Vehicle Charging Infrastructure", "description": "Plan and operate EV charging networks with siting, hardware selection, and uptime monitoring."},
            {"title": "Circular Economy Platforms", "description": "Enable circular supply chains through reverse logistics, refurbishment, and materials intelligence."},
            {"title": "Sustainable Fashion Tech", "description": "Transform fashion operations with sustainable materials, supply chain transparency, and impact tracking."},
            {"title": "Green Building Technology", "description": "Deploy smart building systems that drive efficiency, healthy environments, and sustainability certifications."},
            {"title": "Climate Risk Assessment Tools", "description": "Deliver climate risk models, scenario planning, and adaptation guidance for decision-makers."},
        ],
    ),
    make_domain(
        slug="remote_work_digital_collaboration",
        name="Remote Work & Digital Collaboration",
        description="Design high-performance distributed teams with modern collaboration systems and workflows.",
        icon="fa-laptop-house",
        niches=[
            {"title": "Virtual Office Environments", "description": "Design immersive digital workplaces that recreate presence, collaboration, and team rituals."},
            {"title": "Async Communication Tools", "description": "Implement asynchronous communication systems with clear workflows, etiquette, and visibility."},
            {"title": "Remote Team Productivity Software", "description": "Equip distributed teams with productivity dashboards, goal tracking, and accountability loops."},
            {"title": "Digital Nomad Services and Platforms", "description": "Build services for digital nomads covering compliance, community, and local resource access."},
            {"title": "Hybrid Work Management Solutions", "description": "Coordinate hybrid teams with scheduling, workplace experience, and change management tooling."},
            {"title": "Virtual Event Platforms", "description": "Deliver virtual event experiences with production blueprints, audience engagement, and monetization."},
        ],
    ),
    make_domain(
        slug="cybersecurity",
        name="Cybersecurity",
        description="Protect modern organizations with security architectures, automation, and human-centric programs.",
        icon="fa-shield-alt",
        niches=[
            {"title": "Zero-Trust Security Architecture", "description": "Roll out zero-trust programs covering identity, device posture, micro-segmentation, and governance."},
            {"title": "Identity and Access Management", "description": "Implement IAM strategies spanning provisioning, authentication, and privileged access controls."},
            {"title": "Cloud Security Solutions", "description": "Secure cloud environments with configuration baselines, threat detection, and incident workflows."},
            {"title": "Ransomware Protection", "description": "Build ransomware resilience plans with prevention, backup strategies, and recovery playbooks."},
            {"title": "Privacy-Focused Tools", "description": "Deliver privacy-by-design tooling for consent management, data minimization, and regulatory alignment."},
            {"title": "Security Awareness Training Platforms", "description": "Launch human risk management programs combining education, simulations, and reporting."},
        ],
    ),
    make_domain(
        slug="creator_economy_digital_content",
        name="Creator Economy & Digital Content",
        description="Scale creator-led businesses with tools for monetization, production, and audience growth.",
        icon="fa-video",
        niches=[
            {"title": "Content Monetization Platforms", "description": "Design monetization systems including subscriptions, memberships, and community commerce."},
            {"title": "Creator Management Tools", "description": "Build back-office platforms for talent coordination, analytics, and contract workflows."},
            {"title": "Short-Form Video Editing Software", "description": "Ship editing solutions that accelerate short-form storytelling and cross-platform publishing."},
            {"title": "Live Streaming Technology", "description": "Deliver live streaming stacks covering production, engagement tools, and monetization hooks."},
            {"title": "Digital Asset Management", "description": "Organize content libraries with metadata, collaboration workflows, and rights management."},
            {"title": "Influencer Marketing Platforms", "description": "Create influencer marketing suites for discovery, campaign execution, and performance tracking."},
            {"title": "Podcast Production and Distribution", "description": "Develop podcast production playbooks across recording, editing, distribution, and growth."},
        ],
    ),
    make_domain(
        slug="web3_blockchain",
        name="Web3 & Blockchain",
        description="Navigate the evolving Web3 landscape with practical frameworks and compliant launches.",
        icon="fa-cubes",
        niches=[
            {"title": "Decentralized Finance (DeFi) Applications", "description": "Launch DeFi products with token design, smart contract audits, and liquidity strategies."},
            {"title": "NFT Utility Platforms (Beyond Art)", "description": "Create NFT utility platforms for memberships, credentials, and real-world activations."},
            {"title": "Blockchain Supply Chain Solutions", "description": "Deploy blockchain traceability solutions improving transparency and trust."},
            {"title": "Digital Identity Verification", "description": "Implement digital identity stacks combining wallets, verifiable credentials, and compliance."},
            {"title": "Cryptocurrency Payment Processors", "description": "Build crypto payment infrastructure with risk controls, settlement, and customer experience."},
        ],
    ),
    make_domain(
        slug="edtech_online_learning",
        name="EdTech & Online Learning",
        description="Deliver transformational learning products backed by pedagogy, analytics, and community.",
        icon="fa-graduation-cap",
        niches=[
            {"title": "Micro-Learning Platforms", "description": "Build micro-learning experiences with bite-sized content, spaced repetition, and analytics."},
            {"title": "Skills-Based Learning and Certification", "description": "Deliver competency-based learning paths with assessments and credentialing."},
            {"title": "Corporate Training Solutions", "description": "Create corporate learning ecosystems tying competency models to measurable outcomes."},
            {"title": "Language Learning Apps", "description": "Design language learning products blending immersion, AI feedback, and community."},
            {"title": "STEM Education Tools", "description": "Ship STEM learning kits with hands-on projects, curriculum alignment, and teacher support."},
            {"title": "Adaptive Learning Technology", "description": "Implement adaptive engines that personalize pacing, difficulty, and support."},
        ],
    ),
    make_domain(
        slug="ecommerce_retail_tech",
        name="E-commerce & Retail Tech",
        description="Invent the next wave of commerce experiences across channels, communities, and products.",
        icon="fa-shopping-bag",
        niches=[
            {"title": "Social Commerce Integration", "description": "Integrate social channels, influencer workflows, and conversion funnels for commerce."},
            {"title": "AI-Powered Personalization", "description": "Deliver personalization systems combining data pipelines, experimentation, and automation."},
            {"title": "Augmented Reality Shopping Experiences", "description": "Launch AR shopping experiences across visualization, fitting, and storytelling."},
            {"title": "Subscription Box Services", "description": "Build subscription operations covering product curation, logistics, and retention."},
            {"title": "Direct-to-Consumer (D2C) Brands", "description": "Scale D2C brands with lifecycle marketing, supply chain orchestration, and growth loops."},
            {"title": "Resale and Secondhand Marketplaces", "description": "Create resale marketplaces focusing on authentication, pricing, and community trust."},
        ],
    ),
    make_domain(
        slug="fintech",
        name="FinTech",
        description="Build financial innovation with regulatory readiness, trust, and profitable distribution.",
        icon="fa-chart-line",
        niches=[
            {"title": "Embedded Finance Solutions", "description": "Ship embedded finance products with API integrations, compliance, and go-to-market."},
            {"title": "Buy-Now-Pay-Later (BNPL) Services", "description": "Launch BNPL offerings covering risk underwriting, merchant integration, and customer care."},
            {"title": "Robo-Advisors and Automated Investing", "description": "Build automated investing platforms with portfolio design, compliance, and UX."},
            {"title": "Cryptocurrency Tax Tools", "description": "Deliver crypto tax software with data aggregation, reconciliation, and reporting."},
            {"title": "Digital Banking for Niche Markets", "description": "Design challenger bank experiences tailored to niche communities."},
            {"title": "Payment Orchestration Platforms", "description": "Implement payment orchestration layers optimizing authorization, routing, and resilience."},
        ],
    ),
    make_domain(
        slug="data_analytics_business_intelligence",
        name="Data Analytics & Business Intelligence",
        description="Turn data into action with modern analytics stacks, governance, and storytelling.",
        icon="fa-chart-pie",
        niches=[
            {"title": "Real-Time Analytics Dashboards", "description": "Create real-time analytics stacks with streaming data, alerting, and visualization."},
            {"title": "Predictive Analytics Tools", "description": "Deploy predictive analytics workflows including feature stores, modeling, and monitoring."},
            {"title": "Customer Data Platforms", "description": "Implement CDPs unifying identities, segmentation, and activation."},
            {"title": "Data Visualization Software", "description": "Design data visualization suites balancing usability, storytelling, and governance."},
            {"title": "Market Intelligence Solutions", "description": "Build market intelligence programs combining research pipelines, insights, and reporting."},
        ],
    ),
    make_domain(
        slug="gaming_interactive_entertainment",
        name="Gaming & Interactive Entertainment",
        description="Create immersive gaming experiences with scalable tech and engaged communities.",
        icon="fa-gamepad",
        niches=[
            {"title": "Cloud Gaming Platforms", "description": "Launch cloud gaming services with infrastructure, content licensing, and user experience design."},
            {"title": "Mobile Gaming Monetization", "description": "Optimize mobile games with monetization blueprints, live ops, and retention loops."},
            {"title": "Game Development Tools", "description": "Create game developer tools that accelerate prototyping, collaboration, and asset pipelines."},
            {"title": "Esports Infrastructure", "description": "Build esports infrastructure covering tournament operations, broadcasting, and community growth."},
            {"title": "Virtual Reality Gaming Experiences", "description": "Design VR gaming experiences with hardware considerations, comfort, and interaction design."},
        ],
    ),
    make_domain(
        slug="automation",
        name="Automation",
        description="Automate processes end-to-end with orchestrated platforms, AI assistance, and measurable outcomes.",
        icon="fa-cogs",
        niches=[
            {"title": "Business Process Automation (BPA)", "description": "Automate cross-department processes with workflow mapping, orchestration, and governance."},
            {"title": "Robotic Process Automation (RPA)", "description": "Deploy RPA programs handling data entry, system integration, and quality control."},
            {"title": "Marketing Automation", "description": "Build marketing automation journeys across channels, segmentation, and analytics."},
            {"title": "Sales Automation", "description": "Enable sales automation for pipeline management, outreach sequencing, and deal tracking."},
            {"title": "Customer Service Automation", "description": "Deliver service automation via chatbots, ticket routing, and self-service design."},
            {"title": "IT & DevOps Automation", "description": "Operationalize DevOps automation spanning CI/CD, infrastructure as code, and reliability."},
            {"title": "No-Code/Low-Code Automation", "description": "Empower teams with no-code automation platforms, governance, and enablement."},
            {"title": "AI-Powered Automation", "description": "Integrate AI-driven automation for intelligent document processing and decision workflows."},
            {"title": "E-commerce Automation", "description": "Automate ecommerce operations from inventory to pricing and fulfillment."},
            {"title": "HR & Recruitment Automation", "description": "Streamline HR automation for hiring, onboarding, and workforce management."},
            {"title": "Personal Productivity Automation", "description": "Design personal automation routines covering tasks, calendaring, and finance."},
            {"title": "Testing & Quality Assurance Automation", "description": "Implement QA automation pipelines for regression, performance, and data quality."},
        ],
    ),
]


DOMAIN_SLUGS = [domain["slug"] for domain in GUIDED_CATALOG]


def get_domain_by_slug(slug: str) -> Dict[str, object]:
    for domain in GUIDED_CATALOG:
        if domain["slug"] == slug:
            return domain
    raise KeyError(f"Domain slug '{slug}' not found in GUIDED_CATALOG")
