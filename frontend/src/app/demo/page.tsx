import Link from "next/link";

import { DemoProjectCards, Eyebrow, PageShell } from "@/evidaraos/site";

export default function DemoPage() {
  return (
    <PageShell>
      <main className="mx-auto max-w-7xl px-5 py-20 sm:px-8">
        <Eyebrow>Demo</Eyebrow>
        <h1 className="mt-5 max-w-5xl text-5xl font-semibold tracking-normal text-[#f8f1e3] md:text-7xl">
          See governed evidence workflows for your team.
        </h1>
        <p className="mt-6 max-w-3xl text-lg leading-8 text-[#c7d1d8]">
          The initial demo shows configured workflows and fixture-labeled
          examples only. Live execution and validated benchmark claims should be
          added only after backend integration and human-labeled validation.
        </p>
        <div className="mt-9">
          <Link
            href="/workspace/modules"
            className="bg-[#d7b46a] px-5 py-3 text-sm font-medium text-[#08111f] hover:bg-[#f0cc80]"
          >
            Open workspace modules
          </Link>
        </div>
        <div className="mt-14">
          <DemoProjectCards />
        </div>
      </main>
    </PageShell>
  );
}
