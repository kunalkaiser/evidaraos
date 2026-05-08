import { ShieldCheck } from "lucide-react";

import { Eyebrow, PageShell, WorkflowStrip } from "@/evidaraos/site";
import { governanceModule } from "@/evidaraos/product-data";

export default function GovernancePage() {
  return (
    <PageShell>
      <main>
        <section className="mx-auto max-w-7xl px-5 py-20 sm:px-8">
          <Eyebrow>Governance</Eyebrow>
          <h1 className="mt-5 max-w-5xl text-5xl font-semibold tracking-normal text-[#f8f1e3] md:text-7xl">
            Validation-ready controls for AI-assisted evidence work.
          </h1>
          <p className="mt-6 max-w-3xl text-lg leading-8 text-[#c7d1d8]">
            Human review, adjudication, validation reports, project manifests,
            audit trails, and fixture-only warnings are shared controls across
            EvidenceOS workflows.
          </p>
        </section>
        <section className="mx-auto grid max-w-7xl gap-10 px-5 py-10 sm:px-8 lg:grid-cols-[0.85fr_1.15fr]">
          <div className="border-l border-[#d7b46a] pl-6">
            <h2 className="text-3xl font-semibold text-[#f8f1e3]">
              Human oversight is a workflow state.
            </h2>
            <p className="mt-4 text-base leading-7 text-[#aebbc5]">
              EvidenceOS should never present fixture smoke tests as real
              validation evidence or treat AI outputs as final scientific,
              payer, regulatory, or development decisions.
            </p>
          </div>
          <div className="grid gap-px bg-white/10 md:grid-cols-2">
            {governanceModule.controls.map((control) => (
              <div key={control} className="bg-[#0b1828] p-6">
                <ShieldCheck className="mb-5 size-5 text-[#d7b46a]" />
                <p className="text-sm font-medium text-[#f8f1e3]">{control}</p>
              </div>
            ))}
          </div>
        </section>
        <section className="mx-auto max-w-7xl px-5 py-20 sm:px-8">
          <div className="mb-8">
            <Eyebrow>Governed Lifecycle</Eyebrow>
          </div>
          <WorkflowStrip />
        </section>
      </main>
    </PageShell>
  );
}
