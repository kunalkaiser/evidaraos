"use client";

import Link from "next/link";

import { AuroraText } from "@/components/ui/aurora-text";
import { Button } from "@/components/ui/button";

import { Section } from "../section";

export function CommunitySection() {
  return (
    <Section
      title={
        <AuroraText colors={["#60A5FA", "#A5FA60", "#A560FA"]}>
          Open-source Runtime
        </AuroraText>
      }
      subtitle="EvidaraOS preserves runtime attribution and third-party notices while focusing the product experience on life-sciences evidence workflows."
    >
      <div className="flex justify-center">
        <Button className="text-xl" size="lg" asChild>
          <Link href="/legal/third-party">
            View Notices
          </Link>
        </Button>
      </div>
    </Section>
  );
}
