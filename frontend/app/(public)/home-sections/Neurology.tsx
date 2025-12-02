export default function Neurology() {
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
          <p className="text-lg text-[#1B4D3E] leading-relaxed">
            Explore AI-assisted neurology tools for Alzheimer’s disease screening
            and diagnostic classification.
          </p>
        </div>

        {/* Two-column layout */}
        <div className="grid md:grid-cols-2 gap-10 items-end">
          {/* Left Column: Alzheimer Card */}
          <div
            className="bg-white text-[#1B4D3E] rounded-2xl p-6 shadow-sm flex flex-col border border-gray-200 self-end"
            style={{ width: "90%", marginRight: "auto" }}
          >
            <div className="mb-4">
              <img
                src="/images/shap_global.png"
                alt="Alzheimer Diagnostic Tools"
                className="w-full rounded-lg shadow-sm"
              />
            </div>

            <a
              href="https://huggingface.co/spaces/Clinovia/alzheimer-diagnosis"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block px-5 py-2.5 bg-[#8daed6] text-white font-semibold rounded-full hover:bg-[#4782c9] transition-colors text-sm text-center"
            >
              Try the Demo
            </a>
          </div>

          {/* Right Column: Descriptions */}
          <div className="flex flex-col justify-start space-y-6">
            {/* Alzheimer Diagnostic Classifier */}
            <div>
              <h3 className="text-xl font-semibold text-[#1B4D3E] mb-2">
                Alzheimer Diagnostic Classifier
              </h3>
              <p className="text-gray-700 mb-2">
                Based on ADNI data, predicts cognitive state:{" "}
                <strong>CN</strong>, <strong>MCI</strong>, or <strong>AD</strong>.
              </p>
              <p className="mb-4 text-gray-700">
                This RUO Alzheimer classification tool was built on data from the{" "}
                <a
                  href="https://adni.loni.usc.edu"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-[#1B4D3E] underline hover:text-green-800 transition-colors font-medium"
                >
                  Alzheimer’s Disease Neuroimaging Initiative (ADNI)
                </a>
                . It was trained using XGBoost on a dataset of 2,618 patients with
                94% accuracy.
              </p>
              <p className="text-sm text-gray-600">
                <strong>Features:</strong> age, gender, race, education_years, moca_score, adas13_score, cdr_sum, faq_total
              </p>
            </div>

            <hr className="border-t border-gray-300" />

            {/* Alzheimer Risk Screener */}
            <div>
              <h3 className="text-xl font-semibold text-[#1B4D3E] mb-2">
                Alzheimer Risk Screener (Rule-Based)
              </h3>
              <p className="text-gray-700 mb-2">
                A rule-based screener to estimate potential Alzheimer’s risk.
              </p>
              <p className="text-sm text-gray-600">
                <strong>Features:</strong> age, gender, race, education_years, apoe4_status, memory_score, hippocampal_volume
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
