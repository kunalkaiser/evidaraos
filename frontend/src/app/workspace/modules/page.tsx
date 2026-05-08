import Link from "next/link";

import { demoProjects, modules } from "@/evidaraos/product-data";

export default function WorkspaceModulesPage() {
  return (
    <main className="min-h-screen bg-[#08111f] p-6 text-[#f8f1e3]">
      <div className="mx-auto max-w-7xl">
        <div className="flex flex-col justify-between gap-5 border-b border-white/10 pb-8 md:flex-row md:items-end">
          <div>
            <p className="text-xs font-semibold tracking-[0.26em] text-[#8ec7c1] uppercase">
              EvidaraOS Workspace
            </p>
            <h1 className="mt-4 text-4xl font-semibold tracking-normal md:text-6xl">
              Evidence modules
            </h1>
            <p className="mt-4 max-w-3xl text-sm leading-6 text-[#aebbc5]">
              Connected skills and configured workflows for precision evidence
              generation. Demo projects are fixture-only and are not validation
              evidence.
            </p>
          </div>
          <Link
            href="/workspace/chats/new"
            className="border border-[#8ec7c1]/35 px-4 py-2 text-sm text-[#f8f1e3] hover:border-[#d7b46a]/70"
          >
            Open runtime chat
          </Link>
        </div>

        <section className="mt-10 grid gap-4 xl:grid-cols-2">
          {modules.map((module) => {
            const Icon = module.icon;
            return (
              <Link
                href={module.workspaceRoute}
                key={module.id}
                className="border border-white/10 bg-[#0b1828] p-6 hover:border-[#8ec7c1]/45"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <Icon className="mb-6 size-6 text-[#d7b46a]" />
                    <h2 className="text-2xl font-semibold text-[#f8f1e3]">
                      {module.displayName}
                    </h2>
                    <p className="mt-3 text-sm leading-6 text-[#aebbc5]">
                      {module.oneLiner}
                    </p>
                  </div>
                  <span className="shrink-0 border border-[#8ec7c1]/30 px-3 py-1 text-xs text-[#8ec7c1]">
                    {module.status}
                  </span>
                </div>
                <div className="mt-6 grid gap-2 text-xs text-[#c7d1d8] md:grid-cols-2">
                  {module.artifacts.slice(0, 4).map((artifact) => (
                    <span
                      key={artifact}
                      className="border border-white/10 px-3 py-2"
                    >
                      {artifact}
                    </span>
                  ))}
                </div>
              </Link>
            );
          })}
        </section>

        <section className="mt-14">
          <div className="mb-5 flex items-end justify-between gap-4">
            <div>
              <p className="text-xs font-semibold tracking-[0.26em] text-[#8ec7c1] uppercase">
                Demo Projects
              </p>
              <h2 className="mt-3 text-3xl font-semibold">
                Fixture-only demos
              </h2>
            </div>
            <p className="max-w-md text-sm leading-6 text-[#aebbc5]">
              Use these to review workflow structure and UI states only.
            </p>
          </div>
          <div className="grid gap-4 lg:grid-cols-3">
            {demoProjects.map((project) => {
              const module = modules.find(
                (item) => item.id === project.moduleId,
              );
              return (
                <div
                  key={project.id}
                  className="border border-white/10 bg-[#0b1828] p-5"
                >
                  <p className="text-sm font-semibold text-[#f8f1e3]">
                    {project.title}
                  </p>
                  <p className="mt-3 text-xs tracking-[0.18em] text-[#8ec7c1] uppercase">
                    {module?.shortName}
                  </p>
                  <p className="mt-4 text-sm text-[#aebbc5]">
                    {project.artifactCount} artifacts. Fixture-only, not
                    validation evidence.
                  </p>
                </div>
              );
            })}
          </div>
        </section>
      </div>
    </main>
  );
}
