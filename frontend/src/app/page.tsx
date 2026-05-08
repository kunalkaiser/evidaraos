import Link from "next/link";
import {
  ArrowRight,
  CheckCircle2,
  ClipboardCheck,
  Database,
  FileCheck2,
  Fingerprint,
  LockKeyhole,
  Microscope,
  Network,
  Search,
  ShieldCheck,
  Split,
  TableProperties,
  Workflow,
} from "lucide-react";

import { Eyebrow, PageShell } from "@/evidaraos/site";
import { modules } from "@/evidaraos/product-data";

const pipeline = [
  {
    label: "Question",
    detail: "Clinical, HEOR, regulatory, or discovery question",
  },
  {
    label: "Protocol",
    detail: "PICO/PECO, scope, criteria, and review plan",
  },
  {
    label: "Retrieval",
    detail: "PubMed, Semantic Scholar, Crossref, and source provenance",
  },
  {
    label: "Screening",
    detail: "Precision scoring, review queue, and exclusion reasons",
  },
  {
    label: "Extraction",
    detail: "Study fields, outcomes, limitations, and citations",
  },
  {
    label: "Validation",
    detail: "Human review, adjudication, metrics, and audit metadata",
  },
];

const techLayers = [
  {
    icon: Search,
    title: "Biomedical retrieval",
    body: "Concept expansion, Boolean strategies, source-specific queries, and deduplication.",
    items: ["PubMed", "Semantic Scholar", "Crossref", "optional arXiv"],
  },
  {
    icon: Split,
    title: "Precision control",
    body: "High-recall, balanced, and high-precision modes with recall guardrails.",
    items: ["concept match", "relevance score", "sentinel checks", "review tiers"],
  },
  {
    icon: TableProperties,
    title: "Evidence structuring",
    body: "Traceable extraction into review tables, model inputs, claims, and briefings.",
    items: ["population", "outcomes", "design", "limitations"],
  },
  {
    icon: ShieldCheck,
    title: "Governance layer",
    body: "Human decisions, validation reports, audit trails, and fixture-only safeguards.",
    items: ["dual review", "adjudication", "metrics", "audit pack"],
  },
];

const proofPoints = [
  ["No hidden conclusions", "AI suggestions stay separate from human decisions."],
  ["No fake validation claims", "Fixture demos are labeled as smoke tests only."],
  ["No unsupported metrics", "Performance requires human-labeled benchmark data."],
  ["No black-box reports", "Queries, sources, decisions, and rationale remain traceable."],
];

const evidenceRows = [
  ["Protocol", "PICO/PECO frame", "review-ready"],
  ["Retrieval", "3 source strategies", "provenance logged"],
  ["Dedup", "DOI, PMID, title", "summary generated"],
  ["Screening", "priority tiers", "human validation"],
  ["Extraction", "study fields", "confidence noted"],
  ["Report", "PRISMA + citations", "draft package"],
];

function QueryIntakePanel() {
  return (
    <div className="relative overflow-hidden border border-[#8ec7c1]/20 bg-[#071523] shadow-2xl shadow-black/30">
      <div className="absolute inset-0 opacity-35 [background-image:linear-gradient(rgba(142,199,193,0.14)_1px,transparent_1px),linear-gradient(90deg,rgba(142,199,193,0.1)_1px,transparent_1px)] [background-size:34px_34px]" />
      <div className="relative border-b border-white/10 p-5">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-xs font-semibold tracking-[0.22em] text-[#8ec7c1] uppercase">
              Evidence Query Intake
            </p>
            <p className="mt-2 text-sm text-[#aebbc5]">
              Convert a question into a governed workflow.
            </p>
          </div>
          <span className="border border-[#d7b46a]/35 px-3 py-1 text-xs text-[#e2c57f]">
            configured workflow
          </span>
        </div>
      </div>

      <div className="relative p-5">
        <label
          htmlFor="evidence-question"
          className="text-sm font-medium text-[#f8f1e3]"
        >
          Evidence question
        </label>
        <div className="mt-3 grid gap-3 md:grid-cols-[1fr_auto]">
          <input
            id="evidence-question"
            name="question"
            className="h-14 border border-white/10 bg-[#08111f] px-4 text-base text-[#f8f1e3] outline-none placeholder:text-[#738390] focus:border-[#8ec7c1]/70"
            placeholder="Example: dupilumab safety in adults with atopic dermatitis"
          />
          <Link
            href="/workspace/modules/precision-slr"
            className="inline-flex h-14 items-center justify-center gap-2 bg-[#d7b46a] px-5 text-sm font-semibold text-[#071523] hover:bg-[#f0cc80]"
          >
            Start SLR workflow
            <ArrowRight className="size-4" />
          </Link>
        </div>

        <div className="mt-5 grid gap-px overflow-hidden border border-white/10 bg-white/10 sm:grid-cols-3">
          {[
            ["Mode", "balanced precision"],
            ["Sources", "PubMed / Scholar / Crossref"],
            ["Oversight", "human review required"],
          ].map(([label, value]) => (
            <div key={label} className="bg-[#0b1828] p-4">
              <p className="text-xs tracking-[0.16em] text-[#8395a3] uppercase">
                {label}
              </p>
              <p className="mt-2 text-sm text-[#f8f1e3]">{value}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function EvidenceConsole() {
  return (
    <div className="overflow-hidden border border-white/10 bg-[#071523]">
      <div className="flex items-center justify-between border-b border-white/10 px-5 py-4">
        <div>
          <p className="text-xs font-semibold tracking-[0.22em] text-[#8ec7c1] uppercase">
            Precision SLR Run
          </p>
          <p className="mt-1 text-sm text-[#aebbc5]">
            Example surface, not live validation evidence
          </p>
        </div>
        <Microscope className="size-5 text-[#d7b46a]" />
      </div>
      <div className="grid gap-px bg-white/10 md:grid-cols-[0.78fr_1.22fr]">
        <div className="bg-[#08111f] p-5">
          <div className="border border-[#8ec7c1]/25 bg-[#0b1828] p-4">
            <p className="text-sm font-semibold text-[#f8f1e3]">
              Dupilumab safety in atopic dermatitis
            </p>
            <p className="mt-3 text-sm leading-6 text-[#aebbc5]">
              The workflow makes search strategy, precision tradeoffs,
              screening decisions, and extraction confidence inspectable.
            </p>
          </div>
          <div className="mt-5 grid grid-cols-2 gap-px bg-white/10 text-sm">
            {[
              ["Recall", "guarded"],
              ["Precision", "controlled"],
              ["Review", "dual-ready"],
              ["Audit", "active"],
            ].map(([label, value]) => (
              <div key={label} className="bg-[#071523] p-4">
                <p className="text-xs tracking-[0.16em] text-[#8395a3] uppercase">
                  {label}
                </p>
                <p className="mt-2 text-[#f8f1e3]">{value}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-[#0b1828]">
          <div className="grid grid-cols-[0.78fr_1fr_0.75fr] border-b border-white/10 px-5 py-3 text-xs font-semibold tracking-[0.16em] text-[#8ec7c1] uppercase">
            <span>Stage</span>
            <span>Artifact</span>
            <span>State</span>
          </div>
          {evidenceRows.map(([stage, artifact, state]) => (
            <div
              key={stage}
              className="grid grid-cols-[0.78fr_1fr_0.75fr] border-b border-white/10 px-5 py-4 text-sm last:border-b-0"
            >
              <span className="font-medium text-[#f8f1e3]">{stage}</span>
              <span className="text-[#c7d1d8]">{artifact}</span>
              <span className="text-[#d7b46a]">{state}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function WorkflowStack() {
  return (
    <div className="relative overflow-hidden border border-white/10 bg-[#071523]">
      <div className="absolute inset-0 opacity-35 [background-image:radial-gradient(circle_at_1px_1px,rgba(142,199,193,0.28)_1px,transparent_0)] [background-size:26px_26px]" />
      <div className="relative grid gap-px bg-white/10 lg:grid-cols-6">
        {pipeline.map((step, index) => (
          <div key={step.label} className="bg-[#08111f]/95 p-5">
            <div className="flex items-center justify-between">
              <span className="text-xs text-[#8ec7c1]">
                {String(index + 1).padStart(2, "0")}
              </span>
              {index < pipeline.length - 1 ? (
                <ArrowRight className="hidden size-4 text-[#d7b46a] lg:block" />
              ) : (
                <CheckCircle2 className="size-4 text-[#d7b46a]" />
              )}
            </div>
            <p className="mt-8 text-lg font-semibold text-[#f8f1e3]">
              {step.label}
            </p>
            <p className="mt-3 text-sm leading-6 text-[#aebbc5]">
              {step.detail}
            </p>
          </div>
        ))}
      </div>
      <div className="relative grid gap-px bg-white/10 lg:grid-cols-3">
        {[
          {
            icon: ClipboardCheck,
            title: "Protocol-bound",
            body: "Every workflow starts with scope, criteria, sources, and decision rules.",
          },
          {
            icon: Fingerprint,
            title: "Traceable by design",
            body: "Every record, extraction field, reviewer action, and report claim keeps provenance.",
          },
          {
            icon: LockKeyhole,
            title: "Governed output",
            body: "Validation reports and audit summaries travel with the final evidence package.",
          },
        ].map((item) => {
          const Icon = item.icon;
          return (
            <div key={item.title} className="bg-[#0b1828] p-6">
              <Icon className="mb-8 size-5 text-[#d7b46a]" />
              <h3 className="text-xl font-semibold text-[#f8f1e3]">
                {item.title}
              </h3>
              <p className="mt-3 text-sm leading-6 text-[#aebbc5]">
                {item.body}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function TechnologyLayer() {
  return (
    <div className="grid gap-6 lg:grid-cols-[0.92fr_1.08fr]">
      <div className="relative min-h-[560px] overflow-hidden border border-white/10 bg-[#071523] p-6">
        <div className="absolute inset-0 opacity-40 [background-image:linear-gradient(rgba(142,199,193,0.12)_1px,transparent_1px),linear-gradient(90deg,rgba(142,199,193,0.12)_1px,transparent_1px)] [background-size:46px_46px]" />
        <div className="absolute left-1/2 top-1/2 size-36 -translate-x-1/2 -translate-y-1/2 border border-[#d7b46a]/40 bg-[#08111f] p-5 shadow-2xl shadow-black/30">
          <Workflow className="mb-5 size-6 text-[#d7b46a]" />
          <p className="text-sm font-semibold text-[#f8f1e3]">EvidenceOS</p>
          <p className="mt-2 text-xs leading-5 text-[#9fb0bb]">
            governed evidence intelligence layer
          </p>
        </div>
        {[
          ["Protocol", ClipboardCheck, "9%", "16%"],
          ["Retrieval", Database, "57%", "11%"],
          ["Evidence Map", Network, "11%", "66%"],
          ["Validation", ShieldCheck, "58%", "66%"],
        ].map(([label, Icon, left, top]) => {
          const NodeIcon = Icon as typeof ClipboardCheck;
          return (
            <div
              key={label as string}
              className="absolute w-40 border border-[#8ec7c1]/35 bg-[#08111f]/95 p-4 shadow-2xl shadow-black/25"
              style={{ left: left as string, top: top as string }}
            >
              <NodeIcon className="mb-5 size-5 text-[#d7b46a]" />
              <p className="text-sm font-medium text-[#f8f1e3]">
                {label as string}
              </p>
            </div>
          );
        })}
        <div className="absolute left-[25%] right-[26%] top-[30%] h-px rotate-[18deg] bg-[#d7b46a]/35" />
        <div className="absolute left-[21%] right-[24%] top-[66%] h-px -rotate-[12deg] bg-[#8ec7c1]/35" />
        <div className="absolute bottom-0 left-0 right-0 border-t border-white/10 bg-[#08111f]/90 px-6 py-5">
          <div className="grid gap-3 text-xs text-[#c7d1d8] sm:grid-cols-3">
            <span>Source provenance</span>
            <span>Reviewer control</span>
            <span>Audit-ready output</span>
          </div>
        </div>
      </div>

      <div className="grid gap-px overflow-hidden border border-white/10 bg-white/10 sm:grid-cols-2">
        {techLayers.map((layer) => {
          const Icon = layer.icon;
          return (
            <div key={layer.title} className="bg-[#08111f] p-6">
              <Icon className="mb-10 size-6 text-[#d7b46a]" />
              <h3 className="text-2xl font-semibold leading-tight text-[#f8f1e3]">
                {layer.title}
              </h3>
              <p className="mt-4 text-sm leading-6 text-[#aebbc5]">
                {layer.body}
              </p>
              <div className="mt-8 flex flex-wrap gap-2">
                {layer.items.map((item) => (
                  <span
                    key={item}
                    className="border border-white/10 px-3 py-1 text-xs text-[#c7d1d8]"
                  >
                    {item}
                  </span>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function ModuleBand() {
  return (
    <div className="grid gap-px overflow-hidden border border-white/10 bg-white/10 lg:grid-cols-3">
      {modules.slice(0, 5).map((module, index) => {
        const Icon = module.icon;
        return (
          <Link
            key={module.id}
            href={module.publicRoute}
            className={`group bg-[#071523] p-6 hover:bg-[#0b1828] ${
              index === 0 ? "lg:col-span-2" : ""
            }`}
          >
            <div className="flex items-start justify-between gap-5">
              <Icon className="size-6 text-[#d7b46a]" />
              <ArrowRight className="size-5 text-[#8ec7c1] transition-transform group-hover:translate-x-1" />
            </div>
            <p className="mt-10 text-xs font-semibold tracking-[0.18em] text-[#8ec7c1] uppercase">
              {module.status}
            </p>
            <h3 className="mt-4 max-w-xl text-3xl font-semibold leading-tight text-[#f8f1e3]">
              {module.displayName}
            </h3>
            <p className="mt-4 max-w-xl text-sm leading-6 text-[#aebbc5]">
              {module.oneLiner}
            </p>
            <div className="mt-8 flex flex-wrap gap-2">
              {module.artifacts.slice(0, 4).map((artifact) => (
                <span
                  key={artifact}
                  className="border border-white/10 px-3 py-1 text-xs text-[#c7d1d8]"
                >
                  {artifact}
                </span>
              ))}
            </div>
          </Link>
        );
      })}
      <Link
        href="/governance"
        className="group bg-[#071523] p-6 hover:bg-[#0b1828]"
      >
        <ShieldCheck className="size-6 text-[#d7b46a]" />
        <p className="mt-10 text-xs font-semibold tracking-[0.18em] text-[#8ec7c1] uppercase">
          control layer
        </p>
        <h3 className="mt-4 text-3xl font-semibold leading-tight text-[#f8f1e3]">
          Evidence Governance & Validation
        </h3>
        <p className="mt-4 text-sm leading-6 text-[#aebbc5]">
          Human review, adjudication, validation reports, audit trails, and
          fixture-only controls across every module.
        </p>
      </Link>
    </div>
  );
}

export default function HomePage() {
  return (
    <PageShell>
      <main>
        <section className="relative overflow-hidden border-b border-white/10">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_0%,rgba(142,199,193,0.16),transparent_32%),radial-gradient(circle_at_80%_12%,rgba(215,180,106,0.12),transparent_28%)]" />
          <div className="relative mx-auto grid max-w-7xl gap-12 px-5 py-20 sm:px-8 lg:grid-cols-[0.9fr_1.1fr] lg:py-28">
            <div className="flex flex-col justify-center">
              <Eyebrow>EvidaraOS</Eyebrow>
              <h1 className="mt-5 max-w-4xl text-5xl font-semibold leading-[0.94] tracking-normal text-[#f8f1e3] md:text-7xl">
                Precision evidence generation for life sciences.
              </h1>
              <p className="mt-6 max-w-2xl text-lg leading-8 text-[#c7d1d8]">
                Turn biomedical literature, clinical evidence, and real-world
                data into traceable, validation-ready workflows for evidence,
                HEOR, regulatory, and market access teams.
              </p>
              <div className="mt-9 flex flex-wrap gap-3">
                <Link
                  href="/workspace/modules"
                  className="bg-[#d7b46a] px-5 py-3 text-sm font-medium text-[#08111f] hover:bg-[#f0cc80]"
                >
                  Open workspace
                </Link>
                <Link
                  href="/platform"
                  className="border border-white/15 px-5 py-3 text-sm font-medium text-[#f8f1e3] hover:border-[#8ec7c1]/60"
                >
                  See platform
                </Link>
              </div>
              <div className="mt-10 grid gap-3 text-sm leading-6 text-[#aebbc5] sm:grid-cols-3">
                {["Evidence generation", "HEOR and market access", "Regulatory strategy"].map(
                  (item) => (
                    <div key={item} className="border-l border-[#d7b46a] pl-4">
                      {item}
                    </div>
                  ),
                )}
              </div>
            </div>
            <div className="space-y-5">
              <QueryIntakePanel />
              <EvidenceConsole />
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-5 py-24 sm:px-8">
          <div className="mb-8 grid gap-8 lg:grid-cols-[0.72fr_1.28fr]">
            <div>
              <Eyebrow>Operating Model</Eyebrow>
              <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
                From evidence question to reviewable package.
              </h2>
            </div>
            <p className="max-w-3xl text-base leading-7 text-[#aebbc5] lg:pt-10">
              EvidaraOS is designed around the actual evidence workflow:
              protocol framing, controlled retrieval, screening, extraction,
              validation, reporting, and audit. Each step is visible before it
              becomes part of the final output.
            </p>
          </div>
          <WorkflowStack />
        </section>

        <section className="border-y border-white/10 bg-[#0b1828]">
          <div className="mx-auto max-w-7xl px-5 py-24 sm:px-8">
            <div className="mb-8 max-w-3xl">
              <Eyebrow>Technology Layer</Eyebrow>
              <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
                Biomedical retrieval, evidence structuring, and governance in
                one system.
              </h2>
              <p className="mt-5 text-base leading-7 text-[#aebbc5]">
                The visible product is simple. Underneath it, the system
                coordinates source retrieval, precision controls, structured
                extraction, human validation, and audit metadata.
              </p>
            </div>
            <TechnologyLayer />
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-5 py-24 sm:px-8">
          <div className="mb-8 grid gap-8 lg:grid-cols-[0.7fr_1.3fr]">
            <div>
              <Eyebrow>Product Modules</Eyebrow>
              <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
                Professional workflows, not generic skills.
              </h2>
            </div>
            <p className="max-w-3xl text-base leading-7 text-[#aebbc5] lg:pt-10">
              Each module maps to a concrete life-sciences evidence job and
              carries the same governance layer: human review, validation
              reporting, project manifests, fixture warnings, and audit trails.
            </p>
          </div>
          <ModuleBand />
        </section>

        <section className="border-y border-white/10 bg-[#071523]">
          <div className="mx-auto grid max-w-7xl gap-10 px-5 py-24 sm:px-8 lg:grid-cols-[0.76fr_1.24fr]">
            <div>
              <Eyebrow>Governance</Eyebrow>
              <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
                Built for human validation.
              </h2>
              <p className="mt-5 text-base leading-7 text-[#aebbc5]">
                The system supports AI-assisted work without pretending the AI
                is the final reviewer. It makes uncertainty, disagreement, and
                provenance part of the product surface.
              </p>
              <Link
                href="/governance"
                className="mt-8 inline-flex items-center gap-2 border border-white/15 px-5 py-3 text-sm font-medium text-[#f8f1e3] hover:border-[#8ec7c1]/60"
              >
                View governance layer
                <ArrowRight className="size-4" />
              </Link>
            </div>
            <div className="grid gap-px overflow-hidden border border-white/10 bg-white/10 md:grid-cols-2">
              {proofPoints.map(([title, body]) => (
                <div key={title} className="bg-[#08111f] p-6">
                  <FileCheck2 className="mb-10 size-6 text-[#d7b46a]" />
                  <h3 className="text-xl font-semibold text-[#f8f1e3]">
                    {title}
                  </h3>
                  <p className="mt-4 text-sm leading-6 text-[#aebbc5]">
                    {body}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="mx-auto grid max-w-7xl gap-8 px-5 py-24 sm:px-8 lg:grid-cols-[1fr_auto] lg:items-end">
          <div>
            <Eyebrow>Next Step</Eyebrow>
            <h2 className="mt-4 max-w-4xl text-4xl font-semibold leading-tight tracking-normal text-[#f8f1e3] md:text-6xl">
              Start with one evidence question.
            </h2>
            <p className="mt-6 max-w-2xl text-base leading-7 text-[#aebbc5]">
              Open the workspace, choose a configured module, and use a
              fixture-safe demo until live execution and validated benchmark
              data are connected.
            </p>
          </div>
          <div className="flex flex-wrap gap-3">
            <Link
              href="/workspace/modules"
              className="bg-[#d7b46a] px-5 py-3 text-sm font-medium text-[#08111f] hover:bg-[#f0cc80]"
            >
              Open workspace
            </Link>
            <Link
              href="/demo"
              className="border border-white/15 px-5 py-3 text-sm font-medium text-[#f8f1e3] hover:border-[#8ec7c1]/60"
            >
              Request demo
            </Link>
          </div>
        </section>
      </main>
    </PageShell>
  );
}
