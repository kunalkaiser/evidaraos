import Link from "next/link";
import {
  ArrowRight,
  BookOpenText,
  CheckCircle2,
  Database,
  ExternalLink,
  FileCheck2,
  Fingerprint,
  Layers3,
  LockKeyhole,
  MonitorCheck,
  Search,
  ShieldAlert,
  Split,
  TableProperties,
  Workflow,
} from "lucide-react";

import {
  demoProjects,
  governanceModule,
  lifecycle,
  modules,
  platformStats,
  visualNodes,
  type EvidenceModule,
} from "./product-data";
import { designContract } from "./design-contract";

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-40 border-b border-white/10 bg-[#08111f]/92 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-5 sm:px-8">
        <Link href="/" className="flex items-center gap-3">
          <span className="flex size-8 items-center justify-center border border-[#8ec7c1]/40 bg-[#0e2234] text-sm font-semibold text-[#dff7f2]">
            {designContract.brand.monogram}
          </span>
          <span className="text-sm font-semibold tracking-[0.18em] text-[#f8f1e3] uppercase">
            {designContract.brand.wordmark}
          </span>
        </Link>
        <nav className="hidden items-center gap-7 text-sm text-[#b9c4cc] lg:flex">
          <Link href="/platform" className="hover:text-[#f8f1e3]">
            Platform
          </Link>
          <Link
            href="/solutions/systematic-literature-review"
            className="hover:text-[#f8f1e3]"
          >
            Solutions
          </Link>
          <Link href="/evidence-engine" className="hover:text-[#f8f1e3]">
            Evidence Engine
          </Link>
          <Link href="/governance" className="hover:text-[#f8f1e3]">
            Governance
          </Link>
        </nav>
        <div className="flex items-center gap-3">
          <Link
            href="/workspace/modules"
            className="hidden border border-white/15 px-4 py-2 text-sm text-[#f8f1e3] hover:border-[#8ec7c1]/60 md:inline-flex"
          >
            Workspace
          </Link>
          <Link
            href="/demo"
            className="bg-[#d7b46a] px-4 py-2 text-sm font-medium text-[#08111f] hover:bg-[#f0cc80]"
          >
            Request demo
          </Link>
        </div>
      </div>
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className="border-t border-white/10 bg-[#070d17]">
      <div className="mx-auto grid max-w-7xl gap-8 px-5 py-10 text-sm text-[#9eabb6] sm:px-8 md:grid-cols-[1.2fr_1fr]">
        <div>
          <p className="font-semibold tracking-[0.18em] text-[#f8f1e3] uppercase">
            {designContract.brand.wordmark}
          </p>
          <p className="mt-3 max-w-xl leading-6">
            Precision evidence workflows for life-sciences teams. Governed
            artifacts, human review, and audit-ready evidence outputs.
          </p>
        </div>
        <div className="grid grid-cols-2 gap-3 text-[#c7d1d8]">
          <Link href="/platform" className="hover:text-[#f8f1e3]">
            Platform
          </Link>
          <Link href="/governance" className="hover:text-[#f8f1e3]">
            Governance
          </Link>
          <Link href="/data-methodology" className="hover:text-[#f8f1e3]">
            Data methodology
          </Link>
          <Link href="/workspace/modules" className="hover:text-[#f8f1e3]">
            Workspace
          </Link>
          <Link href="/legal/third-party" className="hover:text-[#f8f1e3]">
            Legal
          </Link>
        </div>
      </div>
    </footer>
  );
}

export function PageShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-[#08111f] text-[#f8f1e3]">
      <SiteHeader />
      {children}
      <SiteFooter />
    </div>
  );
}

export function Eyebrow({ children }: { children: React.ReactNode }) {
  return (
    <p className="text-xs font-semibold tracking-[0.26em] text-[#8ec7c1] uppercase">
      {children}
    </p>
  );
}

export function ArchitectureVisual() {
  return (
    <div className="relative min-h-[460px] overflow-hidden border border-white/10 bg-[#071523]">
      <div className="absolute inset-0 opacity-40 [background-image:linear-gradient(rgba(142,199,193,0.12)_1px,transparent_1px),linear-gradient(90deg,rgba(142,199,193,0.12)_1px,transparent_1px)] [background-size:44px_44px]" />
      <div className="absolute inset-x-10 top-1/2 h-px bg-[#8ec7c1]/35" />
      <div className="absolute left-[16%] right-[17%] top-[24%] h-px rotate-[12deg] bg-[#d7b46a]/30" />
      <div className="absolute left-[16%] right-[13%] top-[69%] h-px -rotate-[9deg] bg-[#d7b46a]/25" />
      <div className="absolute left-1/2 top-1/2 size-28 -translate-x-1/2 -translate-y-1/2 border border-[#d7b46a]/35 bg-[#08111f] p-5 shadow-2xl shadow-black/30">
        <Workflow className="mb-5 size-6 text-[#d7b46a]" />
        <p className="text-sm font-semibold text-[#f8f1e3]">EvidenceOS</p>
        <p className="mt-2 text-xs leading-5 text-[#9fb0bb]">
          governed evidence layer
        </p>
      </div>
      {visualNodes.map((node) => {
        const Icon = node.icon;
        return (
          <div
            key={node.label}
            className="absolute w-40 border border-[#8ec7c1]/35 bg-[#08111f]/95 p-4 shadow-2xl shadow-black/25"
            style={{ left: node.x, top: node.y }}
          >
            <Icon className="mb-5 size-5 text-[#d7b46a]" />
            <p className="text-sm font-medium text-[#f8f1e3]">{node.label}</p>
          </div>
        );
      })}
      <div className="absolute bottom-0 left-0 right-0 border-t border-white/10 bg-[#08111f]/90 px-6 py-5">
        <div className="grid gap-4 text-xs text-[#c7d1d8] md:grid-cols-3">
          <span>Protocol-bound retrieval</span>
          <span>Human review required</span>
          <span>Audit-ready artifacts</span>
        </div>
      </div>
    </div>
  );
}

export function HeroEvidenceConsole() {
  const rows = [
    ["Precision SLR", "high precision", "human review"],
    ["HEOR Modeler", "input extraction", "assumption flag"],
    ["Payer Dossier", "claim matrix", "source required"],
    ["Reg Briefing", "benefit-risk", "overclaim check"],
  ];

  return (
    <div className="relative overflow-hidden border border-white/10 bg-[#071523] shadow-2xl shadow-black/20">
      <div className="border-b border-white/10 px-5 py-4">
        <div className="flex items-center justify-between gap-4">
          <p className="text-xs font-semibold tracking-[0.22em] text-[#8ec7c1] uppercase">
            Evidence Operations Console
          </p>
          <span className="border border-[#d7b46a]/35 px-2 py-1 text-[11px] text-[#e2c57f]">
            fixture-safe demo
          </span>
        </div>
      </div>
      <div className="grid gap-px bg-white/10 md:grid-cols-[0.95fr_1.05fr]">
        <div className="bg-[#08111f] p-5">
          <p className="text-sm font-medium text-[#f8f1e3]">
            Dupilumab atopic dermatitis evidence workflow
          </p>
          <div className="mt-5 space-y-3">
            {[
              ["Query", "PICO framed"],
              ["Retrieval", "PubMed / Scholar / Crossref"],
              ["Screening", "prioritized queue"],
              ["Validation", "fixture warning active"],
            ].map(([label, value]) => (
              <div
                key={label}
                className="flex items-center justify-between border-b border-white/10 pb-3 text-sm"
              >
                <span className="text-[#8395a3]">{label}</span>
                <span className="text-[#f8f1e3]">{value}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="bg-[#0b1828] p-5">
          <div className="grid gap-3">
            {rows.map(([module, state, gate]) => (
              <div
                key={module}
                className="grid grid-cols-[1fr_auto] gap-3 border border-white/10 bg-[#08111f] p-3"
              >
                <div>
                  <p className="text-sm font-medium text-[#f8f1e3]">{module}</p>
                  <p className="mt-1 text-xs text-[#8ec7c1]">{state}</p>
                </div>
                <span className="self-start border border-[#d7b46a]/30 px-2 py-1 text-[11px] text-[#e2c57f]">
                  {gate}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className="grid grid-cols-4 border-t border-white/10 text-center text-xs text-[#aebbc5]">
        {["Protocol", "Evidence map", "Review", "Audit"].map((item) => (
          <span key={item} className="border-r border-white/10 px-2 py-3 last:border-r-0">
            {item}
          </span>
        ))}
      </div>
    </div>
  );
}

export function EvidenceArtifactMosaic() {
  const primary = [
    {
      label: "Precision Literature Review",
      title: "Screening queue with recall guardrail",
      meta: "PICO / search / dedup / PRISMA",
      status: "human review required",
    },
    {
      label: "HEOR Evidence Modeler",
      title: "Model input table with assumption flags",
      meta: "inputs / uncertainty / provenance",
      status: "economist review required",
    },
    {
      label: "Drug Repurposing Explorer",
      title: "Method evidence matrix",
      meta: "KG / target / literature / risk",
      status: "hypothesis only",
    },
  ];

  const side = [
    ["Audit trail", "tool version / source / decision"],
    ["Validation report", "fixture warning / metrics / limitations"],
    ["Payer dossier", "claim matrix / gap check / evidence blocks"],
    ["Regulatory briefing", "benefit-risk / uncertainty / language guardrail"],
  ];

  return (
    <div className="grid gap-px overflow-hidden border border-white/10 bg-white/10 lg:grid-cols-[1.2fr_0.8fr]">
      <div className="grid gap-px bg-white/10 md:grid-cols-3">
        {primary.map((item, index) => (
          <div key={item.label} className="bg-[#071523] p-5">
            <div className="flex items-start justify-between gap-4">
              <p className="text-xs font-semibold tracking-[0.18em] text-[#8ec7c1] uppercase">
                {String(index + 1).padStart(2, "0")}
              </p>
              <span className="border border-[#d7b46a]/30 px-2 py-1 text-[11px] text-[#e2c57f]">
                artifact
              </span>
            </div>
            <p className="mt-10 text-xs font-semibold tracking-[0.16em] text-[#8ec7c1] uppercase">
              {item.label}
            </p>
            <h3 className="mt-3 text-2xl font-semibold leading-tight text-[#f8f1e3]">
              {item.title}
            </h3>
            <p className="mt-5 text-sm leading-6 text-[#aebbc5]">{item.meta}</p>
            <div className="mt-8 border-t border-white/10 pt-4 text-xs text-[#c7d1d8]">
              {item.status}
            </div>
          </div>
        ))}
      </div>
      <div className="grid gap-px bg-white/10">
        {side.map(([title, detail]) => (
          <div key={title} className="bg-[#0b1828] p-5">
            <p className="text-lg font-semibold text-[#f8f1e3]">{title}</p>
            <p className="mt-2 text-sm leading-6 text-[#aebbc5]">{detail}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export function TheWorkBand() {
  const work = [
    {
      icon: Database,
      title: "Bring evidence into one operating model",
      detail:
        "Biomedical literature, trial context, economic inputs, payer claims, regulatory precedent, and real-world evidence signals are handled as source-bound inputs.",
    },
    {
      icon: TableProperties,
      title: "Convert inputs into reviewable artifacts",
      detail:
        "The platform produces protocols, evidence maps, claim matrices, model-input tables, reviewer queues, validation reports, and audit trails.",
    },
    {
      icon: MonitorCheck,
      title: "Keep humans in the decision path",
      detail:
        "AI-assisted steps are routed through reviewer decisions, overrides, adjudication, limitations, and final decision capture.",
    },
  ];

  return (
    <section className="border-y border-white/10 bg-[#071523]">
      <div className="mx-auto max-w-7xl px-5 py-24 sm:px-8">
        <div className="grid gap-10 lg:grid-cols-[0.72fr_1.28fr]">
          <div>
            <Eyebrow>The Work</Eyebrow>
            <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
              From evidence chaos to governed evidence operations.
            </h2>
          </div>
          <div className="grid gap-px bg-white/10">
            {work.map((item) => {
              const Icon = item.icon;
              return (
                <div
                  key={item.title}
                  className="grid gap-5 bg-[#08111f] p-6 md:grid-cols-[72px_1fr]"
                >
                  <div className="flex size-12 items-center justify-center border border-[#8ec7c1]/35 bg-[#0b1828]">
                    <Icon className="size-5 text-[#d7b46a]" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold text-[#f8f1e3]">
                      {item.title}
                    </h3>
                    <p className="mt-3 text-sm leading-6 text-[#aebbc5]">
                      {item.detail}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}

export function EnterpriseProofSection() {
  const items = [
    {
      icon: Search,
      label: "Precision retrieval",
      body: "Search strategies can be tuned for high recall, balanced review, or high precision workflows.",
    },
    {
      icon: Layers3,
      label: "Evidence maps",
      body: "Records, claims, inputs, and graph paths are organized into traceable review artifacts.",
    },
    {
      icon: FileCheck2,
      label: "Validation pack",
      body: "Reports preserve fixture-only warnings, reviewer decisions, adjudication status, and limitations.",
    },
    {
      icon: LockKeyhole,
      label: "Audit surface",
      body: "Project manifests and audit events retain source provenance, tool metadata, and workflow status.",
    },
  ];

  return (
    <section className="border-y border-white/10 bg-[#0b1828]">
      <div className="mx-auto grid max-w-7xl gap-px bg-white/10 px-5 py-px sm:px-8 lg:grid-cols-4">
        {items.map((item) => {
          const Icon = item.icon;
          return (
            <div key={item.label} className="bg-[#08111f] p-6">
              <Icon className="mb-8 size-6 text-[#d7b46a]" />
              <p className="text-lg font-semibold text-[#f8f1e3]">
                {item.label}
              </p>
              <p className="mt-3 text-sm leading-6 text-[#aebbc5]">
                {item.body}
              </p>
            </div>
          );
        })}
      </div>
    </section>
  );
}

export function ResourcesBand() {
  const resources = [
    {
      title: "Evidence methodology",
      detail: "How EvidaraOS separates sources, AI interpretation, human decision, validation status, and limitations.",
      href: "/data-methodology",
    },
    {
      title: "Governance layer",
      detail: "Human review queues, adjudication, validation reports, audit metadata, and fixture-only controls.",
      href: "/governance",
    },
    {
      title: "Evidence engine",
      detail: "The lifecycle that connects protocol, retrieval, extraction, validation, reporting, and audit.",
      href: "/evidence-engine",
    },
  ];

  return (
    <section className="mx-auto max-w-7xl px-5 py-24 sm:px-8">
      <div className="mb-8 flex flex-col justify-between gap-5 md:flex-row md:items-end">
        <div>
          <Eyebrow>Resources</Eyebrow>
          <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
            Methods, governance, and evidence architecture.
          </h2>
        </div>
        <p className="max-w-md text-sm leading-6 text-[#aebbc5]">
          Resource pages are built to explain methodology and constraints,
          not to inflate unsupported performance claims.
        </p>
      </div>
      <div className="grid gap-px overflow-hidden border border-white/10 bg-white/10 md:grid-cols-3">
        {resources.map((resource) => (
          <Link
            key={resource.title}
            href={resource.href}
            className="group bg-[#0b1828] p-6 hover:bg-[#0e2234]"
          >
            <BookOpenText className="mb-8 size-6 text-[#d7b46a]" />
            <h3 className="text-xl font-semibold text-[#f8f1e3]">
              {resource.title}
            </h3>
            <p className="mt-4 text-sm leading-6 text-[#aebbc5]">
              {resource.detail}
            </p>
            <div className="mt-8 flex items-center gap-2 text-sm text-[#8ec7c1]">
              Open resource
              <ArrowRight className="size-4 transition-transform group-hover:translate-x-1" />
            </div>
          </Link>
        ))}
      </div>
    </section>
  );
}

export function EnterpriseCta() {
  return (
    <section className="border-t border-white/10 bg-[#070d17]">
      <div className="mx-auto grid max-w-7xl gap-8 px-5 py-20 sm:px-8 lg:grid-cols-[1fr_auto] lg:items-end">
        <div>
          <Eyebrow>Enterprise Review</Eyebrow>
          <h2 className="mt-4 max-w-4xl text-4xl font-semibold leading-tight tracking-normal text-[#f8f1e3] md:text-6xl">
            Build evidence workflows your reviewers can inspect.
          </h2>
          <p className="mt-6 max-w-2xl text-base leading-7 text-[#aebbc5]">
            Start with fixture-labeled demos, connect real evidence sources,
            then move toward human-labeled validation and production governance.
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <Link
            href="/demo"
            className="bg-[#d7b46a] px-5 py-3 text-sm font-medium text-[#08111f] hover:bg-[#f0cc80]"
          >
            Request demo
          </Link>
          <Link
            href="/workspace/modules"
            className="border border-white/15 px-5 py-3 text-sm font-medium text-[#f8f1e3] hover:border-[#8ec7c1]/60"
          >
            View workspace
          </Link>
        </div>
      </div>
    </section>
  );
}

export function EvidencePipelinePanel() {
  const columns = [
    {
      title: "Evidence inputs",
      icon: Database,
      items: ["Biomedical literature", "Clinical evidence", "Economic inputs", "Payer claims", "Regulatory context"],
    },
    {
      title: "Governed processing",
      icon: Workflow,
      items: ["Protocol framing", "Evidence maps", "Screening queues", "Extraction tables", "Living updates"],
    },
    {
      title: "Controlled outputs",
      icon: ShieldAlert,
      items: ["Review packets", "Validation reports", "PRISMA summaries", "Dossiers", "Audit trails"],
    },
  ];

  return (
    <div className="grid gap-px bg-white/10 lg:grid-cols-3">
      {columns.map((column) => {
        const Icon = column.icon;
        return (
          <div key={column.title} className="bg-[#071523] p-6">
            <Icon className="mb-8 size-6 text-[#8ec7c1]" />
            <h3 className="text-2xl font-semibold text-[#f8f1e3]">
              {column.title}
            </h3>
            <div className="mt-6 space-y-3">
              {column.items.map((item) => (
                <div
                  key={item}
                  className="border-l border-[#d7b46a]/50 pl-4 text-sm text-[#c7d1d8]"
                >
                  {item}
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}

export function EvidenceStackDiagram() {
  const layers = [
    {
      label: "Source Layer",
      detail: "PubMed, scholarly metadata, claim files, model inputs, agency context",
      tone: "border-[#8ec7c1]/45",
    },
    {
      label: "Normalization Layer",
      detail: "Records, concepts, claims, parameters, entities, relations, provenance",
      tone: "border-[#8ec7c1]/35",
    },
    {
      label: "Evidence Intelligence Layer",
      detail: "Precision retrieval, evidence maps, scoring, extraction, living updates",
      tone: "border-[#d7b46a]/45",
    },
    {
      label: "Human Oversight Layer",
      detail: "Reviewer queues, overrides, adjudication, rationale capture",
      tone: "border-[#d7b46a]/35",
    },
    {
      label: "Validation and Audit Layer",
      detail: "Validation reports, fixture warnings, audit trail, project manifest",
      tone: "border-white/20",
    },
  ];

  return (
    <div className="relative overflow-hidden border border-white/10 bg-[#071523] p-6">
      <div className="absolute inset-y-6 left-10 w-px bg-[#8ec7c1]/30" />
      <div className="space-y-4">
        {layers.map((layer, index) => (
          <div
            key={layer.label}
            className={`relative ml-8 border ${layer.tone} bg-[#08111f] p-5 shadow-xl shadow-black/10`}
          >
            <div className="absolute -left-[43px] top-5 flex size-5 items-center justify-center border border-[#8ec7c1]/50 bg-[#071523] text-[10px] text-[#8ec7c1]">
              {index + 1}
            </div>
            <div className="flex flex-col justify-between gap-4 md:flex-row md:items-start">
              <div>
                <p className="text-lg font-semibold text-[#f8f1e3]">
                  {layer.label}
                </p>
                <p className="mt-2 max-w-2xl text-sm leading-6 text-[#aebbc5]">
                  {layer.detail}
                </p>
              </div>
              <span className="shrink-0 border border-white/10 px-3 py-1 text-xs text-[#c7d1d8]">
                governed
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export function SystemFlowDiagram() {
  const columns = [
    {
      title: "Evidence Inputs",
      icon: Database,
      items: ["Literature", "Trials", "Economic inputs", "Payer evidence", "Regulatory context"],
    },
    {
      title: "Agent Workflows",
      icon: Split,
      items: ["SLR", "HEOR", "Payer dossier", "Reg briefing", "Repurposing"],
    },
    {
      title: "Governance Controls",
      icon: Fingerprint,
      items: ["Human review", "Adjudication", "Validation", "Audit trail", "Fixture warnings"],
    },
    {
      title: "Evidence Outputs",
      icon: FileCheck2,
      items: ["Review report", "Model inputs", "Claim matrix", "Briefing", "Evidence graph"],
    },
  ];

  return (
    <div className="overflow-hidden border border-white/10 bg-[#071523]">
      <div className="grid gap-px bg-white/10 lg:grid-cols-4">
        {columns.map((column, columnIndex) => {
          const Icon = column.icon;
          return (
            <div key={column.title} className="relative bg-[#08111f] p-5">
              {columnIndex < columns.length - 1 && (
                <div className="absolute right-[-18px] top-10 z-10 hidden h-px w-9 bg-[#d7b46a]/50 lg:block" />
              )}
              <Icon className="mb-8 size-6 text-[#d7b46a]" />
              <p className="text-xl font-semibold text-[#f8f1e3]">
                {column.title}
              </p>
              <div className="mt-6 space-y-2">
                {column.items.map((item) => (
                  <div
                    key={item}
                    className="border border-white/10 bg-[#0b1828] px-3 py-2 text-sm text-[#c7d1d8]"
                  >
                    {item}
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
      <div className="border-t border-white/10 bg-[#0b1828] px-5 py-4 text-sm text-[#aebbc5]">
        EvidaraOS organizes biomedical evidence workflows into traceable
        artifacts, validation checkpoints, and human-review surfaces.
      </div>
    </div>
  );
}

export function MethodologyRail() {
  const steps = [
    ["01", "Frame", "Question, protocol, scope, criteria"],
    ["02", "Retrieve", "Searches, source logs, records"],
    ["03", "Map", "Signals, concepts, claims, graph paths"],
    ["04", "Review", "Human decision, override, adjudication"],
    ["05", "Validate", "Metrics, completeness, fixture warnings"],
    ["06", "Publish", "Report, dossier, briefing, audit pack"],
  ];

  return (
    <div className="grid gap-px bg-white/10 md:grid-cols-2 xl:grid-cols-6">
      {steps.map(([num, title, body]) => (
        <div key={num} className="bg-[#071523] p-5">
          <p className="text-xs text-[#8ec7c1]">{num}</p>
          <p className="mt-6 text-xl font-semibold text-[#f8f1e3]">{title}</p>
          <p className="mt-3 text-sm leading-6 text-[#aebbc5]">{body}</p>
        </div>
      ))}
    </div>
  );
}

export function ModuleBand({ module }: { module: EvidenceModule }) {
  const Icon = module.icon;
  return (
    <Link
      href={module.publicRoute}
      className="group grid gap-5 border-t border-white/10 py-7 md:grid-cols-[220px_1fr_220px]"
    >
      <div className="flex items-center gap-3">
        <span className="flex size-10 items-center justify-center border border-[#8ec7c1]/25 bg-[#0c1b2c]">
          <Icon className="size-5 text-[#8ec7c1]" />
        </span>
        <span className="text-sm font-semibold text-[#f8f1e3]">
          {module.shortName}
        </span>
      </div>
      <div>
        <h3 className="text-xl font-semibold text-[#f8f1e3]">
          {module.displayName}
        </h3>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-[#aebbc5]">
          {module.oneLiner}
        </p>
      </div>
      <div className="flex items-center justify-between gap-4 md:justify-end">
        <span className="border border-[#d7b46a]/35 px-3 py-1 text-xs text-[#e2c57f]">
          {module.status}
        </span>
        <ArrowRight className="size-5 text-[#8ec7c1] transition-transform group-hover:translate-x-1" />
      </div>
    </Link>
  );
}

export function ModuleMatrix() {
  return (
    <div className="overflow-hidden border border-white/10">
      <div className="grid grid-cols-[1.1fr_0.9fr_0.9fr_0.9fr] bg-[#071523] text-xs font-semibold tracking-[0.18em] text-[#8ec7c1] uppercase max-lg:hidden">
        <div className="border-r border-white/10 p-4">Module</div>
        <div className="border-r border-white/10 p-4">Primary workflow</div>
        <div className="border-r border-white/10 p-4">Governance artifact</div>
        <div className="p-4">Workspace status</div>
      </div>
      {modules.map((module) => {
        const Icon = module.icon;
        return (
          <Link
            href={module.publicRoute}
            key={module.id}
            className="group grid gap-px border-t border-white/10 bg-white/10 lg:grid-cols-[1.1fr_0.9fr_0.9fr_0.9fr]"
          >
            <div className="bg-[#08111f] p-5">
              <div className="flex items-center gap-3">
                <Icon className="size-5 text-[#d7b46a]" />
                <p className="font-semibold text-[#f8f1e3]">
                  {module.displayName}
                </p>
              </div>
              <p className="mt-3 text-sm leading-6 text-[#aebbc5]">
                {module.oneLiner}
              </p>
            </div>
            <div className="bg-[#0b1828] p-5 text-sm text-[#c7d1d8]">
              {module.workflow.slice(0, 3).join(" / ")}
            </div>
            <div className="bg-[#0b1828] p-5 text-sm text-[#c7d1d8]">
              {module.artifacts.includes("Audit trail")
                ? "Validation report + audit trail"
                : "Human review + audit trail"}
            </div>
            <div className="flex items-center justify-between gap-4 bg-[#0b1828] p-5 text-sm text-[#8ec7c1]">
              {module.status}
              <ArrowRight className="size-4 transition-transform group-hover:translate-x-1" />
            </div>
          </Link>
        );
      })}
    </div>
  );
}

export function DemoProjectCards() {
  return (
    <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
      {demoProjects.map((project) => {
        const module = modules.find((item) => item.id === project.moduleId);
        return (
          <div
            key={project.id}
            className="border border-white/10 bg-[#0b1828] p-5"
          >
            <div className="flex items-start justify-between gap-3">
              <p className="text-sm font-semibold text-[#f8f1e3]">
                {project.title}
              </p>
              <span className="border border-[#d7b46a]/35 px-2 py-1 text-[11px] text-[#e2c57f]">
                fixture
              </span>
            </div>
            <p className="mt-3 text-xs uppercase tracking-[0.18em] text-[#8ec7c1]">
              {module?.shortName}
            </p>
            <p className="mt-4 text-sm text-[#aebbc5]">
              {project.artifactCount} configured artifacts. Fixture-only demo
              content, not validation evidence.
            </p>
          </div>
        );
      })}
    </div>
  );
}

export function WorkflowStrip() {
  return (
    <div className="grid gap-px overflow-hidden border border-white/10 bg-white/10 md:grid-cols-3 xl:grid-cols-9">
      {lifecycle.map((step, index) => (
        <div key={step} className="bg-[#0b1828] p-4">
          <p className="text-xs text-[#8ec7c1]">{String(index + 1).padStart(2, "0")}</p>
          <p className="mt-3 text-sm font-medium text-[#f8f1e3]">{step}</p>
        </div>
      ))}
    </div>
  );
}

export function GovernancePanel() {
  const Icon = governanceModule.icon;
  return (
    <section className="border-y border-white/10 bg-[#0b1828]">
      <div className="mx-auto grid max-w-7xl gap-10 px-5 py-20 sm:px-8 lg:grid-cols-[0.8fr_1.2fr]">
        <div>
          <Eyebrow>Governance</Eyebrow>
          <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
            Human oversight is built into the workflow.
          </h2>
          <p className="mt-5 max-w-xl text-base leading-7 text-[#aebbc5]">
            EvidenceOS treats review, validation, fixture warnings, and audit
            trails as product primitives rather than after-the-fact paperwork.
          </p>
        </div>
        <div className="grid gap-px bg-white/10 md:grid-cols-2">
          {governanceModule.controls.map((control) => (
            <div key={control} className="bg-[#08111f] p-5">
              <Icon className="mb-5 size-5 text-[#d7b46a]" />
              <p className="text-sm font-medium text-[#f8f1e3]">{control}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export function StatusPill({ children }: { children: React.ReactNode }) {
  return (
    <span className="inline-flex border border-[#8ec7c1]/30 px-3 py-1 text-xs text-[#8ec7c1]">
      {children}
    </span>
  );
}

export function StatRow() {
  return (
    <div className="grid border-y border-white/10 md:grid-cols-4">
      {platformStats.map((stat) => (
        <div key={stat.label} className="border-white/10 px-5 py-6 md:border-r">
          <p className="text-3xl font-semibold text-[#f8f1e3]">{stat.value}</p>
          <p className="mt-2 text-sm text-[#aebbc5]">{stat.label}</p>
        </div>
      ))}
    </div>
  );
}

export function GuardrailList({ items }: { items: string[] }) {
  return (
    <div className="space-y-3">
      {items.map((item) => (
        <div key={item} className="flex gap-3 text-sm leading-6 text-[#c7d1d8]">
          <CheckCircle2 className="mt-1 size-4 shrink-0 text-[#8ec7c1]" />
          <span>{item}</span>
        </div>
      ))}
    </div>
  );
}

export function TextLink({
  href,
  children,
}: {
  href: string;
  children: React.ReactNode;
}) {
  return (
    <Link
      href={href}
      className="inline-flex items-center gap-2 text-sm font-medium text-[#d7b46a] hover:text-[#f0cc80]"
    >
      {children}
      <ExternalLink className="size-4" />
    </Link>
  );
}
