"use client";

import { useState, FormEvent } from "react";
import { AlzheimerDiagnosisBasicInput } from "@/features/alzheimer/types";

type Props = {
  onSubmit: (data: AlzheimerDiagnosisBasicInput) => void;
  loading?: boolean;
};

// ✅ Helper to display clean field names (removes _bl suffix)
const getDisplayLabel = (fieldName: string): string => {
  const labels: Record<string, string> = {
    AGE: "Age",
    MMSE_bl: "MMSE (Mini-Mental State Exam)",
    CDRSB_bl: "CDR Sum of Boxes",
    FAQ_bl: "FAQ (Functional Activities)",
    PTEDUCAT: "Education (years)",
    PTGENDER: "Gender",
    APOE4: "APOE4 Allele Count",
    RAVLT_immediate_bl: "RAVLT Immediate Recall",
    MOCA_bl: "MoCA (Montreal Cognitive Assessment)",
    ADAS13_bl: "ADAS13 (Alzheimer's Disease Assessment)",
  };
  return labels[fieldName] || fieldName;
};

export default function DiagBasicForm({ onSubmit, loading = false }: Props) {
  // ✅ State includes PTGENDER and APOE4
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
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* AGE */}
      <div>
        <label htmlFor="AGE" className="block font-medium">
          {getDisplayLabel("AGE")}
        </label>
        <input
          id="AGE"
          type="range"
          min={18}
          max={120}
          value={formData.AGE}
          onChange={(e) => handleChange("AGE", Number(e.target.value))}
          className="w-full"
        />
        <span className="ml-2">{formData.AGE} yrs</span>
      </div>

      {/* PTGENDER */}
      <div>
        <label htmlFor="PTGENDER" className="block font-medium">
          {getDisplayLabel("PTGENDER")}
        </label>
        <select
          id="PTGENDER"
          value={formData.PTGENDER}
          onChange={(e) => handleChange("PTGENDER", e.target.value)}
          className="w-full border border-gray-300 rounded px-3 py-2"
        >
          <option value="male">Male</option>
          <option value="female">Female</option>
        </select>
      </div>

      {/* APOE4 */}
      <div>
        <label htmlFor="APOE4" className="block font-medium">
          {getDisplayLabel("APOE4")}
        </label>
        <select
          id="APOE4"
          value={formData.APOE4}
          onChange={(e) => handleChange("APOE4", Number(e.target.value))}
          className="w-full border border-gray-300 rounded px-3 py-2"
        >
          <option value={-1}>Unknown</option>
          <option value={0}>0 (No alleles)</option>
          <option value={1}>1 (One allele)</option>
          <option value={2}>2 (Two alleles)</option>
        </select>
        <p className="text-sm text-gray-500 mt-1">
          Number of APOE4 alleles (genetic risk factor for Alzheimer's)
        </p>
      </div>

      {/* MMSE_bl */}
      <div>
        <label htmlFor="MMSE_bl" className="block font-medium">
          {getDisplayLabel("MMSE_bl")}
        </label>
        <input
          id="MMSE_bl"
          type="range"
          min={0}
          max={30}
          value={formData.MMSE_bl}
          onChange={(e) => handleChange("MMSE_bl", Number(e.target.value))}
          className="w-full"
        />
        <span className="ml-2">{formData.MMSE_bl}</span>
      </div>

      {/* CDRSB_bl */}
      <div>
        <label htmlFor="CDRSB_bl" className="block font-medium">
          {getDisplayLabel("CDRSB_bl")}
        </label>
        <input
          id="CDRSB_bl"
          type="range"
          min={0}
          max={20}
          step={0.1}
          value={formData.CDRSB_bl}
          onChange={(e) => handleChange("CDRSB_bl", Number(e.target.value))}
          className="w-full"
        />
        <span className="ml-2">{formData.CDRSB_bl}</span>
      </div>

      {/* FAQ_bl */}
      <div>
        <label htmlFor="FAQ_bl" className="block font-medium">
          {getDisplayLabel("FAQ_bl")}
        </label>
        <input
          id="FAQ_bl"
          type="range"
          min={0}
          max={30}
          step={0.1}
          value={formData.FAQ_bl}
          onChange={(e) => handleChange("FAQ_bl", Number(e.target.value))}
          className="w-full"
        />
        <span className="ml-2">{formData.FAQ_bl}</span>
      </div>

      {/* PTEDUCAT */}
      <div>
        <label htmlFor="PTEDUCAT" className="block font-medium">
          {getDisplayLabel("PTEDUCAT")}
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
        <span className="ml-2">{formData.PTEDUCAT} yrs</span>
      </div>

      {/* RAVLT_immediate_bl */}
      <div>
        <label htmlFor="RAVLT_immediate_bl" className="block font-medium">
          {getDisplayLabel("RAVLT_immediate_bl")}
        </label>
        <input
          id="RAVLT_immediate_bl"
          type="range"
          min={0}
          max={75}
          value={formData.RAVLT_immediate_bl}
          onChange={(e) => handleChange("RAVLT_immediate_bl", Number(e.target.value))}
          className="w-full"
        />
        <span className="ml-2">{formData.RAVLT_immediate_bl}</span>
      </div>

      {/* MOCA_bl */}
      <div>
        <label htmlFor="MOCA_bl" className="block font-medium">
          {getDisplayLabel("MOCA_bl")}
        </label>
        <input
          id="MOCA_bl"
          type="range"
          min={0}
          max={30}
          value={formData.MOCA_bl}
          onChange={(e) => handleChange("MOCA_bl", Number(e.target.value))}
          className="w-full"
        />
        <span className="ml-2">{formData.MOCA_bl}</span>
      </div>

      {/* ADAS13_bl */}
      <div>
        <label htmlFor="ADAS13_bl" className="block font-medium">
          {getDisplayLabel("ADAS13_bl")}
        </label>
        <input
          id="ADAS13_bl"
          type="range"
          min={0}
          max={100}
          step={0.1}
          value={formData.ADAS13_bl}
          onChange={(e) => handleChange("ADAS13_bl", Number(e.target.value))}
          className="w-full"
        />
        <span className="ml-2">{formData.ADAS13_bl}</span>
      </div>

      {/* Submit */}
      <button
        type="submit"
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Predicting..." : "🧠 Predict Diagnosis"}
      </button>
    </form>
  );
}