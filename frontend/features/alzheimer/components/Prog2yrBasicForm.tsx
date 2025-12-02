"use client";

import { useState, FormEvent } from "react";
import { AlzheimerPrognosis2yrBasicInput } from "@/features/alzheimer/types";

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
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Age */}
      <div>
        <label htmlFor="AGE" className="block font-medium">
          Age: {formData.AGE}
        </label>
        <input
          id="AGE"
          type="range"
          min={40}
          max={100}
          value={formData.AGE}
          onChange={(e) => handleChange("AGE", Number(e.target.value))}
          className="w-full"
        />
      </div>

      {/* Gender */}
      <div>
        <label htmlFor="PTGENDER" className="block font-medium">
          Gender
        </label>
        <select
          id="PTGENDER"
          value={formData.PTGENDER}
          onChange={(e) => handleChange("PTGENDER", e.target.value)}
          className="w-full border rounded p-1"
        >
          <option value="female">Female</option>
          <option value="male">Male</option>
        </select>
      </div>

      {/* Education */}
      <div>
        <label htmlFor="PTEDUCAT" className="block font-medium">
          Years of Education: {formData.PTEDUCAT}
        </label>
        <input
          id="PTEDUCAT"
          type="range"
          min={0}
          max={30}
          value={formData.PTEDUCAT}
          onChange={(e) => handleChange("PTEDUCAT", Number(e.target.value))}
          className="w-full"
        />
      </div>

      {/* ADAS13 */}
      <div>
        <label htmlFor="ADAS13" className="block font-medium">
          ADAS13: {formData.ADAS13}
        </label>
        <input
          id="ADAS13"
          type="range"
          min={0}
          max={85}
          value={formData.ADAS13}
          onChange={(e) => handleChange("ADAS13", Number(e.target.value))}
          className="w-full"
        />
      </div>

      {/* MOCA */}
      <div>
        <label htmlFor="MOCA" className="block font-medium">
          MOCA: {formData.MOCA}
        </label>
        <input
          id="MOCA"
          type="range"
          min={0}
          max={30}
          value={formData.MOCA}
          onChange={(e) => handleChange("MOCA", Number(e.target.value))}
          className="w-full"
        />
      </div>

      {/* CDRSB */}
      <div>
        <label htmlFor="CDRSB" className="block font-medium">
          CDRSB: {formData.CDRSB}
        </label>
        <input
          id="CDRSB"
          type="range"
          min={0}
          max={18}
          step={0.1}
          value={formData.CDRSB}
          onChange={(e) => handleChange("CDRSB", Number(e.target.value))}
          className="w-full"
        />
      </div>

      {/* FAQ */}
      <div>
        <label htmlFor="FAQ" className="block font-medium">
          FAQ: {formData.FAQ}
        </label>
        <input
          id="FAQ"
          type="range"
          min={0}
          max={30}
          value={formData.FAQ}
          onChange={(e) => handleChange("FAQ", Number(e.target.value))}
          className="w-full"
        />
      </div>

      {/* APOE4_count */}
      <div>
        <label htmlFor="APOE4_count" className="block font-medium">
          APOE4 Count: {formData.APOE4_count}
        </label>
        <input
          id="APOE4_count"
          type="range"
          min={0}
          max={2}
          value={formData.APOE4_count}
          onChange={(e) => handleChange("APOE4_count", Number(e.target.value))}
          className="w-full"
        />
      </div>

      {/* GDTOTAL */}
      <div>
        <label htmlFor="GDTOTAL" className="block font-medium">
          Global Deterioration (GDTOTAL): {formData.GDTOTAL}
        </label>
        <input
          id="GDTOTAL"
          type="range"
          min={1}
          max={7}
          step={0.1}
          value={formData.GDTOTAL}
          onChange={(e) => handleChange("GDTOTAL", Number(e.target.value))}
          className="w-full"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Predicting..." : "Predict 2-Year Progression"}
      </button>
    </form>
  );
}
