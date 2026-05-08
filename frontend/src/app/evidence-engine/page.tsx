import {
  EvidenceStackDiagram,
  Eyebrow,
  MethodologyRail,
  PageShell,
  SystemFlowDiagram,
  WorkflowStrip,
} from "@/evidaraos/site";

export default function EvidenceEnginePage() {
  return (
    <PageShell>
      <main className="mx-auto max-w-7xl px-5 py-20 sm:px-8">
        <Eyebrow>Evidence Engine</Eyebrow>
        <h1 className="mt-5 max-w-5xl text-5xl font-semibold tracking-normal text-[#f8f1e3] md:text-7xl">
          Retrieval, evidence maps, provenance, and governed artifacts.
        </h1>
        <p className="mt-6 max-w-3xl text-lg leading-8 text-[#c7d1d8]">
          The EvidenceOS engine organizes records, claims, parameters, findings,
          and graph paths into structured artifacts that can be reviewed,
          validated, and audited.
        </p>
        <div className="mt-14">
          <WorkflowStrip />
        </div>
        <section className="mt-20">
          <div className="mb-8">
            <Eyebrow>Evidence Stack</Eyebrow>
          </div>
          <EvidenceStackDiagram />
        </section>
        <section className="mt-20">
          <div className="mb-8">
            <Eyebrow>System Flow</Eyebrow>
          </div>
          <SystemFlowDiagram />
        </section>
        <section className="mt-20">
          <div className="mb-8">
            <Eyebrow>Methodology</Eyebrow>
          </div>
          <MethodologyRail />
        </section>
      </main>
    </PageShell>
  );
}
