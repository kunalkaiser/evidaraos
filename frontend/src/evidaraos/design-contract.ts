export const designContract = {
  version: "0.1.0",
  brand: {
    wordmark: "EvidaraOS",
    monogram: "EO",
    positioning: "Precision evidence operating system for life sciences",
  },
  colors: {
    canvasDeepest: "#070d17",
    canvasBase: "#08111f",
    canvasRaised: "#071523",
    canvasPanel: "#0b1828",
    textPrimary: "#f8f1e3",
    textSecondary: "#c7d1d8",
    textMuted: "#aebbc5",
    clinical: "#8ec7c1",
    evidenceGold: "#d7b46a",
  },
  rules: [
    "No fake metrics, fake validation, or fake live data.",
    "Show workflow architecture and governance whenever possible.",
    "Separate source evidence, AI interpretation, human decision, and final decision.",
    "Use restrained enterprise life-sciences visual language.",
  ],
} as const;
