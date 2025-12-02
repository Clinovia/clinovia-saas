"use client";

import { useState, FormEvent } from "react";
import { BPCategoryInput } from "@/features/cardiology/types";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";

type Props = {
  onSubmit: (data: BPCategoryInput) => void;
  loading?: boolean;
};

export default function BPCategoryForm({ onSubmit, loading = false }: Props) {
  const [formData, setFormData] = useState<BPCategoryInput>({
    systolic_bp: 120,
    diastolic_bp: 80,
    patient_id: null,
  });

  const handleChange = (key: keyof BPCategoryInput, value: number) => {
    setFormData((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Blood Pressure Category Assessment</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Systolic BP */}
          <div>
            <Label htmlFor="systolic_bp">
              Systolic BP: {formData.systolic_bp} mmHg
            </Label>
            <Slider
              id="systolic_bp"
              value={[formData.systolic_bp]}
              min={70}
              max={250}
              step={1}
              onValueChange={(val) => handleChange("systolic_bp", val[0])}
            />
          </div>

          {/* Diastolic BP */}
          <div>
            <Label htmlFor="diastolic_bp">
              Diastolic BP: {formData.diastolic_bp} mmHg
            </Label>
            <Slider
              id="diastolic_bp"
              value={[formData.diastolic_bp]}
              min={40}
              max={150}
              step={1}
              onValueChange={(val) => handleChange("diastolic_bp", val[0])}
            />
          </div>

          {/* Submit Button */}
          <Button type="submit" disabled={loading}>
            {loading ? "Assessing..." : "🫀 Assess BP Category"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
