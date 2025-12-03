"use client";

import { useState, FormEvent } from "react";
import { Race } from "@/features/alzheimer/types";
import { AlzheimerDiagnosisScreeningInput } from "@/features/alzheimer/types";
import { Card, CardContent } from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

type Props = {
  onSubmit: (data: AlzheimerDiagnosisScreeningInput) => void;
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

export default function DiagnosisScreeningForm({ onSubmit, loading = false }: Props) {
  const [formData, setFormData] = useState<AlzheimerDiagnosisScreeningInput>({
    age: 75,
    education_years: 16,
    moca_score: 26,
    adas13_score: 10,
    cdr_sum: 1,
    faq_total: 5,
    gender: "female",
    race: 1,
  });

  const handleChange = <K extends keyof AlzheimerDiagnosisScreeningInput>(
    key: K,
    value: AlzheimerDiagnosisScreeningInput[K]
  ) => {
    setFormData((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Card className="p-6 rounded-2xl shadow-md">
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Age */}
          <div className="space-y-2">
            <Label>Age: {formData.age}</Label>
            <Slider
              min={50}
              max={95}
              step={1}
              value={[formData.age]}
              onValueChange={(v) => handleChange("age", v[0])}
            />
          </div>

          {/* Education Years */}
          <div className="space-y-2">
            <Label>Years of Education: {formData.education_years}</Label>
            <Slider
              min={6}
              max={20}
              step={1}
              value={[formData.education_years]}
              onValueChange={(v) => handleChange("education_years", v[0])}
            />
          </div>

          {/* MoCA Score */}
          <div className="space-y-2">
            <Label>MoCA Score: {formData.moca_score}</Label>
            <Slider
              min={0}
              max={30}
              step={1}
              value={[formData.moca_score]}
              onValueChange={(v) => handleChange("moca_score", v[0])}
            />
          </div>

          {/* ADAS13 Score */}
          <div className="space-y-2">
            <Label>ADAS13 Score: {formData.adas13_score}</Label>
            <Slider
              min={0}
              max={70}
              step={0.5}
              value={[formData.adas13_score]}
              onValueChange={(v) => handleChange("adas13_score", v[0])}
            />
          </div>

          {/* CDR Sum */}
          <div className="space-y-2">
            <Label>CDR Sum: {formData.cdr_sum}</Label>
            <Slider
              min={0}
              max={18}
              step={0.5}
              value={[formData.cdr_sum]}
              onValueChange={(v) => handleChange("cdr_sum", v[0])}
            />
          </div>

          {/* FAQ Total */}
          <div className="space-y-2">
            <Label>FAQ Total: {formData.faq_total}</Label>
            <Slider
              min={0}
              max={30}
              step={1}
              value={[formData.faq_total]}
              onValueChange={(v) => handleChange("faq_total", v[0])}
            />
          </div>

          {/* Gender */}
          <div className="space-y-2">
            <Label>Gender</Label>
            <Select
              value={formData.gender}
              onValueChange={(v) =>
                handleChange("gender", v as "female" | "male")
              }
            >
              <SelectTrigger>
                <SelectValue placeholder="Select gender" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="female">Female</SelectItem>
                <SelectItem value="male">Male</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Race */}
          <div className="space-y-2">
            <Label>Race</Label>
            <Select
              value={String(formData.race)}
              onValueChange={(v) => handleChange("race", Number(v) as Race)}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select race" />
              </SelectTrigger>
              <SelectContent>
                {Object.entries(raceMap).map(([key, label]) => (
                  <SelectItem key={key} value={key}>
                    {label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Submit */}
          <Button type="submit" disabled={loading} className="w-full">
            {loading ? "Predicting..." : "Predict"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
