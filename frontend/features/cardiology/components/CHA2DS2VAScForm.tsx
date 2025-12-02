"use client";

import { useState, FormEvent } from "react";
import { CHA2DS2VAScInput } from "@/features/cardiology/types";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";

type Props = {
  onSubmit: (data: CHA2DS2VAScInput) => void;
  loading?: boolean;
};

export default function CHA2DS2VAScForm({ onSubmit, loading = false }: Props) {
  const [formData, setFormData] = useState<CHA2DS2VAScInput>({
    age: 65,
    gender: "female",
    congestive_heart_failure: false,
    hypertension: false,
    diabetes: false,
    stroke_tia_thromboembolism: false,
    vascular_disease: false,
    patient_id: null,
  });

  const handleChange = (key: keyof CHA2DS2VAScInput, value: any) => {
    setFormData((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>CHA₂DS₂-VASc Score Assessment</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Age Slider */}
          <div>
            <Label htmlFor="age">Age: {formData.age}</Label>
            <Slider
              id="age"
              value={[formData.age]}
              min={18}
              max={120}
              step={1}
              onValueChange={(val) => handleChange("age", val[0])}
            />
          </div>

          {/* Gender */}
          <div>
            <Label htmlFor="gender">Gender</Label>
            <select
              id="gender"
              value={formData.gender}
              onChange={(e) => handleChange("gender", e.target.value)}
              className="w-full border rounded p-1"
            >
              <option value="female">Female</option>
              <option value="male">Male</option>
            </select>
          </div>

          {/* Checkboxes */}
          <div className="space-y-2">
            {[
              ["congestive_heart_failure", "Congestive Heart Failure"],
              ["hypertension", "Hypertension"],
              ["diabetes", "Diabetes"],
              ["stroke_tia_thromboembolism", "Stroke / TIA / Thromboembolism"],
              ["vascular_disease", "Vascular Disease"],
            ].map(([key, label]) => (
              <div key={key} className="flex items-center space-x-2">
                <Checkbox
                  checked={formData[key as keyof CHA2DS2VAScInput] as boolean}
                  onCheckedChange={(checked) =>
                    handleChange(key as keyof CHA2DS2VAScInput, checked)
                  }
                />
                <span>{label}</span>
              </div>
            ))}
          </div>

          {/* Submit Button */}
          <Button type="submit" disabled={loading}>
            {loading ? "Calculating..." : "🫀 Assess CHA₂DS₂-VASc"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
