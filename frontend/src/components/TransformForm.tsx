import { useState } from "react";
import { api } from "../api/client";
import type { OutputFormat, TransformRequest } from "../types";

const defaultFormats: OutputFormat[] = ["linkedin", "twitter", "executive_summary", "video_script"];

export function TransformForm() {
  const [content, setContent] = useState("");
  const [result, setResult] = useState<unknown>(null);
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    setLoading(true);
    const payload: TransformRequest = {
      content,
      input_type: "text",
      output_formats: defaultFormats,
      parameters: {
        tone: "Professional",
        audience: "General Public",
        length: "Medium",
        style: "Conversational",
        language: "English",
        detail_level: "Overview",
        quality_cost_balance: 0.75
      }
    };
    try {
      const { data } = await api.post("/transform", payload);
      setResult(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section>
      <h2>Morphine Dashboard</h2>
      <textarea
        rows={12}
        placeholder="Paste text, URL, or extracted content..."
        value={content}
        onChange={(e) => setContent(e.target.value)}
        style={{ width: "100%" }}
      />
      <button onClick={submit} disabled={loading || !content.trim()}>
        {loading ? "Transforming..." : "Run Transformation"}
      </button>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </section>
  );
}
