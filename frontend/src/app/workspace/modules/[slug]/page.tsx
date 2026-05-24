import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowRight, ClipboardCheck, PlayCircle } from "lucide-react";

import { modules } from "@/evidaraos/product-data";

export function generateStaticParams() {
  return [
    { slug: "precision-slr" },
    { slug: "heor" },
    { slug: "payer-value-dossier" },
    { slug: "regulatory-briefing" },
    { slug: "drug-repurposing" },
  ];
}

const routeToModule: Record<string, string> = {
  "precision-slr": "precision_literature_review",
  heor: "heor_evidence_modeler",
  "payer-value-dossier": "payer_value_dossier",
  "regulatory-briefing": "regulatory_evidence_briefing",
  "drug-repurposing": "drug_repurposing_explorer",
};

function firstParam(value: string | string[] | undefined) {
  return Array.isArray(value) ? value[0] : value;
}

function buildPrecisionSlrPrompt(question: string, mode: string) {
  return [
    "Run the EvidenceOS Precision SLR workflow for this review question:",
    "",
    question,
    "",
    `Precision mode: ${mode}`,
    "",
    "Start by framing the review as PICO or PECO, then generate PubMed, Semantic Scholar, and Crossref search strategies. Next outline retrieval, deduplication, relevance scoring, screening prioritization, evidence extraction, PRISMA-style counts, human review, validation reporting, and audit trail steps.",
    "",
    "Do not claim records were retrieved, screened, or validated until the appropriate tools or scripts have actually been run. Label any fixture-only examples clearly.",
  ].join("\n");
}

export default async function WorkspaceModulePage({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string }>;
  searchParams?: Promise<Record<string, string | string[] | undefined>>;
}) {
  const { slug } = await params;
  const resolvedSearchParams = searchParams ? await searchParams : {};
  const module = modules.find((item) => item.id === routeToModule[slug]);

  if (!module) {
    notFound();
  }

  const Icon = module.icon;
  const receivedQuestion =
    firstParam(resolvedSearchParams.question)?.trim() ?? "";
  const precisionMode = firstParam(resolvedSearchParams.mode) ?? "balanced";
  const isPrecisionSlr = slug === "precision-slr";
  const runtimePrompt =
    isPrecisionSlr && receivedQuestion
      ? buildPrecisionSlrPrompt(receivedQuestion, precisionMode)
      : "";
  const runtimeChatHref = runtimePrompt
    ? `/workspace/chats/new?text=${encodeURIComponent(runtimePrompt)}`
    : "/workspace/chats/new";
  const launchSteps = [
    "Frame PICO/PECO protocol",
    "Generate Boolean search strategy",
    "Prepare PubMed, Semantic Scholar, and Crossref retrieval",
    "Deduplicate by DOI, PMID, and normalized title",
    "Score precision and prioritize screening",
    "Create PRISMA, validation, and audit artifacts",
  ];

  return (
    <main className="min-h-screen bg-[#08111f] p-6 text-[#f8f1e3]">
      <div className="mx-auto max-w-6xl">
        <Link
          href="/workspace/modules"
          className="text-sm text-[#8ec7c1] hover:text-[#d7b46a]"
        >
          Back to modules
        </Link>
        <section className="mt-8 grid gap-8 border-b border-white/10 pb-10 lg:grid-cols-[0.8fr_1.2fr]">
          <div>
            <Icon className="mb-8 size-8 text-[#d7b46a]" />
            <h1 className="text-4xl font-semibold tracking-normal md:text-6xl">
              {module.displayName}
            </h1>
            <p className="mt-5 text-base leading-7 text-[#aebbc5]">
              {module.oneLiner}
            </p>
            <div className="mt-6 flex flex-wrap gap-2">
              <span className="border border-[#8ec7c1]/30 px-3 py-1 text-xs text-[#8ec7c1]">
                {module.status}
              </span>
              <span className="border border-[#d7b46a]/35 px-3 py-1 text-xs text-[#e2c57f]">
                {module.mappedSkill}
              </span>
            </div>
          </div>
          <div className="grid gap-px bg-white/10 md:grid-cols-2">
            {module.workflow.map((step, index) => (
              <div key={step} className="bg-[#0b1828] p-5">
                <p className="text-xs text-[#8ec7c1]">
                  {String(index + 1).padStart(2, "0")}
                </p>
                <p className="mt-4 text-sm font-medium">{step}</p>
              </div>
            ))}
          </div>
        </section>
        {isPrecisionSlr && receivedQuestion && (
          <section className="mt-8 border border-[#8ec7c1]/25 bg-[#0b1828] p-6 shadow-[0_24px_80px_rgba(0,0,0,0.24)]">
            <div className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
              <div className="max-w-3xl">
                <div className="flex items-center gap-3 text-sm font-medium text-[#8ec7c1]">
                  <ClipboardCheck className="size-4" />
                  Question received
                </div>
                <p className="mt-4 text-xl leading-8 text-[#f8f1e3]">
                  {receivedQuestion}
                </p>
                <div className="mt-5 flex flex-wrap gap-2 text-xs">
                  <span className="border border-[#d7b46a]/35 px-3 py-1 text-[#e2c57f]">
                    Mode: {precisionMode}
                  </span>
                  <span className="border border-[#8ec7c1]/30 px-3 py-1 text-[#8ec7c1]">
                    Configured workflow
                  </span>
                  <span className="border border-white/15 px-3 py-1 text-[#aebbc5]">
                    Pending live module API execution
                  </span>
                </div>
              </div>
              <Link
                href={runtimeChatHref}
                className="inline-flex shrink-0 items-center justify-center gap-2 bg-[#d7b46a] px-5 py-3 text-sm font-semibold text-[#08111f] transition hover:bg-[#e2c57f]"
              >
                <PlayCircle className="size-4" />
                Start in runtime chat
                <ArrowRight className="size-4" />
              </Link>
            </div>
            <div className="mt-7 grid gap-px bg-white/10 md:grid-cols-3">
              {launchSteps.map((step, index) => (
                <div key={step} className="bg-[#08111f] p-4">
                  <p className="text-xs text-[#8ec7c1]">
                    {String(index + 1).padStart(2, "0")}
                  </p>
                  <p className="mt-3 text-sm text-[#dce5e8]">{step}</p>
                </div>
              ))}
            </div>
            <p className="mt-5 max-w-4xl text-sm leading-6 text-[#aebbc5]">
              This page has captured the request and prepared the governed SLR
              workflow. It is not displaying fake search results; automated
              retrieval and screening should be run through the runtime or the
              next branded module API integration.
            </p>
          </section>
        )}
        <section className="grid gap-8 py-10 lg:grid-cols-2">
          <div>
            <h2 className="text-2xl font-semibold">Artifacts</h2>
            <div className="mt-5 grid gap-px bg-white/10">
              {module.artifacts.map((artifact) => (
                <div
                  key={artifact}
                  className="bg-[#0b1828] p-4 text-sm text-[#c7d1d8]"
                >
                  {artifact}
                </div>
              ))}
            </div>
          </div>
          <div>
            <h2 className="text-2xl font-semibold">Execution status</h2>
            <div className="mt-5 border border-white/10 bg-[#0b1828] p-5 text-sm leading-6 text-[#c7d1d8]">
              Connected skill: workflow scripts and governance artifacts exist
              in skills/public. Live backend execution through a branded module
              API is still the next integration step.
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
