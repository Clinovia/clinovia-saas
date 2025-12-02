"use client";

import Link from "next/link";

export default function ModulesPage() {
  const cardiology = [
    { name: "ASCVD", description: "Atherosclerotic cardiovascular disease risk calculator", inputs: "Patient demographics, vitals, labs", outputs: "10-year ASCVD risk score" },
    { name: "Blood Pressure Category", description: "Classifies BP readings", inputs: "Systolic & diastolic BP", outputs: "BP category classification" },
    { name: "CHA2DS2VASc", description: "Stroke risk estimation in AF patients", inputs: "Clinical factors", outputs: "Risk score" },
    { name: "ECG Interpreter", description: "Basic ECG interpretation module", inputs: "ECG parameters", outputs: "Interpretation summary" },
    { name: "EF Prediction", description: "Deep learning model for EF prediction", inputs: "Clinical inputs", outputs: "Estimated EF %" },
  ];

  const neurology = [
    { name: "Risk Screener", description: "Neurologic risk screening tool", inputs: "Basic clinical inputs", outputs: "Risk assessment" },
    { name: "Diagnosis Screening", description: "Initial diagnostic triage", inputs: "Symptoms, history", outputs: "Suggested differentials" },
    { name: "Diagnosis Basic", description: "Basic diagnostic model", inputs: "Symptoms, vitals", outputs: "Preliminary diagnosis" },
    { name: "Diagnosis Extended", description: "Advanced diagnostic model", inputs: "Extended clinical data", outputs: "Detailed diagnostic output" },
    { name: "2yr Prognosis Basic", description: "Basic prognosis model", inputs: "Clinical features", outputs: "2-year prognosis" },
    { name: "2yr Prognosis Extended", description: "Advanced prognosis model", inputs: "Detailed clinical features", outputs: "Extended 2-year prognosis" },
  ];

  const renderTable = (title, data) => (
    <div className="mb-12">
      <h2 className="text-2xl font-semibold mb-4">{title}</h2>
      <table className="w-full border border-gray-300 text-left">
        <thead className="bg-gray-100">
          <tr>
            <th className="border p-2">Module</th>
            <th className="border p-2">Description</th>
            <th className="border p-2">Inputs</th>
            <th className="border p-2">Outputs</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.name}>
              <td className="border p-2 font-medium">{row.name}</td>
              <td className="border p-2">{row.description}</td>
              <td className="border p-2">{row.inputs}</td>
              <td className="border p-2">{row.outputs}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  return (
    <div className="container mx-auto py-16 px-4">
      <h1 className="text-4xl font-bold mb-10 text-center">Clinical Modules</h1>

      {renderTable("Cardiology", cardiology)}
      {renderTable("Neurology", neurology)}

      <div className="flex flex-col items-center mt-12 space-y-4">
        <Link
          href="/signup"
          className="bg-blue-600 text-white px-6 py-3 rounded-lg text-lg hover:bg-blue-700"
        >
          Get Started
        </Link>
        <Link href="/login" className="text-blue-600 hover:underline text-lg">
          Log In if you have an account
        </Link>
      </div>
    </div>
  );
}
