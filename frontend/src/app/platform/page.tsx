import {
  ArchitectureVisual,
  EnterpriseProofSection,
  EvidencePipelinePanel,
  EvidenceStackDiagram,
  Eyebrow,
  MethodologyRail,
  ModuleMatrix,
  PageShell,
  SystemFlowDiagram,
  WorkflowStrip,
} from "@/evidaraos/site";

export default function PlatformPage() {
  return (
    <PageShell>
      <main>
        <section className="mx-auto max-w-7xl px-5 py-20 sm:px-8">
          <Eyebrow>Platform</Eyebrow>
          <h1 className="mt-5 max-w-5xl text-5xl font-semibold leading-[0.98] tracking-normal text-[#f8f1e3] md:text-7xl">
            Evidence workflows with traceability built in.
          </h1>
          <p className="mt-6 max-w-3xl text-lg leading-8 text-[#c7d1d8]">
            EvidaraOS connects question framing, biomedical retrieval, evidence
            mapping, extraction, human review, validation, reporting, and audit
            trails across life-sciences evidence workflows.
          </p>
        </section>
        <section className="mx-auto max-w-7xl px-5 sm:px-8">
          <ArchitectureVisual />
        </section>
        <EnterpriseProofSection />
        <section className="mx-auto max-w-7xl px-5 py-20 sm:px-8">
          <div className="mb-8 max-w-3xl">
            <Eyebrow>Evidence Stack</Eyebrow>
            <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
              The platform is layered around traceability.
            </h2>
          </div>
          <EvidenceStackDiagram />
        </section>
        <section className="mx-auto max-w-7xl px-5 py-20 sm:px-8">
          <div className="mb-8 max-w-3xl">
            <Eyebrow>Lifecycle</Eyebrow>
            <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
              One governed operating model across evidence teams.
            </h2>
          </div>
          <WorkflowStrip />
        </section>
        <section className="mx-auto max-w-7xl px-5 py-20 sm:px-8">
          <div className="mb-8 max-w-3xl">
            <Eyebrow>Operating Model</Eyebrow>
            <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
              Inputs, governed processing, controlled outputs.
            </h2>
          </div>
          <EvidencePipelinePanel />
        </section>
        <section className="mx-auto max-w-7xl px-5 py-20 sm:px-8">
          <div className="mb-8 max-w-3xl">
            <Eyebrow>System Flow</Eyebrow>
            <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
              How evidence moves through the operating system.
            </h2>
          </div>
          <SystemFlowDiagram />
        </section>
        <section className="mx-auto max-w-7xl px-5 py-20 sm:px-8">
          <div className="mb-8">
            <Eyebrow>Methodology</Eyebrow>
          </div>
          <MethodologyRail />
        </section>
        <section className="mx-auto max-w-7xl px-5 py-20 sm:px-8">
          <div className="mb-6">
            <Eyebrow>Modules</Eyebrow>
          </div>
          <ModuleMatrix />
        </section>
      </main>
    </PageShell>
  );
}
