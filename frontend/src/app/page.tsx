import Link from "next/link";
import {
  ArrowRight,
  ClipboardCheck,
  Search,
  ShieldCheck,
  TableProperties,
} from "lucide-react";

import { Eyebrow, PageShell } from "@/evidaraos/site";
import { modules } from "@/evidaraos/product-data";

const workbenchRows = [
  ["Question", "Dupilumab safety in atopic dermatitis", "protocol draft"],
  ["Search", "PubMed + Semantic Scholar + Crossref", "sources logged"],
  ["Screen", "1,284 records prioritized", "human review"],
  ["Extract", "Safety, efficacy, population, follow-up", "table ready"],
  ["Report", "PRISMA + limitations + citations", "draft package"],
];

const workflow = [
  "Question",
  "Protocol",
  "Search",
  "Screen",
  "Extract",
  "Validate",
  "Report",
];

const proof = [
  {
    icon: Search,
    title: "Precision search",
    body: "Generate broad, balanced, and high-precision strategies before teams commit to screening.",
  },
  {
    icon: ClipboardCheck,
    title: "Reviewer control",
    body: "Separate AI suggestions from human decisions, overrides, and adjudication notes.",
  },
  {
    icon: TableProperties,
    title: "Structured extraction",
    body: "Move evidence into tables with fields, confidence, limitations, and citations intact.",
  },
  {
    icon: ShieldCheck,
    title: "Audit trail",
    body: "Track source, query, tool version, prompt version, rationale, and final decision.",
  },
];

const useCases = [
  "Systematic literature review",
  "HEOR model input foundation",
  "Payer value dossier support",
  "Regulatory evidence briefing",
  "Drug repurposing hypothesis review",
  "Evidence governance and validation",
];

function ProductWorkbench() {
  return (
    <div className="overflow-hidden border border-white/10 bg-[#071523] shadow-2xl shadow-black/30">
      <div className="flex items-center justify-between border-b border-white/10 px-5 py-4">
        <div>
          <p className="text-xs font-semibold tracking-[0.2em] text-[#8ec7c1] uppercase">
            Evidence Workbench
          </p>
          <p className="mt-1 text-sm text-[#aebbc5]">
            Example workflow surface, fixture-only
          </p>
        </div>
        <span className="border border-[#d7b46a]/35 px-3 py-1 text-xs text-[#e2c57f]">
          review mode
        </span>
      </div>

      <div className="grid gap-px bg-white/10 lg:grid-cols-[0.85fr_1.15fr]">
        <div className="bg-[#08111f] p-5">
          <div className="border border-[#8ec7c1]/25 bg-[#0b1828] p-4">
            <p className="text-sm font-semibold text-[#f8f1e3]">
              Precision Literature Review
            </p>
            <p className="mt-3 text-sm leading-6 text-[#aebbc5]">
              Search, screening, extraction, PRISMA, validation report.
            </p>
          </div>
          <div className="mt-5 grid grid-cols-2 gap-px bg-white/10 text-sm">
            {[
              ["Mode", "balanced"],
              ["Review", "dual reviewer"],
              ["Sources", "3 connected"],
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
          <div className="grid grid-cols-[0.9fr_1.15fr_0.75fr] border-b border-white/10 px-5 py-3 text-xs font-semibold tracking-[0.16em] text-[#8ec7c1] uppercase">
            <span>Step</span>
            <span>Artifact</span>
            <span>Status</span>
          </div>
          {workbenchRows.map(([step, artifact, status]) => (
            <div
              key={step}
              className="grid grid-cols-[0.9fr_1.15fr_0.75fr] border-b border-white/10 px-5 py-4 text-sm last:border-b-0"
            >
              <span className="font-medium text-[#f8f1e3]">{step}</span>
              <span className="text-[#c7d1d8]">{artifact}</span>
              <span className="text-[#d7b46a]">{status}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function ModuleGrid() {
  return (
    <div className="grid gap-px overflow-hidden border border-white/10 bg-white/10 md:grid-cols-2 xl:grid-cols-3">
      {modules.slice(0, 5).map((module) => {
        const Icon = module.icon;
        return (
          <Link
            key={module.id}
            href={module.publicRoute}
            className="group bg-[#071523] p-6 hover:bg-[#0b1828]"
          >
            <div className="flex items-start justify-between gap-5">
              <Icon className="size-6 text-[#d7b46a]" />
              <ArrowRight className="size-5 text-[#8ec7c1] transition-transform group-hover:translate-x-1" />
            </div>
            <h3 className="mt-10 text-2xl font-semibold leading-tight text-[#f8f1e3]">
              {module.displayName}
            </h3>
            <p className="mt-4 text-sm leading-6 text-[#aebbc5]">
              {module.oneLiner}
            </p>
            <p className="mt-8 border-t border-white/10 pt-4 text-xs font-semibold tracking-[0.16em] text-[#8ec7c1] uppercase">
              {module.status}
            </p>
          </Link>
        );
      })}
      <Link
        href="/governance"
        className="group bg-[#071523] p-6 hover:bg-[#0b1828]"
      >
        <ShieldCheck className="size-6 text-[#d7b46a]" />
        <h3 className="mt-10 text-2xl font-semibold leading-tight text-[#f8f1e3]">
          Evidence Governance & Validation
        </h3>
        <p className="mt-4 text-sm leading-6 text-[#aebbc5]">
          Human review, adjudication, validation reports, audit trails, and
          fixture-only controls across every workflow.
        </p>
        <p className="mt-8 border-t border-white/10 pt-4 text-xs font-semibold tracking-[0.16em] text-[#8ec7c1] uppercase">
          platform control layer
        </p>
      </Link>
    </div>
  );
}

function WorkflowRail() {
  return (
    <div className="overflow-hidden border border-white/10 bg-[#071523]">
      <div className="grid gap-px bg-white/10 md:grid-cols-7">
        {workflow.map((step, index) => (
          <div key={step} className="relative bg-[#08111f] p-5">
            {index < workflow.length - 1 && (
              <div className="absolute right-[-18px] top-8 z-10 hidden h-px w-9 bg-[#d7b46a]/50 md:block" />
            )}
            <p className="text-xs text-[#8ec7c1]">
              {String(index + 1).padStart(2, "0")}
            </p>
            <p className="mt-5 text-sm font-semibold text-[#f8f1e3]">{step}</p>
          </div>
        ))}
      </div>
      <div className="grid gap-px bg-white/10 lg:grid-cols-3">
        {[
          ["Before AI", "Protocol, scope, criteria, and source plan."],
          ["During AI", "Search, score, screen, extract, and flag uncertainty."],
          ["After AI", "Human review, validation report, citations, audit pack."],
        ].map(([title, body]) => (
          <div key={title} className="bg-[#0b1828] p-6">
            <p className="text-lg font-semibold text-[#f8f1e3]">{title}</p>
            <p className="mt-3 text-sm leading-6 text-[#aebbc5]">{body}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function HomePage() {
  return (
    <PageShell>
      <main>
        <section className="border-b border-white/10">
          <div className="mx-auto grid max-w-7xl gap-12 px-5 py-20 sm:px-8 lg:grid-cols-[0.88fr_1.12fr] lg:py-28">
            <div className="flex flex-col justify-center">
              <Eyebrow>EvidaraOS</Eyebrow>
              <h1 className="mt-5 max-w-4xl text-5xl font-semibold leading-[0.95] tracking-normal text-[#f8f1e3] md:text-7xl">
                Evidence workbench for life sciences teams.
              </h1>
              <p className="mt-6 max-w-2xl text-lg leading-8 text-[#c7d1d8]">
                Search, screen, extract, validate, and report biomedical
                evidence with traceable human oversight.
              </p>
              <div className="mt-9 flex flex-wrap gap-3">
                <Link
                  href="/platform"
                  className="bg-[#d7b46a] px-5 py-3 text-sm font-medium text-[#08111f] hover:bg-[#f0cc80]"
                >
                  View platform
                </Link>
                <Link
                  href="/demo"
                  className="border border-white/15 px-5 py-3 text-sm font-medium text-[#f8f1e3] hover:border-[#8ec7c1]/60"
                >
                  Request demo
                </Link>
              </div>
              <div className="mt-10 grid gap-3 text-sm leading-6 text-[#aebbc5] sm:grid-cols-3">
                {["Evidence teams", "HEOR teams", "Regulatory and market access"].map(
                  (item) => (
                    <div key={item} className="border-l border-[#d7b46a] pl-4">
                      {item}
                    </div>
                  ),
                )}
              </div>
            </div>
            <ProductWorkbench />
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-5 py-24 sm:px-8">
          <div className="mb-8 max-w-3xl">
            <Eyebrow>What It Does</Eyebrow>
            <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
              One workspace for evidence-heavy work.
            </h2>
            <p className="mt-5 text-base leading-7 text-[#aebbc5]">
              EvidaraOS turns messy evidence tasks into reviewable product
              modules. No hidden conclusions. No fake performance claims.
            </p>
          </div>
          <ModuleGrid />
        </section>

        <section className="border-y border-white/10 bg-[#0b1828]">
          <div className="mx-auto grid max-w-7xl gap-10 px-5 py-24 sm:px-8 lg:grid-cols-[0.72fr_1.28fr]">
            <div>
              <Eyebrow>How Work Moves</Eyebrow>
              <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
                From question to evidence package.
              </h2>
              <p className="mt-5 text-base leading-7 text-[#aebbc5]">
                The platform keeps each step visible so teams can inspect what
                was searched, why records were prioritized, what humans changed,
                and what evidence supports the final report.
              </p>
            </div>
            <WorkflowRail />
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-5 py-24 sm:px-8">
          <div className="mb-8 grid gap-8 lg:grid-cols-[0.78fr_1.22fr]">
            <div>
              <Eyebrow>Governance</Eyebrow>
              <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
                Built for review, not blind automation.
              </h2>
            </div>
            <p className="max-w-3xl text-base leading-7 text-[#aebbc5] lg:pt-10">
              AI can speed up evidence work, but regulated teams need the
              decision trail. EvidaraOS keeps sources, model outputs, reviewer
              decisions, limitations, and audit metadata separate.
            </p>
          </div>
          <div className="grid gap-px overflow-hidden border border-white/10 bg-white/10 md:grid-cols-2 xl:grid-cols-4">
            {proof.map((item) => {
              const Icon = item.icon;
              return (
                <div key={item.title} className="bg-[#071523] p-6">
                  <Icon className="mb-10 size-6 text-[#d7b46a]" />
                  <h3 className="text-xl font-semibold text-[#f8f1e3]">
                    {item.title}
                  </h3>
                  <p className="mt-4 text-sm leading-6 text-[#aebbc5]">
                    {item.body}
                  </p>
                </div>
              );
            })}
          </div>
        </section>

        <section className="border-y border-white/10 bg-[#071523]">
          <div className="mx-auto grid max-w-7xl gap-10 px-5 py-24 sm:px-8 lg:grid-cols-[0.7fr_1.3fr]">
            <div>
              <Eyebrow>Use Cases</Eyebrow>
              <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
                Designed around the work life-sciences teams already do.
              </h2>
            </div>
            <div className="grid gap-px bg-white/10 sm:grid-cols-2">
              {useCases.map((item, index) => (
                <div key={item} className="bg-[#08111f] p-5">
                  <p className="text-xs text-[#8ec7c1]">
                    {String(index + 1).padStart(2, "0")}
                  </p>
                  <p className="mt-5 text-lg font-semibold text-[#f8f1e3]">
                    {item}
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
              Review the platform with a real evidence workflow.
            </h2>
            <p className="mt-6 max-w-2xl text-base leading-7 text-[#aebbc5]">
              Start with a scoped disease, therapy, or evidence question. The
              demo can show what is live, what is configured, and what still
              requires validation data.
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
              href="/data-methodology"
              className="border border-white/15 px-5 py-3 text-sm font-medium text-[#f8f1e3] hover:border-[#8ec7c1]/60"
            >
              Read methodology
            </Link>
          </div>
        </section>
      </main>
    </PageShell>
  );
}
