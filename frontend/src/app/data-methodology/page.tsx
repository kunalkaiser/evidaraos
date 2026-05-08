import { Eyebrow, PageShell } from "@/evidaraos/site";

export default function DataMethodologyPage() {
  return (
    <PageShell>
      <main className="mx-auto max-w-7xl px-5 py-20 sm:px-8">
        <Eyebrow>Data and Methodology</Eyebrow>
        <h1 className="mt-5 max-w-5xl text-5xl font-semibold tracking-normal text-[#f8f1e3] md:text-7xl">
          Transparent sources, limitations, and no unsupported claims.
        </h1>
        <div className="mt-12 grid gap-px bg-white/10 md:grid-cols-3">
          {[
            "Public biomedical sources are used where configured, including PubMed, Semantic Scholar, and Crossref in the SLR workflow.",
            "Demo content is fixture-only and cannot support clinical, economic, payer, regulatory, or performance claims.",
            "Human review, validation reports, and audit trails are required before evidence outputs are treated as decision-support artifacts.",
          ].map((item) => (
            <p key={item} className="bg-[#0b1828] p-6 text-base leading-7 text-[#c7d1d8]">
              {item}
            </p>
          ))}
        </div>
      </main>
    </PageShell>
  );
}
