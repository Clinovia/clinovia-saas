"use client";

import { useState, FormEvent } from "react";
import { AlzheimerDiagnosisBasicInput } from "@/features/alzheimer/types";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

// Clean label map
const getDisplayLabel = (fieldName: string): string => {
  const labels: Record<string, string> = {
    AGE: "Age",
    MMSE_bl: "MMSE",
    CDRSB_bl: "CDR Sum of Boxes",
    FAQ_bl: "FAQ Score",
    PTEDUCAT: "Education (years)",
    PTGENDER: "Gender",
    APOE4: "APOE4 Allele Count",
    RAVLT_immediate_bl: "RAVLT Immediate Recall",
    MOCA_bl: "MoCA Score",
    ADAS13_bl: "ADAS13 Score",
  };
  return labels[fieldName] || fieldName;
};

type Props = {
  onSubmit: (data: AlzheimerDiagnosisBasicInput) => void;
  loading?: boolean;
};

export default function DiagBasicForm({ onSubmit, loading = false }: Props) {
  const [formData, setFormData] = useState<AlzheimerDiagnosisBasicInput>({
    patient_id: null,
    AGE: 74,
    MMSE_bl: 26,
    CDRSB_bl: 1,
    FAQ_bl: 3,
    PTEDUCAT: 16,
    PTGENDER: "female",
    APOE4: 1,
    RAVLT_immediate_bl: 35,
    MOCA_bl: 25,
    ADAS13_bl: 10.5,
  });

  const handleChange = (key: keyof AlzheimerDiagnosisBasicInput, value: number | string) => {
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
          {/* AGE */}
          <div>
            <Label htmlFor="AGE">{getDisplayLabel("AGE")}: {formData.AGE} yrs</Label>
            <input
              type="range"
              min={18}
              max={120}
              value={formData.AGE}
              onChange={(e) => handleChange("AGE", Number(e.target.value))}
              className="w-full"
            />
          </div>

          {/* Gender */}
          <div>
            <Label htmlFor="PTGENDER">{getDisplayLabel("PTGENDER")}</Label>
            <select
              id="PTGENDER"
              value={formData.PTGENDER}
              onChange={(e) => handleChange("PTGENDER", e.target.value)}
              className="w-full border rounded px-3 py-2"
            >
              <option value="female">Female</option>
              <option value="male">Male</option>
            </select>
          </div>

          {/* APOE4 */}
          <div>
            <Label htmlFor="APOE4">{getDisplayLabel("APOE4")}</Label>
            <select
              id="APOE4"
              value={formData.APOE4}
              onChange={(e) => handleChange("APOE4", Number(e.target.value))}
              className="w-full border rounded px-3 py-2"
            >
              <option value={-1}>Unknown</option>
              <option value={0}>0 alleles</option>
              <option value={1}>1 allele</option>
              <option value={2}>2 alleles</option>
            </select>
          </div>

          {/* MMSE */}
          <div>
            <Label htmlFor="MMSE_bl">{getDisplayLabel("MMSE_bl")}: {formData.MMSE_bl}</Label>
            <input
              type="range"
              min={0}
              max={30}
              value={formData.MMSE_bl}
              onChange={(e) => handleChange("MMSE_bl", Number(e.target.value))}
              className="w-full"
            />
          </div>

          {/* CDRSB */}
          <div>
            <Label htmlFor="CDRSB_bl">{getDisplayLabel("CDRSB_bl")}: {formData.CDRSB_bl}</Label>
            <input
              type="range"
              min={0}
              max={20}
              step={0.1}
              value={formData.CDRSB_bl}
              onChange={(e) => handleChange("CDRSB_bl", Number(e.target.value))}
              className="w-full"
            />
          </div>

          {/* FAQ */}
          <div>
            <Label htmlFor="FAQ_bl">{getDisplayLabel("FAQ_bl")}: {formData.FAQ_bl}</Label>
            <input
              type="range"
              min={0}
              max={30}
              step={0.1}
              value={formData.FAQ_bl}
              onChange={(e) => handleChange("FAQ_bl", Number(e.target.value))}
              className="w-full"
            />
          </div>

          {/* Education */}
          <div>
            <Label htmlFor="PTEDUCAT">
              {getDisplayLabel("PTEDUCAT")}: {formData.PTEDUCAT} yrs
            </Label>
            <input
              type="range"
              min={0}
              max={30}
              value={formData.PTEDUCAT}
              onChange={(e) => handleChange("PTEDUCAT", Number(e.target.value))}
              className="w-full"
            />
          </div>

          {/* RAVLT */}
          <div>
            <Label htmlFor="RAVLT_immediate_bl">
              {getDisplayLabel("RAVLT_immediate_bl")}: {formData.RAVLT_immediate_bl}
            </Label>
            <input
              type="range"
              min={0}
              max={75}
              value={formData.RAVLT_immediate_bl}
              onChange={(e) => handleChange("RAVLT_immediate_bl", Number(e.target.value))}
              className="w-full"
            />
          </div>

          {/* MoCA */}
          <div>
            <Label htmlFor="MOCA_bl">{getDisplayLabel("MOCA_bl")}: {formData.MOCA_bl}</Label>
            <input
              type="range"
              min={0}
              max={30}
              value={formData.MOCA_bl}
              onChange={(e) => handleChange("MOCA_bl", Number(e.target.value))}
              className="w-full"
            />
          </div>

          {/* ADAS13 */}
          <div>
            <Label htmlFor="ADAS13_bl">
              {getDisplayLabel("ADAS13_bl")}: {formData.ADAS13_bl}
            </Label>
            <input
              type="range"
              min={0}
              max={100}
              step={0.1}
              value={formData.ADAS13_bl}
              onChange={(e) => handleChange("ADAS13_bl", Number(e.target.value))}
              className="w-full"
            />
          </div>

          {/* Submit */}
          <Button type="submit" disabled={loading} className="w-full">
            {loading ? "Predicting..." : "🧠 Predict Diagnosis"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
