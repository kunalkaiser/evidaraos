import Link from "next/link";

import { PageShell } from "@/evidaraos/site";

export default function ThirdPartyNoticesPage() {
  return (
    <PageShell>
      <main className="mx-auto max-w-4xl px-5 py-24 sm:px-8">
        <p className="text-xs font-semibold tracking-[0.26em] text-[#8ec7c1] uppercase">
          Legal
        </p>
        <h1 className="mt-5 text-4xl font-semibold tracking-normal text-[#f8f1e3] md:text-6xl">
          Third-party notices
        </h1>
        <p className="mt-6 text-base leading-7 text-[#c7d1d8]">
          EvidaraOS includes open-source software and third-party dependencies.
          This page summarizes runtime attribution and directs maintainers to
          the repository notices for complete license details.
        </p>

        <section className="mt-12 border border-white/10 bg-[#0b1828] p-6">
          <h2 className="text-2xl font-semibold text-[#f8f1e3]">
            Open-source agent harness
          </h2>
          <p className="mt-4 text-sm leading-7 text-[#aebbc5]">
            The agent harness used in this repository is based on DeerFlow,
            distributed under the MIT License. Upstream license, copyright,
            author notices, and attribution must remain intact in source
            distributions and substantial copies.
          </p>
          <div className="mt-6 grid gap-px bg-white/10 text-sm md:grid-cols-2">
            {[
              ["Project", "DeerFlow"],
              ["License", "MIT License"],
              [
                "Copyright",
                "Bytedance Ltd. and/or its affiliates; DeerFlow Authors",
              ],
              ["Repository notices", "THIRD_PARTY_NOTICES.md"],
            ].map(([label, value]) => (
              <div key={label} className="bg-[#08111f] p-4">
                <p className="text-xs font-semibold tracking-[0.18em] text-[#8ec7c1] uppercase">
                  {label}
                </p>
                <p className="mt-3 text-[#f8f1e3]">{value}</p>
              </div>
            ))}
          </div>
        </section>

        <Link
          href="/"
          className="mt-10 inline-flex text-sm font-medium text-[#d7b46a] hover:text-[#f0cc80]"
        >
          Back to EvidaraOS
        </Link>
      </main>
    </PageShell>
  );
}
