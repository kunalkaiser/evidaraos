import Link from "next/link";

import {
  DemoProjectCards,
  EnterpriseCta,
  EvidenceArtifactMosaic,
  EvidencePipelinePanel,
  EvidenceStackDiagram,
  Eyebrow,
  GovernancePanel,
  HeroEvidenceConsole,
  ModuleMatrix,
  PageShell,
  ResourcesBand,
  StatRow,
  SystemFlowDiagram,
  TheWorkBand,
  WorkflowStrip,
} from "@/evidaraos/site";

export default function HomePage() {
  return (
    <PageShell>
      <main>
        <section className="relative overflow-hidden border-b border-white/10">
          <div className="absolute inset-0 opacity-25 [background-image:linear-gradient(rgba(142,199,193,0.12)_1px,transparent_1px),linear-gradient(90deg,rgba(142,199,193,0.12)_1px,transparent_1px)] [background-size:52px_52px]" />
          <div className="relative mx-auto grid max-w-7xl gap-12 px-5 py-20 sm:px-8 lg:grid-cols-[0.92fr_1.08fr] lg:py-28">
            <div className="flex flex-col justify-center">
              <Eyebrow>Precision Evidence Operating System</Eyebrow>
              <h1 className="mt-5 max-w-4xl text-5xl font-semibold leading-[0.95] tracking-normal text-[#f8f1e3] md:text-7xl">
                Precision evidence generation for life sciences.
              </h1>
              <p className="mt-6 max-w-2xl text-lg leading-8 text-[#c7d1d8]">
                EvidaraOS helps evidence, HEOR, regulatory, and market access
                teams turn biomedical literature, clinical evidence, and
                real-world data into traceable, validation-ready evidence
                workflows.
              </p>
              <div className="mt-9 flex flex-wrap gap-3">
                <Link
                  href="/demo"
                  className="bg-[#d7b46a] px-5 py-3 text-sm font-medium text-[#08111f] hover:bg-[#f0cc80]"
                >
                  Request a demo
                </Link>
                <Link
                  href="/platform"
                  className="border border-white/15 px-5 py-3 text-sm font-medium text-[#f8f1e3] hover:border-[#8ec7c1]/60"
                >
                  Explore platform
                </Link>
              </div>
              <div className="mt-10 grid gap-4 border-l border-[#d7b46a] pl-5 text-sm leading-6 text-[#aebbc5]">
                <p>
                  Built for precision SLR, HEOR, payer evidence, regulatory
                  briefing, repurposing hypotheses, and audit-ready governance.
                </p>
                <p>
                  Designed for traceable, validation-ready workflows with
                  human review, provenance, and audit-ready outputs.
                </p>
              </div>
            </div>
            <HeroEvidenceConsole />
          </div>
          <StatRow />
        </section>

        <section className="mx-auto max-w-7xl px-5 py-24 sm:px-8">
          <div className="mb-8 grid gap-8 lg:grid-cols-[0.78fr_1.22fr]">
            <div>
              <Eyebrow>Evidence Artifacts</Eyebrow>
              <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
                A product surface built around what teams actually review.
              </h2>
            </div>
            <p className="max-w-3xl text-base leading-7 text-[#aebbc5] lg:pt-10">
              The homepage should show more than a promise. EvidaraOS is
              organized around concrete evidence artifacts: screening queues,
              evidence maps, model-input tables, validation reports, and audit
              records.
            </p>
          </div>
          <EvidenceArtifactMosaic />
        </section>

        <TheWorkBand />

        <section className="mx-auto max-w-7xl px-5 py-24 sm:px-8">
          <div className="mb-8 grid gap-8 lg:grid-cols-[0.75fr_1.25fr]">
            <div>
              <Eyebrow>System Architecture</Eyebrow>
              <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
                A layered operating system for evidence work.
              </h2>
            </div>
            <p className="max-w-3xl text-base leading-7 text-[#aebbc5] lg:pt-10">
              EvidenceOS separates source collection, normalization, agent
              workflows, human oversight, validation, and audit. That structure
              is what keeps outputs traceable instead of becoming generic AI
              summaries.
            </p>
          </div>
          <EvidenceStackDiagram />
        </section>

        <section className="mx-auto max-w-7xl px-5 py-24 sm:px-8">
          <div className="mb-8 max-w-3xl">
            <Eyebrow>Platform Modules</Eyebrow>
            <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
              A governed evidence intelligence layer.
            </h2>
            <p className="mt-5 text-base leading-7 text-[#aebbc5]">
              Each module shares the same operating model: protocol-bound
              evidence work, traceable artifacts, human review, validation
              reports, and audit trails.
            </p>
          </div>
          <ModuleMatrix />
        </section>

        <section className="border-y border-white/10 bg-[#0b1828]">
          <div className="mx-auto max-w-7xl px-5 py-24 sm:px-8">
            <div className="grid gap-10 lg:grid-cols-[0.72fr_1.28fr]">
              <div>
                <Eyebrow>Problem</Eyebrow>
                <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
                  Evidence teams are drowning in inputs but judged on
                  traceability.
                </h2>
              </div>
              <div className="grid gap-px bg-white/10">
                {[
                  "Manual literature review creates large screening burden and inconsistent exclusion rationale.",
                  "Clinical, economic, payer, and regulatory evidence often live in disconnected artifacts.",
                  "AI-assisted outputs are hard to trust without human review, validation, and audit trails.",
                ].map((point) => (
                  <p
                    key={point}
                    className="bg-[#08111f] p-7 text-lg leading-7 text-[#c7d1d8]"
                  >
                    {point}
                  </p>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-5 py-24 sm:px-8">
          <div className="mb-8 max-w-3xl">
            <Eyebrow>Evidence Engine</Eyebrow>
            <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
              A controlled path from evidence inputs to governed outputs.
            </h2>
          </div>
          <EvidencePipelinePanel />
        </section>

        <section className="mx-auto max-w-7xl px-5 py-24 sm:px-8">
          <div className="mb-8 max-w-3xl">
            <Eyebrow>Technical Flow</Eyebrow>
            <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
              From evidence inputs to governed outputs.
            </h2>
          </div>
          <SystemFlowDiagram />
        </section>

        <section className="mx-auto max-w-7xl px-5 py-24 sm:px-8">
          <div className="mb-8 max-w-3xl">
            <Eyebrow>How It Works</Eyebrow>
            <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
              From question to audit-ready evidence package.
            </h2>
          </div>
          <WorkflowStrip />
        </section>

        <GovernancePanel />

        <section className="mx-auto max-w-7xl px-5 py-24 sm:px-8">
          <div className="mb-8 flex flex-col justify-between gap-5 md:flex-row md:items-end">
            <div>
              <Eyebrow>Demo Projects</Eyebrow>
              <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
                Fixture-labeled workflows for review.
              </h2>
            </div>
            <p className="max-w-md text-sm leading-6 text-[#aebbc5]">
              Demo projects show workflow structure only. They are not
              validation evidence, clinical conclusions, economic results, payer
              predictions, or regulatory claims.
            </p>
          </div>
          <DemoProjectCards />
        </section>

        <ResourcesBand />

        <EnterpriseCta />
      </main>
    </PageShell>
  );
}
