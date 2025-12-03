"use client";

import { useState, FormEvent } from "react";
import { AlzheimerPrognosis2yrExtendedInput } from "@/features/alzheimer/types";

import { Card, CardContent } from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

type Props = {
  onSubmit: (data: AlzheimerPrognosis2yrExtendedInput) => void;
  loading?: boolean;
};

export default function Prog2yrExtendedForm({ onSubmit, loading = false }: Props) {
  const [formData, setFormData] = useState<AlzheimerPrognosis2yrExtendedInput>({
    patient_id: null,
    AGE: 70,
    PTGENDER: "female",
    PTEDUCAT: 12,
    ADAS13: 10,
    CDRSB: 1,
    FAQ: 2,
    APOE4_count: 1,
    GDTOTAL: 3,
    ABETA: 900,
    TAU: 250,
    PTAU: 22,
  });

  const handleChange = (key: keyof AlzheimerPrognosis2yrExtendedInput, value: any) => {
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
          <div className="space-y-2">
            <Label>Age: {formData.AGE}</Label>
            <Slider
              min={40}
              max={100}
              step={1}
              value={[formData.AGE]}
              onValueChange={(v) => handleChange("AGE", v[0])}
            />
          </div>

          {/* Gender */}
          <div className="space-y-2">
            <Label>Gender</Label>
            <Select
              value={formData.PTGENDER}
              onValueChange={(v) => handleChange("PTGENDER", v)}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="female">Female</SelectItem>
                <SelectItem value="male">Male</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Education */}
          <div className="space-y-2">
            <Label>Years of Education: {formData.PTEDUCAT}</Label>
            <Slider
              min={0}
              max={30}
              step={1}
              value={[formData.PTEDUCAT]}
              onValueChange={(v) => handleChange("PTEDUCAT", v[0])}
            />
          </div>

          {/* ADAS13 */}
          <div className="space-y-2">
            <Label>ADAS13: {formData.ADAS13}</Label>
            <Slider
              min={0}
              max={85}
              step={1}
              value={[formData.ADAS13]}
              onValueChange={(v) => handleChange("ADAS13", v[0])}
            />
          </div>

          {/* CDRSB */}
          <div className="space-y-2">
            <Label>CDRSB: {formData.CDRSB}</Label>
            <Slider
              min={0}
              max={18}
              step={0.1}
              value={[formData.CDRSB]}
              onValueChange={(v) => handleChange("CDRSB", v[0])}
            />
          </div>

          {/* FAQ */}
          <div className="space-y-2">
            <Label>FAQ: {formData.FAQ}</Label>
            <Slider
              min={0}
              max={30}
              step={1}
              value={[formData.FAQ]}
              onValueChange={(v) => handleChange("FAQ", v[0])}
            />
          </div>

          {/* APOE4 Count */}
          <div className="space-y-2">
            <Label>APOE4 Count: {formData.APOE4_count}</Label>
            <Slider
              min={0}
              max={2}
              step={1}
              value={[formData.APOE4_count]}
              onValueChange={(v) => handleChange("APOE4_count", v[0])}
            />
          </div>

          {/* GDTOTAL */}
          <div className="space-y-2">
            <Label>Global Deterioration (GDTOTAL): {formData.GDTOTAL}</Label>
            <Slider
              min={1}
              max={7}
              step={0.1}
              value={[formData.GDTOTAL]}
              onValueChange={(v) => handleChange("GDTOTAL", v[0])}
            />
          </div>

          {/* ABETA */}
          <div className="space-y-2">
            <Label>CSF Aβ (ABETA): {formData.ABETA}</Label>
            <Slider
              min={200}
              max={2000}
              step={10}
              value={[formData.ABETA ?? 0]}
              onValueChange={(v) => handleChange("ABETA", v[0])}
            />
          </div>

          {/* TAU */}
          <div className="space-y-2">
            <Label>CSF Tau (TAU): {formData.TAU}</Label>
            <Slider
              min={50}
              max={1000}
              step={5}
              value={[formData.TAU ?? 0]}
              onValueChange={(v) => handleChange("TAU", v[0])}
            />
          </div>

          {/* PTAU */}
          <div className="space-y-2">
            <Label>CSF p-Tau (PTAU): {formData.PTAU}</Label>
            <Slider
              min={5}
              max={100}
              step={1}
              value={[formData.PTAU ?? 0]}
              onValueChange={(v) => handleChange("PTAU", v[0])}
            />
          </div>

          {/* Submit */}
          <Button type="submit" disabled={loading} className="w-full">
            {loading ? "Predicting..." : "🧬 Predict 2-Year Progression (Extended)"}
          </Button>

        </form>
      </CardContent>
    </Card>
  );
}
