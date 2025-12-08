import Link from "next/link";

export default function Neurology() {
  const neuroTools = [
    {
      name: "Alzheimer Risk Screener (Rule-Based)",
      description: `Estimate potential Alzheimer’s risk using key clinical and demographic features.`,
    },
    {
      name: "Alzheimer Diagnostic Classifiers",
      description: `Predict cognitive state (CN, MCI, AD) using a range of features from basic clinical tests to advanced multimodal biomarkers. All models were trained on ADNI data.`,
    },
    {
      name: "2-Year Cognitive Progress Predictors",
      description: `Forecast cognitive decline over 2 years using basic and advanced biomarkers, including neuroimaging and cognitive test scores.  
Built on ADNI data to assist research in Alzheimer’s progression.`,
    },
  ];

  return (
    <section id="neurology" className="py-16 bg-gray-50 w-full">
      <div className="max-w-7xl mx-auto px-12">
        {/* Heading */}
        <div className="text-center mb-10">
          <h2
            className="text-3xl font-bold text-[#1B4D3E] mb-4"
            style={{ fontFamily: "Inter, sans-serif" }}
          >
            Neurology
          </h2>
          <p
            className="text-lg text-[#1B4D3E] font-normal leading-relaxed"
            style={{ lineHeight: "1.8" }}
          >
            Explore our research-use-only neurology tools for Alzheimer’s disease
            risk assessment, diagnosis, and progression prediction.
          </p>
        </div>

        {/* Two-column layout */}
        <div className="grid md:grid-cols-2 gap-10 items-start">
          {/* Left Column: Demo Card */}
          <div
            className="bg-white text-[#1B4D3E] rounded-2xl p-6 shadow-sm flex flex-col border border-gray-200 self-start"
            style={{ width: "90%", marginRight: "auto" }}
          >
            <div className="mb-4">
              <img
                src="/images/shap_global.png"
                alt="Neurology Tools Overview"
                className="w-full rounded-lg shadow-sm"
              />
            </div>

            <a
              href="http://3.94.152.216:7860"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block px-5 py-2.5 bg-[#8daed6] text-white font-semibold rounded-full hover:bg-[#4782c9] transition-colors text-sm text-center"
            >
              Try the Demo
            </a>
          </div>

          {/* Right Column: Compact Tool List */}
          <div className="flex flex-col justify-start space-y-6">
            {neuroTools.map((tool, index) => (
              <div key={tool.name}>
                <h3 className="text-base font-semibold text-[#1B4D3E] mb-2">{tool.name}</h3>
                {tool.description.split("\n").map((line, i) => (
                  <p key={i} className="text-gray-700 mb-1">
                    {line}
                  </p>
                ))}
                {index !== neuroTools.length - 1 && (
                  <hr className="border-t border-gray-300 mt-2" />
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
