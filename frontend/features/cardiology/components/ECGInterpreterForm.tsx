"use client";

import { useState, FormEvent } from "react";
import { ECGInterpreterInput } from "@/features/cardiology/types";
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
  onSubmit: (data: ECGInterpreterInput) => void;
  loading?: boolean;
};

export default function ECGInterpreterForm({ onSubmit, loading = false }: Props) {
  const [formData, setFormData] = useState<ECGInterpreterInput>({
    heart_rate: 70,
    qrs_duration: 100,
    qt_interval: 400,
    pr_interval: 160,
    rhythm: "sinus",
    st_elevation: false,
    t_wave_inversion: false,
    patient_id: null,
  });

  const handleChange = (key: keyof ECGInterpreterInput, value: any) => {
    setFormData((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>ECG Interpretation</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Heart Rate */}
          <div>
            <Label htmlFor="heart_rate">Heart Rate: {formData.heart_rate} bpm</Label>
            <Slider
              id="heart_rate"
              value={[formData.heart_rate  ?? 0]}
              min={20}
              max={300}
              step={1}
              onValueChange={(val) => handleChange("heart_rate", val[0])}
            />
          </div>

          {/* QRS Duration */}
          <div>
            <Label htmlFor="qrs_duration">QRS Duration: {formData.qrs_duration} ms</Label>
            <Slider
              id="qrs_duration"
              value={[formData.qrs_duration ?? 0]}
              min={50}
              max={200}
              step={1}
              onValueChange={(val) => handleChange("qrs_duration", val[0])}
            />
          </div>

          {/* QT Interval */}
          <div>
            <Label htmlFor="qt_interval">QT Interval: {formData.qt_interval} ms</Label>
            <Slider
              id="qt_interval"
              value={[formData.qt_interval ?? 0]}
              min={300}
              max={600}
              step={1}
              onValueChange={(val) => handleChange("qt_interval", val[0])}
            />
          </div>

          {/* PR Interval */}
          <div>
            <Label htmlFor="pr_interval">PR Interval: {formData.pr_interval} ms</Label>
            <Slider
              id="pr_interval"
              value={[formData.pr_interval ?? 0]}
              min={80}
              max={400}
              step={1}
              onValueChange={(val) => handleChange("pr_interval", val[0])}
            />
          </div>

          {/* Rhythm */}
          <div>
            <Label htmlFor="rhythm">Rhythm</Label>
            <select
              id="rhythm"
              value={formData.rhythm}
              onChange={(e) => handleChange("rhythm", e.target.value)}
              className="w-full border rounded p-1"
            >
              <option value="sinus">Sinus</option>
              <option value="afib">Atrial Fibrillation</option>
              <option value="flutter">Atrial Flutter</option>
              <option value="other">Other</option>
            </select>
          </div>

          {/* Checkboxes */}
          <div className="space-y-2">
            {[
              ["st_elevation", "ST Elevation"],
              ["t_wave_inversion", "T Wave Inversion"],
            ].map(([key, label]) => (
              <div key={key} className="flex items-center space-x-2">
                <Checkbox
                  checked={formData[key as keyof ECGInterpreterInput] as boolean}
                  onCheckedChange={(checked) =>
                    handleChange(key as keyof ECGInterpreterInput, checked)
                  }
                />
                <span>{label}</span>
              </div>
            ))}
          </div>

          {/* Submit Button */}
          <Button type="submit" disabled={loading}>
            {loading ? "Submitting..." : "🫀 Submit ECG"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
