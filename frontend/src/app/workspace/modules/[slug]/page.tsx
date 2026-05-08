import Link from "next/link";
import { notFound } from "next/navigation";

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

export default async function WorkspaceModulePage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const module = modules.find((item) => item.id === routeToModule[slug]);

  if (!module) {
    notFound();
  }

  const Icon = module.icon;

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
