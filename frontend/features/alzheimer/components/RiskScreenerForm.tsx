"use client";

import { useState, FormEvent } from "react";
import { AlzheimerRiskScreenerInput } from "@/features/alzheimer/types";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

type Props = {
  onSubmit: (data: AlzheimerRiskScreenerInput) => void;
  loading?: boolean;
};

export default function AlzheimerRiskForm({ onSubmit, loading = false }: Props) {
  const [formData, setFormData] = useState<AlzheimerRiskScreenerInput>({
    age: 65,
    gender: "female",
    education_years: 16,
    apoe4_status: false,
    memory_score: 26,
    hippocampal_volume: 3500,
  });

  const handleChange = <K extends keyof AlzheimerRiskScreenerInput>(
    key: K,
    value: AlzheimerRiskScreenerInput[K]
  ) => {
    setFormData((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Card className="p-6 rounded-2xl shadow-md">
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          
          {/* Age */}
          <div>
            <label htmlFor="age" className="block font-medium">
              Age: {formData.age}
            </label>
            <input
              id="age"
              type="range"
              min={40}
              max={90}
              value={formData.age}
              onChange={(e) => handleChange("age", Number(e.target.value))}
              className="w-full"
            />
          </div>

          {/* Gender */}
          <div>
            <label htmlFor="gender" className="block font-medium">
              Gender
            </label>
            <select
              id="gender"
              value={formData.gender}
              onChange={(e) =>
                handleChange("gender", e.target.value as "male" | "female")
              }
              className="w-full border rounded p-2"
            >
              <option value="female">Female</option>
              <option value="male">Male</option>
            </select>
          </div>

          {/* Education Years */}
          <div>
            <label htmlFor="education_years" className="block font-medium">
              Years of Education: {formData.education_years}
            </label>
            <input
              id="education_years"
              type="range"
              min={0}
              max={30}
              step={1}
              value={formData.education_years}
              onChange={(e) =>
                handleChange("education_years", Number(e.target.value))
              }
              className="w-full"
            />
          </div>

          {/* APOE4 Status */}
          <div>
            <label htmlFor="apoe4_status" className="block font-medium">
              APOE4 Status: {formData.apoe4_status ? "Positive" : "Negative"}
            </label>
            <input
              id="apoe4_status"
              type="checkbox"
              checked={formData.apoe4_status}
              onChange={(e) => handleChange("apoe4_status", e.target.checked)}
              className="mt-1"
            />
          </div>

          {/* Memory Score */}
          <div>
            <label htmlFor="memory_score" className="block font-medium">
              Memory Score: {formData.memory_score}
            </label>
            <input
              id="memory_score"
              type="range"
              min={0}
              max={30}
              step={0.5}
              value={formData.memory_score}
              onChange={(e) =>
                handleChange("memory_score", Number(e.target.value))
              }
              className="w-full"
            />
          </div>

          {/* Hippocampal Volume */}
          <div>
            <label htmlFor="hippocampal_volume" className="block font-medium">
              Hippocampal Volume: {formData.hippocampal_volume}
            </label>
            <input
              id="hippocampal_volume"
              type="range"
              min={2000}
              max={5000}
              step={10}
              value={formData.hippocampal_volume ?? 0}
              onChange={(e) =>
                handleChange("hippocampal_volume", Number(e.target.value))
              }
              className="w-full"
            />
          </div>

          {/* Submit Button */}
          <Button type="submit" disabled={loading} className="w-full">
            {loading ? "Assessing..." : "🧠 Assess Alzheimer's Risk"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
