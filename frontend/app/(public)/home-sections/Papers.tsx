// components/Papers.tsx
export default function Papers() {
  return (
    <section id="papers" className="py-16 bg-white">
      <div className="max-w-5xl mx-auto px-6">
        {/* Section Heading */}
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-[#1B4D3E] mb-4">
            Related Papers
          </h2>
          <p className="text-lg text-gray-700 leading-relaxed">
            Explore peer-reviewed research and technical insights behind Clinovia’s AI-powered cardiovascular and neurodegenerative risk assessment tools.
          </p>
        </div>

        {/* Papers List */}
        <div className="space-y-8">
          {/* Paper 1: AI in CVD Risk */}
          <div className="border-l-4 border-[#B5D9A3] pl-6 py-2 hover:bg-gray-50 rounded-r-lg transition">
            <h3 className="text-xl font-semibold text-[#1B4D3E] mb-2">
              Advancing Cardiovascular Risk Prediction: A Review of Machine Learning Models and Their Clinical Potential
            </h3>
            <p className="text-gray-600 mb-3">
              <strong>Journal:</strong> Life (MDPI), 2025
            </p>
            <p className="text-gray-700 mb-3">
              This review examines the latest AI techniques for predicting cardiovascular risk,
              addressing strengths, limitations, and steps toward clinical integration.
            </p>
            <a
              href="https://www.researchgate.net/publication/391162367_Advancing_Cardiovascular_Risk_Prediction_A_Review_of_Machine_Learning_Models_and_Their_Clinical_Potential"
              className="text-[#1B4D3E] underline hover:text-green-800 font-medium text-sm transition-colors"
            >
              Read Full Review
            </a>
          </div>

          {/* Paper 2: XGBoost & MCI Prediction */}
          <div className="border-l-4 border-[#B5D9A3] pl-6 py-2 hover:bg-gray-50 rounded-r-lg transition">
            <h3 className="text-xl font-semibold text-[#1B4D3E] mb-2">
              XGBoost Models Based on Non-Imaging Features for Prediction of Mild Cognitive Impairment in Older Adults
            </h3>
            <p className="text-gray-600 mb-3">
              <strong>Journal:</strong> Scientific Reports, 2025
            </p>
            <p className="text-gray-700 mb-3">
              Uses features like demographics and cognitive scores (no imaging) to model MCI,
              leveraging SHAP for feature interpretability.
            </p>
            <a
              href="https://doi.org/10.1038/s41598-025-14832-0"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[#1B4D3E] underline hover:text-green-800 font-medium text-sm transition-colors"
            >
              View on Scientific Reports
            </a>
          </div>

          {/* Paper 3: Survival Modeling of MCI Progression */}
          <div className="border-l-4 border-[#B5D9A3] pl-6 py-2 hover:bg-gray-50 rounded-r-lg transition">
            <h3 className="text-xl font-semibold text-[#1B4D3E] mb-2">
              Predicting Deterioration in Mild Cognitive Impairment with Survival Transformers, XGBoost & Cox Models
            </h3>
            <p className="text-gray-600 mb-3">
              <strong>Repository:</strong> arXiv (2024)
            </p>
            <p className="text-gray-700 mb-3">
              Compares survival transformer and XGBoost models in forecasting cognitive decline,
              highlighting their predictive accuracy and stability.
            </p>
            <a
              href="https://arxiv.org/abs/2409.16231"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[#1B4D3E] underline hover:text-green-800 font-medium text-sm transition-colors"
            >
              Read on arXiv
            </a>
          </div>
        </div>

        {/* RUO Disclaimer */}
        <div className="text-center mt-10 text-sm text-gray-500">
          Clinovia’s tools are research-use-only (RUO) and built on peer-reviewed methodologies.
        </div>
      </div>
    </section>
  );
}
