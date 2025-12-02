"use client";

import { useState, FormEvent } from "react";
import { ASCVDInput } from "@/features/cardiology/types";
import { Slider } from "@/components/ui/slider";
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

type Props = {
  onSubmit: (data: ASCVDInput) => void;
  loading?: boolean;
};

export default function ASCVDForm({ onSubmit, loading = false }: Props) {
  const [formData, setFormData] = useState<ASCVDInput>({
    age: 55,
    gender: "female",
    race: "white",
    total_cholesterol: 180,
    hdl_cholesterol: 50,
    systolic_bp: 120,
    on_hypertension_treatment: false,
    smoker: false,
    diabetes: false,
  });

  const handleChange = (key: keyof ASCVDInput, value: any) => {
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
              min={40}
              max={79}
              step={1}
              value={[formData.age]}
              onValueChange={(v) => handleChange("age", v[0])}
            />
          </div>

          {/* Gender */}
          <div className="space-y-2">
            <Label>Gender</Label>
            <Select
              value={formData.gender}
              onValueChange={(v) => handleChange("gender", v)}
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

          {/* Race */}
          <div className="space-y-2">
            <Label>Race</Label>
            <Select
              value={formData.race}
              onValueChange={(v) => handleChange("race", v)}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="white">White</SelectItem>
                <SelectItem value="black">Black</SelectItem>
                <SelectItem value="hispanic">Hispanic</SelectItem>
                <SelectItem value="asian">Asian</SelectItem>
                <SelectItem value="other">Other</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Total Cholesterol */}
          <div className="space-y-2">
            <Label>Total Cholesterol: {formData.total_cholesterol} mg/dL</Label>
            <Slider
              min={130}
              max={320}
              step={1}
              value={[formData.total_cholesterol]}
              onValueChange={(v) => handleChange("total_cholesterol", v[0])}
            />
          </div>

          {/* HDL Cholesterol */}
          <div className="space-y-2">
            <Label>HDL Cholesterol: {formData.hdl_cholesterol} mg/dL</Label>
            <Slider
              min={20}
              max={100}
              step={1}
              value={[formData.hdl_cholesterol]}
              onValueChange={(v) => handleChange("hdl_cholesterol", v[0])}
            />
          </div>

          {/* Systolic BP */}
          <div className="space-y-2">
            <Label>Systolic BP: {formData.systolic_bp} mmHg</Label>
            <Slider
              min={90}
              max={200}
              step={1}
              value={[formData.systolic_bp]}
              onValueChange={(v) => handleChange("systolic_bp", v[0])}
            />
          </div>

          {/* Checkboxes */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Checkbox
                checked={formData.on_hypertension_treatment}
                onCheckedChange={(v) =>
                  handleChange("on_hypertension_treatment", Boolean(v))
                }
              />
              <Label>On Hypertension Treatment</Label>
            </div>

            <div className="flex items-center space-x-2">
              <Checkbox
                checked={formData.smoker}
                onCheckedChange={(v) => handleChange("smoker", Boolean(v))}
              />
              <Label>Smoker</Label>
            </div>

            <div className="flex items-center space-x-2">
              <Checkbox
                checked={formData.diabetes}
                onCheckedChange={(v) => handleChange("diabetes", Boolean(v))}
              />
              <Label>Diabetes</Label>
            </div>
          </div>

          {/* Submit Button */}
          <Button type="submit" disabled={loading} className="w-full">
            {loading ? "Calculating..." : "🫀 Assess ASCVD Risk"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
