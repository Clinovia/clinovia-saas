"use client";

import { useState, FormEvent } from "react";
import { AlzheimerPrognosis2yrBasicInput } from "@/features/alzheimer/types";

import { Card, CardContent } from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

type Props = {
  onSubmit: (data: AlzheimerPrognosis2yrBasicInput) => void;
  loading?: boolean;
};

export default function Prog2yrBasicForm({ onSubmit, loading = false }: Props) {
  const [formData, setFormData] = useState<AlzheimerPrognosis2yrBasicInput>({
    patient_id: null,
    AGE: 70,
    PTGENDER: "female",
    PTEDUCAT: 12,
    ADAS13: 10,
    MOCA: 25,
    CDRSB: 1,
    FAQ: 2,
    APOE4_count: 1,
    GDTOTAL: 3,
  });

  const handleChange = (key: keyof AlzheimerPrognosis2yrBasicInput, value: any) => {
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

          {/* MOCA */}
          <div className="space-y-2">
            <Label>MOCA: {formData.MOCA}</Label>
            <Slider
              min={0}
              max={30}
              step={1}
              value={[formData.MOCA]}
              onValueChange={(v) => handleChange("MOCA", v[0])}
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

          {/* Submit */}
          <Button type="submit" disabled={loading} className="w-full">
            {loading ? "Predicting..." : "🧠 Predict 2-Year Progression"}
          </Button>

        </form>
      </CardContent>
    </Card>
  );
}
