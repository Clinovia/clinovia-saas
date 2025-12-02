// app/cardiology/page.tsx
"use client";

import ModuleCard from "@/components/shared/ModuleCard";

export default function CardiologyPage() {
  const modules = [
    {
      name: "ASCVD Risk Assessment",
      description: "Estimate 10-year atherosclerotic cardiovascular risk for prevention.",
      inputs: ["Age", "Gender", "Total Cholesterol", "HDL", "Systolic BP", "Diabetes", "Smoking", "Hypertension Treatment"],
      outputs: ["10-year ASCVD risk %", "Risk Category (Low/Moderate/High)"],
      href: "/protected/cardiology/ascvd",
    },
    {
      name: "Blood Pressure Category",
      description: "Categorize blood pressure for clinical assessment.",
      inputs: ["Systolic BP", "Diastolic BP", "Patient ID"],
      outputs: ["BP Category"],
      href: "/protected/cardiology/bp-category",
    },
    {
      name: "CHA₂DS₂-VASc Score",
      description: "Assess stroke risk in atrial fibrillation patients.",
      inputs: ["Age", "Gender", "CHF", "Hypertension", "Diabetes", "Stroke/TIA", "Vascular Disease", "Patient ID"],
      outputs: ["CHA₂DS₂-VASc Score", "Risk Level"],
      href: "/protected/cardiology/cha2ds2vasc",
    },
    {
      name: "ECG Interpretation",
      description: "Analyze ECG features for rhythm abnormalities.",
      inputs: ["Heart Rate", "QRS Duration", "QT Interval", "PR Interval", "Rhythm", "ST Elevation", "T Wave Inversion"],
      outputs: ["ECG interpretation", "Abnormality flags"],
      href: "/protected/cardiology/ecg-interpreter",
    },
    {
      name: "Ejection Fraction Prediction",
      description: "Predict left ventricular ejection fraction from echocardiogram video.",
      inputs: ["Echo/video file", "Patient ID"],
      outputs: ["EF %", "EF Category (Normal, Mildly Reduced, etc.)"],
      href: "/protected/cardiology/ejection-fraction",
    },
  ];

  return (
    <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {modules.map((mod) => (
        <ModuleCard key={mod.name} {...mod} />
      ))}
    </div>
  );
}
