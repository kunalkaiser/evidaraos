"use client";

import { useMemo, useState } from "react";
import { ArrowRight, Mic, MicOff, Search, X } from "lucide-react";
import { useRouter } from "next/navigation";

function getSpeechRecognition() {
  if (typeof window === "undefined") return null;
  if ("SpeechRecognition" in window || "webkitSpeechRecognition" in window) {
    return window.SpeechRecognition || window.webkitSpeechRecognition;
  }
  return null;
}

export function EvidenceQueryIntake() {
  const router = useRouter();
  const [question, setQuestion] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [voiceStatus, setVoiceStatus] = useState<string | null>(null);

  const speechRecognition = useMemo(getSpeechRecognition, []);
  const canSubmit = question.trim().length > 0;

  function startWorkflow() {
    const normalizedQuestion = question.trim();
    const params = new URLSearchParams();
    if (normalizedQuestion) params.set("question", normalizedQuestion);
    params.set("mode", "balanced");
    router.push(`/workspace/modules/precision-slr?${params.toString()}`);
  }

  function toggleVoice() {
    if (!speechRecognition) {
      setVoiceStatus("Voice input is not supported in this browser.");
      return;
    }

    if (isListening) {
      setIsListening(false);
      setVoiceStatus("Voice capture stopped.");
      return;
    }

    const recognition = new speechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onstart = () => {
      setIsListening(true);
      setVoiceStatus("Listening for your evidence question...");
    };

    recognition.onresult = (event) => {
      let transcript = "";

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i];
        transcript += result?.[0]?.transcript ?? "";
      }

      transcript = transcript.trim();

      if (transcript) {
        setQuestion((current) =>
          current.trim() ? `${current.trim()} ${transcript}` : transcript,
        );
        setVoiceStatus("Voice question captured.");
      }
    };

    recognition.onerror = (event) => {
      setVoiceStatus(
        event.error
          ? `Voice input stopped: ${event.error}.`
          : "Voice input stopped.",
      );
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  }

  return (
    <div className="relative overflow-hidden border border-[#8ec7c1]/25 bg-[#071523] shadow-2xl shadow-black/30">
      <div className="absolute inset-0 opacity-35 [background-image:linear-gradient(rgba(142,199,193,0.14)_1px,transparent_1px),linear-gradient(90deg,rgba(142,199,193,0.1)_1px,transparent_1px)] [background-size:34px_34px]" />
      <div className="relative border-b border-white/10 p-5">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-xs font-semibold tracking-[0.22em] text-[#8ec7c1] uppercase">
              Ask EvidaraOS
            </p>
            <h2 className="mt-3 text-2xl font-semibold tracking-normal text-[#f8f1e3]">
              Type or speak an evidence question.
            </h2>
            <p className="mt-2 text-sm leading-6 text-[#aebbc5]">
              Natural-language intake for SLR, HEOR, payer, regulatory, and
              discovery workflows.
            </p>
          </div>
          <span className="shrink-0 border border-[#d7b46a]/35 px-3 py-1 text-xs text-[#e2c57f]">
            NLP intake
          </span>
        </div>
      </div>

      <div className="relative p-5">
        <label
          htmlFor="evidence-question"
          className="text-sm font-medium text-[#f8f1e3]"
        >
          Customer query
        </label>
        <div className="mt-3 border border-white/10 bg-[#08111f] focus-within:border-[#8ec7c1]/70">
          <textarea
            id="evidence-question"
            name="question"
            rows={4}
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            className="min-h-32 w-full resize-none bg-transparent px-4 py-4 text-base leading-7 text-[#f8f1e3] outline-none placeholder:text-[#738390]"
            placeholder="Example: Compare the safety and efficacy evidence for dupilumab in adults with moderate-to-severe atopic dermatitis."
          />
          <div className="flex flex-wrap items-center justify-between gap-3 border-t border-white/10 px-3 py-3">
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={toggleVoice}
                className={`inline-flex h-10 items-center gap-2 border px-3 text-sm ${
                  isListening
                    ? "border-[#d7b46a]/60 bg-[#d7b46a] text-[#071523]"
                    : "border-white/15 text-[#f8f1e3] hover:border-[#8ec7c1]/60"
                }`}
                aria-pressed={isListening}
              >
                {isListening ? (
                  <MicOff className="size-4" />
                ) : (
                  <Mic className="size-4" />
                )}
                {isListening ? "Stop" : "Speak"}
              </button>
              {question && (
                <button
                  type="button"
                  onClick={() => {
                    setQuestion("");
                    setVoiceStatus(null);
                  }}
                  className="inline-flex h-10 items-center gap-2 border border-white/15 px-3 text-sm text-[#c7d1d8] hover:border-[#8ec7c1]/60 hover:text-[#f8f1e3]"
                >
                  <X className="size-4" />
                  Clear
                </button>
              )}
            </div>
            <button
              type="button"
              onClick={startWorkflow}
              disabled={!canSubmit}
              className="inline-flex h-10 items-center gap-2 bg-[#d7b46a] px-4 text-sm font-semibold text-[#071523] hover:bg-[#f0cc80] disabled:cursor-not-allowed disabled:opacity-45"
            >
              <Search className="size-4" />
              Route to Precision SLR
              <ArrowRight className="size-4" />
            </button>
          </div>
        </div>

        {voiceStatus && (
          <p className="mt-3 text-xs text-[#8ec7c1]">{voiceStatus}</p>
        )}

        <div className="mt-5 grid gap-px overflow-hidden border border-white/10 bg-white/10 sm:grid-cols-3">
          {[
            ["Input", "natural language"],
            ["Default module", "Precision SLR"],
            ["Mode", "balanced precision"],
          ].map(([label, value]) => (
            <div key={label} className="bg-[#0b1828] p-4">
              <p className="text-xs tracking-[0.16em] text-[#8395a3] uppercase">
                {label}
              </p>
              <p className="mt-2 text-sm text-[#f8f1e3]">{value}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
