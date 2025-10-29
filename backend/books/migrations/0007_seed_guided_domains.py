from django.db import migrations


GUIDED_DOMAINS = [
    {
        "slug": "ai_automation",
        "name": "AI & Automation",
        "description": "Playbooks for automating operations, marketing, and content with AI agents.",
        "icon": "fa-robot",
        "niches": [
            {
                "slug": "workflow_automation_playbook",
                "name": "Workflow Automation Playbook",
                "description": "Automate repetitive operations with no-code and AI orchestrations.",
                "prompt_template": (
                    "You are an automation consultant helping a scaling operations team replace manual work with AI-powered workflows."
                    " Focus on actionable steps, metrics, and change management guidance."
                ),
                "content_skeleton": [
                    {"title": "Automation Opportunity Scan", "summary": "Identify bottlenecks and high-impact candidates.", "slug": "opportunity-scan"},
                    {"title": "Process Mapping Quickstart", "summary": "Document current vs future workflow states.", "slug": "process-mapping"},
                    {"title": "Selecting the Right Tools", "summary": "Compare AI automation platforms and integration patterns.", "slug": "selecting-tools"},
                    {"title": "Implementation Sprint Guide", "summary": "Plan and execute a 14-day automation sprint.", "slug": "implementation-sprint"},
                    {"title": "Adoption & Change Management", "summary": "Activate training, QA, and guardrails for the team.", "slug": "adoption"},
                    {"title": "KPI Dashboard & Next Iterations", "summary": "Measure ROI and roadmap follow-up automations.", "slug": "kpi-dashboard"},
                ],
            },
            {
                "slug": "ai_marketing_studio",
                "name": "AI Marketing Studio",
                "description": "Launch AI-assisted campaigns, creative assets, and conversion experiments.",
                "prompt_template": (
                    "You are an AI marketing lead building a high-converting campaign system."
                    " Provide frameworks, tool stacks, and creative testing checklists."
                ),
                "content_skeleton": [
                    {"title": "Campaign Strategy Blueprint", "summary": "Clarify ICP, offer, and success metrics.", "slug": "strategy-blueprint"},
                    {"title": "Persona & Messaging Engine", "summary": "Generate messaging matrices and positioning.", "slug": "messaging-engine"},
                    {"title": "AI Creative Production", "summary": "Produce copy, visuals, and video variations with AI.", "slug": "creative-production"},
                    {"title": "Launch Playbook", "summary": "Activate campaigns across paid, email, and social.", "slug": "launch-playbook"},
                    {"title": "Optimization Lab", "summary": "Run experiments, review analytics, and iterate weekly.", "slug": "optimization-lab"},
                    {"title": "Scaling & Governance", "summary": "Create documentation, guardrails, and team workflows.", "slug": "scaling-governance"},
                ],
            },
            {
                "slug": "ai_content_ops",
                "name": "AI Content Ops",
                "description": "Build an AI-assisted content engine for blogs, video, and social.",
                "prompt_template": (
                    "You are a director of content operations rolling out AI co-pilots to a content team."
                    " Emphasize editorial standards, review gates, and repurposing workflows."
                ),
                "content_skeleton": [
                    {"title": "Content Operating Model", "summary": "Define roles, responsibilities, and production cadence.", "slug": "operating-model"},
                    {"title": "Research & Insight System", "summary": "Gather voice-of-customer inputs and trend signals.", "slug": "research-system"},
                    {"title": "Prompt & Template Library", "summary": "Design reusable AI instructions and briefs.", "slug": "prompt-library"},
                    {"title": "Multiformat Production", "summary": "Produce long-form, short-form, and multimedia assets.", "slug": "multiformat-production"},
                    {"title": "Quality & Compliance", "summary": "Review checklists, fact-checking, and brand safety.", "slug": "quality-compliance"},
                    {"title": "Distribution & Repurposing", "summary": "Package assets for channels and create evergreen loops.", "slug": "distribution"},
                ],
            },
        ],
    },
    {
        "slug": "parenting_preschool_learning",
        "name": "Parenting: Pre-school Speech & Learning",
        "description": "Support families with playful speech therapy and early learning routines.",
        "icon": "fa-child",
        "niches": [
            {
                "slug": "speech_confidence_boost",
                "name": "Speech Confidence Boost",
                "description": "Daily speech exercises and games for ages 3-6.",
                "prompt_template": (
                    "You are a certified speech-language pathologist coaching parents to build confident communicators."
                    " Keep activities playful, time-boxed, and materials-light."
                ),
                "content_skeleton": [
                    {"title": "Family Intake & Milestones", "summary": "Benchmark current speech sounds and social confidence.", "slug": "family-intake"},
                    {"title": "Daily Sound Play", "summary": "Introduce articulation games for high-priority sounds.", "slug": "sound-play"},
                    {"title": "Conversation Sparks", "summary": "Use storytelling cards and routines to expand vocabulary.", "slug": "conversation-sparks"},
                    {"title": "Movement & Sensory Pairings", "summary": "Blend gross-motor play with speech prompts.", "slug": "movement-sensory"},
                    {"title": "Progress Celebrations", "summary": "Track wins, reinforce confidence, and involve siblings.", "slug": "progress-celebrations"},
                    {"title": "Parent Coaching Toolkit", "summary": "Offer troubleshooting tips and expert escalation paths.", "slug": "parent-coaching"},
                ],
            },
            {
                "slug": "phonics_foundations_lab",
                "name": "Phonics Foundations Lab",
                "description": "Phonics-rich routines to launch early reading skills.",
                "prompt_template": (
                    "You are an early literacy specialist designing a six-week phonics lab for preschoolers."
                    " Blend multi-sensory activities, decodable stories, and progress trackers."
                ),
                "content_skeleton": [
                    {"title": "Readiness Check & Goals", "summary": "Assess letter knowledge and set family goals.", "slug": "readiness"},
                    {"title": "Sound-to-Symbol Stations", "summary": "Hands-on games that map sounds to letters.", "slug": "sound-symbol"},
                    {"title": "Blending & Segmenting Mini-Labs", "summary": "Daily exercises to blend sounds into words.", "slug": "blending-labs"},
                    {"title": "Decodable Story Time", "summary": "Introduce short stories with comprehension prompts.", "slug": "story-time"},
                    {"title": "Writing & Fine Motor Boost", "summary": "Letter formation activities and tactile tracing.", "slug": "writing-motor"},
                    {"title": "Family Literacy Rituals", "summary": "Design consistent home reading rituals and trackers.", "slug": "literacy-rituals"},
                ],
            },
            {
                "slug": "sensory_learning_adventures",
                "name": "Sensory Learning Adventures",
                "description": "Weekly sensory bins, outdoor missions, and calm-down kits.",
                "prompt_template": (
                    "You are an occupational therapist curating sensory-rich adventures that reinforce speech, motor, and social skills."
                    " Provide setup lists, calming strategies, and reflection prompts."
                ),
                "content_skeleton": [
                    {"title": "Sensory Profile Snapshot", "summary": "Identify sensory seekers, avoiders, and regulators.", "slug": "sensory-profile"},
                    {"title": "Indoor Sensory Stations", "summary": "Create tactile bins, fine-motor labs, and calm corners.", "slug": "indoor-stations"},
                    {"title": "Outdoor Adventure Missions", "summary": "Design scavenger hunts and movement circuits.", "slug": "outdoor-missions"},
                    {"title": "Calm-Down Toolkit", "summary": "Build reset kits with breathing prompts and visuals.", "slug": "calm-down-toolkit"},
                    {"title": "Parent Coaching Scripts", "summary": "Model language, praise, and conflict resolution.", "slug": "coaching-scripts"},
                    {"title": "Progress Reflection Journal", "summary": "Celebrate growth and adapt activities weekly.", "slug": "reflection-journal"},
                ],
            },
        ],
    },
    {
        "slug": "ecommerce_digital_products",
        "name": "E-commerce & Digital Products",
        "description": "Launch and scale digital product businesses with AI-accelerated systems.",
        "icon": "fa-shopping-cart",
        "niches": [
            {
                "slug": "digital_product_blueprint",
                "name": "Digital Product Blueprint",
                "description": "Validate, package, and launch a high-ticket digital product in 30 days.",
                "prompt_template": (
                    "You are a digital product strategist guiding a founder from idea to launch."
                    " Emphasize validation interviews, offer design, and funnel automation."
                ),
                "content_skeleton": [
                    {"title": "Customer Discovery Sprint", "summary": "Research pain points, desired outcomes, and willingness to pay.", "slug": "discovery-sprint"},
                    {"title": "Offer Architecture", "summary": "Shape transformation pillars, modules, and bonuses.", "slug": "offer-architecture"},
                    {"title": "Minimum Viable Curriculum", "summary": "Outline lesson templates, assets, and delivery tools.", "slug": "mvc"},
                    {"title": "Audience Building Engine", "summary": "Grow waitlists through collaborations, lead magnets, and communities.", "slug": "audience-engine"},
                    {"title": "Launch Funnel & Automation", "summary": "Draft sales pages, email sequences, and checkout flows.", "slug": "launch-funnel"},
                    {"title": "Metrics & Iteration", "summary": "Track conversion metrics and design post-launch improvements.", "slug": "metrics-iteration"},
                ],
            },
            {
                "slug": "shopify_growth_system",
                "name": "Shopify Growth System",
                "description": "Optimize a Shopify storefront with AI-driven merchandising and retention.",
                "prompt_template": (
                    "You are an ecommerce operator revamping a Shopify store for profitable growth."
                    " Provide dashboards, automation recipes, and retention checkpoints."
                ),
                "content_skeleton": [
                    {"title": "Store Diagnostics", "summary": "Audit analytics, technical setup, and conversion leaks.", "slug": "store-diagnostics"},
                    {"title": "Merchandising Overhaul", "summary": "Use AI to improve photography, descriptions, and bundles.", "slug": "merchandising"},
                    {"title": "Acquisition Channels", "summary": "Deploy paid, organic, and partnership playbooks.", "slug": "acquisition-channels"},
                    {"title": "Lifecycle Marketing", "summary": "Build automated email/SMS flows and loyalty programs.", "slug": "lifecycle-marketing"},
                    {"title": "Operations & Fulfillment", "summary": "Streamline inventory, shipping, and support workflows.", "slug": "operations-fulfillment"},
                    {"title": "Growth Dashboard", "summary": "Define weekly KPI reviews and experiment backlog.", "slug": "growth-dashboard"},
                ],
            },
            {
                "slug": "print_on_demand_starter",
                "name": "Print-on-Demand Starter",
                "description": "Create and launch a print-on-demand micro-brand with AI-assisted design.",
                "prompt_template": (
                    "You are a print-on-demand mentor helping a creator validate, design, and launch a niche brand."
                    " Focus on trend research, creative testing, and fulfillment workflows."
                ),
                "content_skeleton": [
                    {"title": "Niche & Trend Lab", "summary": "Research micro communities and winning product angles.", "slug": "trend-lab"},
                    {"title": "Brand Identity Sprint", "summary": "Craft brand voice, design system, and product catalog.", "slug": "brand-sprint"},
                    {"title": "AI Design Studio", "summary": "Use AI tools to generate print-ready artwork variations.", "slug": "design-studio"},
                    {"title": "Storefront Setup", "summary": "Configure POD platform, listings, and pricing.", "slug": "storefront-setup"},
                    {"title": "Launch & Promo Plan", "summary": "Plan content launch calendar, influencer packs, and ads.", "slug": "launch-plan"},
                    {"title": "Fulfillment & Customer Care", "summary": "Automate order routing, QA, and post-purchase support.", "slug": "fulfillment"},
                ],
            },
        ],
    },
]


def seed_guided_domains(apps, schema_editor):
    Domain = apps.get_model('books', 'Domain')
    Niche = apps.get_model('books', 'Niche')
    Book = apps.get_model('books', 'Book')
    BookTemplate = apps.get_model('books', 'BookTemplate')

    target_slugs = [domain["slug"] for domain in GUIDED_DOMAINS]

    # Remove legacy domains/niches that are no longer part of the guided experience
    legacy_domains = Domain.objects.exclude(slug__in=target_slugs)
    if legacy_domains.exists():
        Book.objects.filter(domain__in=legacy_domains).delete()
        BookTemplate.objects.filter(domain__in=legacy_domains).delete()
        Domain.objects.filter(pk__in=legacy_domains.values_list("pk", flat=True)).delete()

    for order, domain_data in enumerate(GUIDED_DOMAINS, start=1):
        domain_defaults = {
            "name": domain_data["name"],
            "description": domain_data["description"],
            "icon": domain_data["icon"],
            "order": order,
            "is_active": True,
        }
        domain, _ = Domain.objects.update_or_create(
            slug=domain_data["slug"], defaults=domain_defaults
        )

        niche_slugs = [niche["slug"] for niche in domain_data["niches"]]
        removable_niches = domain.niches.exclude(slug__in=niche_slugs)
        if removable_niches.exists():
            Book.objects.filter(niche__in=removable_niches).delete()
            BookTemplate.objects.filter(niche__in=removable_niches).delete()
            domain.niches.filter(pk__in=removable_niches.values_list("pk", flat=True)).delete()

        for idx, niche_data in enumerate(domain_data["niches"], start=1):
            defaults = {
                "name": niche_data["name"],
                "description": niche_data["description"],
                "prompt_template": niche_data["prompt_template"],
                "content_skeleton": niche_data["content_skeleton"],
                "is_active": True,
                "order": idx,
            }
            Niche.objects.update_or_create(
                domain=domain,
                slug=niche_data["slug"],
                defaults=defaults,
            )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0006_guided_workflow_refactor"),
    ]

    operations = [
        migrations.RunPython(seed_guided_domains, noop),
    ]
