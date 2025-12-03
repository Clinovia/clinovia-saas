"use client";

import { useState, FormEvent } from "react";
import { AlzheimerDiagnosisExtendedInput } from "@/features/alzheimer/types";
import { Card, CardContent } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

type Props = {
  onSubmit: (data: AlzheimerDiagnosisExtendedInput) => void;
  loading?: boolean;
};

export default function DiagExtendedForm({ onSubmit, loading = false }: Props) {
  const [formData, setFormData] = useState<AlzheimerDiagnosisExtendedInput>({
    AGE: 72,
    MMSE_bl: 25,
    CDRSB_bl: 1.5,
    FAQ_bl: 4,
    PTEDUCAT: 14,
    PTGENDER: "male",
    APOE4: 1,
    RAVLT_immediate_bl: 32,
    MOCA_bl: 24,
    ADAS13_bl: 12,
    Hippocampus_bl: 6000,
    Ventricles_bl: 45000,
    WholeBrain_bl: 950000,
    Entorhinal_bl: 3500,
    FDG_bl: 1.25,
    AV45_bl: 1.35,
    PIB_bl: 1.28,
    FBB_bl: 1.2,
    ABETA_bl: 180,
    TAU_bl: 350,
    PTAU_bl: 55,
    mPACCdigit_bl: 0.45,
    mPACCtrailsB_bl: -0.6,
    patient_id: null,
  });

  const handleChange = (key: keyof AlzheimerDiagnosisExtendedInput, value: any) => {
    setFormData((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const sliderFields: Array<[keyof AlzheimerDiagnosisExtendedInput, string, number, number, number]> = [
    ["AGE", "Age", 0, 120, 1],
    ["MMSE_bl", "MMSE", 0, 30, 1],
    ["CDRSB_bl", "CDRSB", 0, 20, 0.1],
    ["FAQ_bl", "FAQ", 0, 30, 0.1],
    ["PTEDUCAT", "Years of Education", 0, 30, 1],
    ["RAVLT_immediate_bl", "RAVLT Immediate", 0, 50, 1],
    ["MOCA_bl", "MOCA", 0, 30, 1],
    ["ADAS13_bl", "ADAS13", 0, 100, 0.1],
    ["Hippocampus_bl", "Hippocampus", 0, 10000, 1],
    ["Ventricles_bl", "Ventricles", 0, 100000, 10],
    ["WholeBrain_bl", "Whole Brain", 0, 2000000, 1000],
    ["Entorhinal_bl", "Entorhinal", 0, 10000, 1],
    ["FDG_bl", "FDG", 0, 5, 0.01],
    ["AV45_bl", "AV45", 0, 5, 0.01],
    ["PIB_bl", "PIB", 0, 5, 0.01],
    ["FBB_bl", "FBB", 0, 5, 0.01],
    ["ABETA_bl", "ABETA", 0, 1000, 1],
    ["TAU_bl", "TAU", 0, 1000, 1],
    ["PTAU_bl", "PTAU", 0, 100, 0.1],
    ["mPACCdigit_bl", "mPACCdigit", -5, 5, 0.01],
    ["mPACCtrailsB_bl", "mPACCtrailsB", -5, 5, 0.01],
  ];

  return (
    <Card className="p-6 rounded-2xl shadow-md max-w-3xl mx-auto">
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">

          {/* Gender */}
          <div>
            <Label htmlFor="PTGENDER">Gender</Label>
            <select
              id="PTGENDER"
              value={formData.PTGENDER}
              onChange={(e) => handleChange("PTGENDER", e.target.value)}
              className="w-full border rounded px-3 py-2"
            >
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
          </div>

          {/* APOE4 */}
          <div>
            <Label htmlFor="APOE4">APOE4 Allele Count: {formData.APOE4}</Label>
            <input
              id="APOE4"
              type="range"
              min={0}
              max={2}
              step={1}
              value={formData.APOE4}
              onChange={(e) => handleChange("APOE4", Number(e.target.value))}
              className="w-full"
            />
          </div>

          {/* Sliders */}
          {sliderFields.map(([key, label, min, max, step]) => (
            <div key={key}>
              <Label htmlFor={key}>
                {label}: {formData[key] ?? 0}
              </Label>
              <input
                id={key}
                type="range"
                min={min}
                max={max}
                step={step}
                value={formData[key] ?? 0}
                onChange={(e) => handleChange(key, Number(e.target.value))}
                className="w-full"
              />
            </div>
          ))}

          {/* Submit */}
          <Button type="submit" disabled={loading} className="w-full">
            {loading ? "Assessing..." : "🧠 Assess Extended Diagnosis"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
