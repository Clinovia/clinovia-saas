"use client";

import { useState, FormEvent } from "react";
import { AlzheimerDiagnosisInput } from "@/features/alzheimer/types";

type Props = {
  onSubmit: (data: AlzheimerDiagnosisInput) => void;
  loading?: boolean;
};

const raceMap: Record<number, string> = {
  1: "American Indian",
  2: "African American",
  3: "Asian",
  4: "Pacific Islander",
  5: "Caucasian",
  6: "More than one race",
  7: "Unknown",
};

export default function AlzheimerForm({ onSubmit, loading = false }: Props) {
  const [formData, setFormData] = useState<AlzheimerDiagnosisInput>({
    age: 75,
    education_years: 16,
    moca_score: 26,
    adas13_score: 10,
    cdr_sum: 1,
    faq_total: 5,
    gender: "female",
    race: 1,
  });

  const handleChange = <K extends keyof AlzheimerDiagnosisInput>(key: K, value: AlzheimerDiagnosisInput[K]) => {
    setFormData((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const renderRangeInput = (
    label: string,
    key: keyof AlzheimerDiagnosisInput,
    min: number,
    max: number,
    step: number = 1
  ) => (
    <div>
      <label className="block font-medium">
        {label}: {formData[key] as number}
      </label>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={formData[key] as number}
        onChange={(e) => handleChange(key, Number(e.target.value) as any)}
        className="w-full"
      />
    </div>
  );

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {renderRangeInput("Age", "age", 50, 95)}
      {renderRangeInput("Years of Education", "education_years", 6, 20)}
      {renderRangeInput("MoCA Score", "moca_score", 0, 30)}
      {renderRangeInput("ADAS13 Score", "adas13_score", 0, 70, 0.5)}
      {renderRangeInput("CDR Sum", "cdr_sum", 0, 18, 0.5)}
      {renderRangeInput("FAQ Total", "faq_total", 0, 30)}

      <div>
        <label className="block font-medium">Gender</label>
        <select
          value={formData.gender}
          onChange={(e) => handleChange("gender", e.target.value as "female" | "male")}
          className="w-full border rounded p-1"
        >
          <option value="female">Female</option>
          <option value="male">Male</option>
        </select>
      </div>

      <div>
        <label className="block font-medium">Race</label>
        <select
          value={formData.race}
          onChange={(e) => handleChange("race", Number(e.target.value))}
          className="w-full border rounded p-1"
        >
          {Object.entries(raceMap).map(([key, label]) => (
            <option key={key} value={key}>
              {label}
            </option>
          ))}
        </select>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        {loading ? "Predicting..." : "🔮 Predict"}
      </button>
    </form>
  );
}
