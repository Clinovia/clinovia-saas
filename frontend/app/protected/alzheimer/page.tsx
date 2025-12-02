"use client";

import ModuleCard from "@/components/shared/ModuleCard";

export default function NeurologyPage() {
  const modules = [
    {
      name: "Alzheimer Risk Screener",
      description:
        "Early assessment of Alzheimer's risk using demographics, cognitive scores, and hippocampal volume.",
      inputs: [
        "patient_id (optional)",
        "Age (40–90)",
        "Gender",
        "Education Years",
        "APOE4 Status",
        "Memory Score",
        "Hippocampal Volume",
      ],
      outputs: [
        "Risk Score (%)",
        "Risk Category (Low/Moderate/High/Error)",
        "Recommendation",
      ],
      href: "/protected/alzheimer/riskScreener",
    },
    {
      name: "Alzheimer Basic Diagnosis",
      description:
        "Predict cognitive status using basic cognitive & demographic features.",
      inputs: [
        "Age",
        "Gender",
        "Race",
        "Education Years",
        "MOCA",
        "ADAS13",
        "CDRSB",
        "FAQ",
      ],
      outputs: ["Predicted class (CN/MCI/AD)", "Confidence", "Probabilities"],
      href: "/protected/alzheimer/diagnosisScreening",
    },
    {
      name: "Basic Diagnosis",
      description:
        "Cognitive status prediction using basic demographic and cognitive tests.",
      inputs: [
        "AGE",
        "MMSE",
        "CDRSB",
        "FAQ",
        "PTEDUCAT",
        "PTGENDER",
        "APOE4",
        "RAVLT_immediate",
        "MOCA",
        "ADAS13",
      ],
      outputs: [
        "predicted_class (CN/MCI/AD)",
        "confidence (0–1)",
        "probabilities",
        "top_features",
      ],
      href: "/protected/alzheimer/diagnosisBasic",
    },
    {
      name: "Extended Diagnosis",
      description:
        "High-accuracy cognitive status prediction with imaging and biomarker features.",
      inputs: [
        "AGE",
        "MMSE",
        "CDRSB",
        "FAQ",
        "PTEDUCAT",
        "PTGENDER",
        "APOE4",
        "RAVLT_immediate",
        "MOCA",
        "ADAS13",
        "Hippocampus",
        "Ventricles",
        "WholeBrain",
        "Entorhinal",
        "FDG",
        "AV45",
        "PIB",
        "FBB",
        "ABETA",
        "TAU",
        "PTAU",
        "mPACCdigit",
        "mPACCtrailsB",
      ],
      outputs: [
        "predicted_class (CN/MCI/AD)",
        "confidence (0–1)",
        "probabilities",
        "top_features",
      ],
      href: "/protected/alzheimer/diagnosisExtended",
    },
    {
      name: "2-Year Prognosis Basic",
      description:
        "Predict risk of cognitive progression over 2 years using basic features.",
      inputs: [
        "Age",
        "Gender",
        "Education",
        "ADAS13",
        "MOCA",
        "CDRSB",
        "FAQ",
        "APOE4",
        "GDTOTAL",
      ],
      outputs: [
        "2-year progression risk",
        "Probabilities",
        "Confidence",
        "Top Features",
      ],
      href: "/protected/alzheimer/prognosis2yrBasic",
    },
    {
      name: "2-Year Prognosis Extended",
      description:
        "Advanced 2-year progression prediction with imaging & biomarker features.",
      inputs: ["Basic features + ABETA, TAU, PTAU, FDG, PIB, AV45, FBB"],
      outputs: [
        "2-year progression risk",
        "Probabilities",
        "Confidence",
        "Top Features",
      ],
      href: "/protected/alzheimer/prognosis2yrExtended",
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
