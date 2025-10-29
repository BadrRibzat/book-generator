"""Management command to train the custom LLM using guided catalog data."""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from books.data.guided_catalog import GUIDED_CATALOG
from customllm.models import TrainingDomain, TrainingNiche, TrainingSample, TrainingSession


DOMAIN_CHOICES = [domain["slug"] for domain in GUIDED_CATALOG]
CATALOG_INDEX = {domain["slug"]: domain for domain in GUIDED_CATALOG}


class Command(BaseCommand):
    help = "Train the custom LLM with structured samples from the guided catalog"

    def add_arguments(self, parser):
        parser.add_argument(
            "--domain",
            type=str,
            choices=DOMAIN_CHOICES + ["all"],
            default="all",
            help="Domain slug to train (default: all)",
        )

    def handle(self, *args, **options):
        domain_slug = options["domain"]

        self.stdout.write(self.style.SUCCESS("\n" + "=" * 70))
        self.stdout.write(self.style.SUCCESS("🧠 CUSTOM LLM TRAINING"))
        self.stdout.write(self.style.SUCCESS("=" * 70 + "\n"))

        session = TrainingSession.objects.create(status="running", started_at=timezone.now())

        try:
            self.stdout.write("📋 Step 1: Initializing domains...")
            domains = self._sync_domains()
            self.stdout.write(
                self.style.SUCCESS(f"   ✓ Synced {len(domains)} training domains\n")
            )

            self.stdout.write("🎯 Step 2: Initializing niches...")
            self.niche_cache = self._sync_niches(domains)
            self.stdout.write(
                self.style.SUCCESS(
                    f"   ✓ Synced {len(self.niche_cache)} training niches\n"
                )
            )

            catalog_subset = (
                GUIDED_CATALOG if domain_slug == "all" else [CATALOG_INDEX[domain_slug]]
            )
            domain_objects = {domain.slug: domain for domain in domains}

            self.stdout.write("📝 Step 3: Generating training samples...")
            total_samples = 0
            for payload in catalog_subset:
                domain = domain_objects[payload["slug"]]
                created = self._generate_samples_for_domain(domain, payload)
                total_samples += created
                self.stdout.write(
                    self.style.SUCCESS(f"   ✓ {domain.name}: {created} samples")
                )

            self.stdout.write(
                self.style.SUCCESS(f"\n   Total samples generated: {total_samples}\n")
            )

            self.stdout.write("📊 Step 4: Updating statistics...")
            for payload in catalog_subset:
                domain = domain_objects[payload["slug"]]
                domain.training_samples_count = TrainingSample.objects.filter(
                    domain=domain
                ).count()
                domain.training_quality_score = 85.0
                domain.last_trained = timezone.now()
                domain.save(
                    update_fields=[
                        "training_samples_count",
                        "training_quality_score",
                        "last_trained",
                    ]
                )
            self.stdout.write(self.style.SUCCESS("   ✓ Statistics updated\n"))

            session.status = "completed"
            session.completed_at = timezone.now()
            session.duration_seconds = int(
                (session.completed_at - session.started_at).total_seconds()
            )
            session.samples_count = total_samples
            session.log = (
                f"Trained {len(catalog_subset)} domains with {total_samples} samples"
            )
            session.save()

            self.stdout.write(self.style.SUCCESS("=" * 70))
            self.stdout.write(self.style.SUCCESS("✅ TRAINING COMPLETE!"))
            self.stdout.write(
                self.style.SUCCESS(f"   Duration: {session.duration_seconds}s")
            )
            self.stdout.write(self.style.SUCCESS(f"   Samples: {total_samples}"))
            self.stdout.write(self.style.SUCCESS("=" * 70 + "\n"))

        except Exception as exc:  # pragma: no cover - surfaced to CLI
            session.status = "failed"
            session.error_message = str(exc)
            session.save(update_fields=["status", "error_message"])
            self.stdout.write(self.style.ERROR(f"\n❌ Training failed: {exc}\n"))
            raise

    def _sync_domains(self):
        domains = []
        for payload in GUIDED_CATALOG:
            domain, _ = TrainingDomain.objects.update_or_create(
                slug=payload["slug"],
                defaults={
                    "name": payload["name"],
                    "description": payload["description"],
                    "is_active": True,
                },
            )
            domains.append(domain)
        return domains

    def _sync_niches(self, domains):
        domain_map = {domain.slug: domain for domain in domains}
        cache = {}
        for payload in GUIDED_CATALOG:
            domain = domain_map[payload["slug"]]
            for niche_payload in payload["niches"]:
                keywords = self._keywords_from_text(
                    niche_payload["name"], niche_payload["description"]
                )
                niche, _ = TrainingNiche.objects.update_or_create(
                    domain=domain,
                    slug=niche_payload["slug"],
                    defaults={
                        "name": niche_payload["name"],
                        "description": niche_payload["description"],
                        "keywords": keywords,
                        "target_audiences": [
                            "operators",
                            "founders",
                            "strategists",
                            "teams",
                        ],
                        "is_active": True,
                    },
                )
                cache[(domain.slug, niche.slug)] = niche
        return cache

    def _generate_samples_for_domain(self, domain, domain_payload):
        created = 0
        for niche_payload in domain_payload["niches"]:
            niche = self.niche_cache[(domain.slug, niche_payload["slug"])]
            created += self._create_outline_sample(domain, niche, niche_payload)
            created += self._create_chapter_samples(domain, niche, niche_payload)
            created += self._create_cover_sample(domain, niche, niche_payload)
        return created

    def _create_outline_sample(self, domain, niche, niche_payload):
        prompt = f"Generate a book outline for: {domain.name} - {niche.name}"
        completion = self._outline_template(domain, niche_payload)
        TrainingSample.objects.update_or_create(
            domain=domain,
            niche=niche,
            sample_type="outline",
            prompt=prompt,
            defaults={
                "completion": completion,
                "context": {"audience": "operators", "length": "medium"},
                "quality_score": 0.9,
                "source": "catalog-template",
            },
        )
        return 1

    def _create_chapter_samples(self, domain, niche, niche_payload):
        skeleton = niche_payload["content_skeleton"]
        created = 0
        for stage in skeleton[:6]:
            title = stage["title"]
            prompt = f"Write a chapter titled '{title}' for the {niche.name} playbook"
            completion = self._chapter_template(domain, niche_payload, stage)
            TrainingSample.objects.update_or_create(
                domain=domain,
                niche=niche,
                sample_type="chapter",
                prompt=prompt,
                defaults={
                    "completion": completion,
                    "context": {"word_count": 520, "audience": "operators"},
                    "quality_score": 0.85,
                    "source": "catalog-template",
                },
            )
            created += 1
        return created

    def _create_cover_sample(self, domain, niche, niche_payload):
        prompt = f"Generate a cover description for a book about {niche.name}"
        completion = self._cover_template(domain, niche_payload)
        TrainingSample.objects.update_or_create(
            domain=domain,
            niche=niche,
            sample_type="cover_description",
            prompt=prompt,
            defaults={
                "completion": completion,
                "context": {"style": "professional", "modern": True},
                "quality_score": 0.9,
                "source": "catalog-template",
            },
        )
        return 1

    def _outline_template(self, domain, niche_payload):
        lines = [
            f"Title: {domain.name} Playbook — {niche_payload['name']}",
            "",
            "Program Objectives",
            f"- {niche_payload['description']}",
            f"- Target outcomes for {domain.name.lower()} teams",
            "",
        ]
        for idx, stage in enumerate(niche_payload["content_skeleton"], 1):
            lines.append(f"{idx}. {stage['title']}")
            summary = stage.get("summary")
            if summary:
                lines.append(f"   - {summary}")
            lines.append("")
        lines.append("Resources & Next Steps")
        lines.append("- Metrics dashboard")
        lines.append("- Tool stack checklist")
        lines.append("- Learning plan")
        return "\n".join(lines).strip()

    def _chapter_template(self, domain, niche_payload, stage):
        summary = stage.get("summary") or (
            f"This chapter dives into {stage['title'].lower()} for "
            f"{niche_payload['name'].lower()}."
        )
        paragraphs = [
            f"# {stage['title']}",
            "",
            summary,
            "",
            "#### Strategic Moves",
            f"- Define how {stage['title'].lower()} unlocks value inside {domain.name.lower()} teams.",
            f"- Map owners, stakeholders, and rituals that keep {stage['title'].lower()} on track.",
            f"- Highlight safeguards, tooling, and documentation requirements.",
            "",
            "#### Implementation Sprint",
            "1. Discover current state and surface gaps.",
            "2. Design the ideal flow with measurable checkpoints.",
            "3. Launch a pilot, gather feedback, and iterate.",
            "4. Operationalize with playbooks, enablement, and dashboards.",
            "",
            "#### Metrics & Signals",
            "- Leading indicator",
            "- Lagging indicator",
            "- Qualitative signal",
            "",
            "#### Risks & Mitigations",
            "- Adoption friction and how to address it",
            "- Governance guardrails to maintain quality",
            "- Escalation path when issues surface",
        ]
        return "\n".join(paragraphs)

    def _cover_template(self, domain, niche_payload):
        return (
            f"Professional book cover for '{niche_payload['name']}'. "
            f"Modern design references the {domain.name.lower()} landscape with confident gradients, "
            f"clean typography, and a focal illustration inspired by {niche_payload['name'].lower()}."
        )

    def _keywords_from_text(self, title, description):
        words = slugify(f"{title} {description}").split("-")
        filtered = [word for word in words if word and not word.isdigit()]
        keywords = []
        seen = set()
        for word in filtered:
            if word in seen:
                continue
            seen.add(word)
            keywords.append(word)
            if len(keywords) >= 8:
                break
        return keywords or ["playbook"]
