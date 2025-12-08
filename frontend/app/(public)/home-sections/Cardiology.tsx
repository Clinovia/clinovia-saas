import Link from "next/link";

export default function Cardiology() {
  const cardioTools = [
    {
      name: "Echonet EF Predictor",
      description:
        "Predict left ventricular ejection fraction (EF) from echocardiogram videos using deep learning.",
    },
    {
      name: "ASCVD",
      description:
        "Estimate a patient’s 10-year risk of atherosclerotic cardiovascular disease.",
    },
    {
      name: "Blood Pressure Category",
      description:
        "Classify patients based on blood pressure measurements for risk stratification.",
    },
    {
      name: "CHA2DS2VASc",
      description:
        "Calculate stroke risk in patients with atrial fibrillation.",
    },
    {
      name: "ECG Interpreter",
      description:
        "Analyze ECG data and provide automated interpretations for research purposes.",
    },
  ];

  return (
    <section id="cardiology" className="py-16 bg-white w-full">
      <div className="max-w-7xl mx-auto px-12">
        {/* Heading */}
        <div className="text-center mb-10">
          <h2
            className="text-3xl font-bold text-[#1B4D3E] mb-4"
            style={{ fontFamily: "Inter, sans-serif" }}
          >
            Cardiology
          </h2>
          <p
            className="text-lg text-[#1B4D3E] font-normal leading-relaxed"
            style={{ lineHeight: "1.8" }}
          >
            Explore our research-use-only cardiology tools for risk assessment,
            patient stratification, and algorithmic ECG interpretation.
          </p>
        </div>

        {/* Two-column layout */}
        <div className="grid md:grid-cols-2 gap-10 items-end">
          {/* Left Column: Compact Tool List */}
          <div className="flex flex-col justify-start">
            {cardioTools.map((tool, index) => (
              <div key={tool.name} className="py-2">
                <p className="text-gray-700">
                  <span className="font-semibold text-[#1B4D3E]">
                    {tool.name}:
                  </span>{" "}
                  {tool.description}
                </p>
                {index !== cardioTools.length - 1 && (
                  <hr className="border-t border-gray-300 mt-2" />
                )}
              </div>
            ))}
          </div>

          {/* Right Column: Smaller Demo Card, bottom-aligned */}
          <div
            className="bg-gray-50 text-[#1B4D3E] rounded-2xl p-6 shadow-sm flex flex-col border border-gray-200 self-end"
            style={{ width: "90%", marginLeft: "auto" }}
          >
            <div className="mb-4">
              <img
                src="/images/ascvd.png"
                alt="Cardio Tools Overview"
                className="w-full rounded-lg shadow-sm"
              />
            </div>

            <a
              href="http://44.204.193.163:7860"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block px-5 py-2.5 bg-[#8daed6] text-white font-semibold rounded-full hover:bg-[#4782c9] transition-colors text-sm text-center"
            >
              Try the Demo
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
