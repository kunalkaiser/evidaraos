import { notFound } from "next/navigation";

import { modules } from "@/evidaraos/product-data";
import {
  EvidencePipelinePanel,
  Eyebrow,
  GuardrailList,
  PageShell,
  StatusPill,
  TextLink,
  WorkflowStrip,
} from "@/evidaraos/site";

export function generateStaticParams() {
  return modules.map((module) => ({ slug: module.slug }));
}

export default async function SolutionPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const module = modules.find((item) => item.slug === slug);

  if (!module) {
    notFound();
  }

  const Icon = module.icon;

  return (
    <PageShell>
      <main>
        <section className="mx-auto grid max-w-7xl gap-10 px-5 py-20 sm:px-8 lg:grid-cols-[0.9fr_1.1fr]">
          <div>
            <Eyebrow>{module.shortName}</Eyebrow>
            <h1 className="mt-5 max-w-5xl text-5xl font-semibold tracking-normal text-[#f8f1e3] md:text-7xl">
              {module.headline}
            </h1>
            <p className="mt-6 max-w-3xl text-lg leading-8 text-[#c7d1d8]">
              {module.oneLiner}
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <StatusPill>{module.status}</StatusPill>
              <StatusPill>mapped skill: {module.mappedSkill}</StatusPill>
            </div>
          </div>
          <div className="border border-white/10 bg-[#0b1828] p-6">
            <Icon className="mb-8 size-8 text-[#d7b46a]" />
            <p className="text-sm font-semibold tracking-[0.18em] text-[#8ec7c1] uppercase">
              Primary users
            </p>
            <div className="mt-5 grid gap-px bg-white/10">
              {module.users.map((user) => (
                <div
                  key={user}
                  className="bg-[#08111f] px-4 py-3 text-sm text-[#f8f1e3]"
                >
                  {user}
                </div>
              ))}
            </div>
            <div className="mt-8">
              <TextLink href={module.workspaceRoute}>
                Open workspace module
              </TextLink>
            </div>
          </div>
        </section>

        <section className="border-y border-white/10 bg-[#0b1828]">
          <div className="mx-auto grid max-w-7xl gap-px bg-white/10 px-5 py-px sm:px-8 lg:grid-cols-3">
            {[
              ["Configured workflow", module.status],
              ["Workflow module", module.shortName],
              ["Demo state", "fixture-labeled"],
            ].map(([label, value]) => (
              <div key={label} className="bg-[#08111f] p-6">
                <p className="text-xs font-semibold tracking-[0.18em] text-[#8ec7c1] uppercase">
                  {label}
                </p>
                <p className="mt-4 text-2xl font-semibold text-[#f8f1e3]">
                  {value}
                </p>
              </div>
            ))}
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-5 py-20 sm:px-8">
          <div className="mb-8">
            <Eyebrow>Workflow</Eyebrow>
          </div>
          <div className="grid gap-px bg-white/10 md:grid-cols-2 lg:grid-cols-4">
            {module.workflow.map((step, index) => (
              <div key={step} className="bg-[#0b1828] p-5">
                <p className="text-xs text-[#8ec7c1]">
                  {String(index + 1).padStart(2, "0")}
                </p>
                <p className="mt-5 text-sm font-medium text-[#f8f1e3]">
                  {step}
                </p>
              </div>
            ))}
          </div>
        </section>

        <section className="mx-auto grid max-w-7xl gap-10 px-5 py-20 sm:px-8 lg:grid-cols-2">
          <div>
            <Eyebrow>Artifacts</Eyebrow>
            <div className="mt-6 grid gap-px bg-white/10">
              {module.artifacts.map((artifact) => (
                <p
                  key={artifact}
                  className="bg-[#0b1828] p-4 text-sm text-[#c7d1d8]"
                >
                  {artifact}
                </p>
              ))}
            </div>
          </div>
          <div>
            <Eyebrow>Guardrails</Eyebrow>
            <div className="mt-6 border border-white/10 bg-[#0b1828] p-6">
              <GuardrailList items={module.guardrails} />
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-5 py-20 sm:px-8">
          <div className="mb-8 max-w-3xl">
            <Eyebrow>Evidence Engine</Eyebrow>
            <h2 className="mt-4 text-3xl font-semibold tracking-normal text-[#f8f1e3] md:text-5xl">
              Structured evidence flow for this module.
            </h2>
          </div>
          <EvidencePipelinePanel />
        </section>

        <section className="mx-auto max-w-7xl px-5 py-20 sm:px-8">
          <div className="mb-8">
            <Eyebrow>Shared Lifecycle</Eyebrow>
          </div>
          <WorkflowStrip />
        </section>
      </main>
    </PageShell>
  );
}
