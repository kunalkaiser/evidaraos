import { AuthProvider } from "@/core/auth/AuthProvider";
import type { User } from "@/core/auth/types";

import { WorkspaceContent } from "./workspace-content";

export const dynamic = "force-dynamic";

const EVIDARAOS_WORKSPACE_USER: User = {
  id: "evidaraos-workspace",
  email: "workspace@evidaraos.local",
  system_role: "admin",
  needs_setup: false,
};

export default async function WorkspaceLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <AuthProvider initialUser={EVIDARAOS_WORKSPACE_USER}>
      <WorkspaceContent>{children}</WorkspaceContent>
    </AuthProvider>
  );
}
