export type OutputFormat = "linkedin" | "twitter" | "executive_summary" | "video_script";

export interface TransformRequest {
  content: string;
  input_type: "text" | "pdf" | "image" | "video" | "url";
  output_formats: OutputFormat[];
  parameters: {
    tone: string;
    audience: string;
    length: string;
    style: string;
    language: string;
    detail_level: string;
    quality_cost_balance: number;
  };
}
