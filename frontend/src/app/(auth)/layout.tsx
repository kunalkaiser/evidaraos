import { redirect } from "next/navigation";
import { type ReactNode } from "react";

export const dynamic = "force-dynamic";

export default async function AuthLayout({
  children: _children,
}: {
  children: ReactNode;
}) {
  redirect("/workspace/modules");
}
