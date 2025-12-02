export default function Features() {
  return (
    <section id="features" className="py-16 bg-gray-50 w-full">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <h2 className="text-3xl font-bold text-center text-green-900">
          Who Benefits from Clinovia.ai
        </h2>
        <p className="mt-4 text-lg text-center text-green-800/90">
          Clinovia.ai’s Research Use Only (RUO) solutions empower hospitals,
          contract research organizations (CROs), and pharmaceutical companies to
          accelerate discovery and improve evidence-based decision making in
          neurology and cardiology.
        </p>

        <div className="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {/* Hospitals */}
          <div className="rounded-2xl bg-white shadow-lg p-6 hover:shadow-xl transition-all duration-300">
            <h3 className="text-xl font-semibold text-green-900">Hospitals</h3>
            <p className="mt-4 text-green-800">
              Evaluate AI-driven diagnostics in controlled research settings to
              explore new approaches for cardiovascular and cognitive assessment.
            </p>
          </div>

          {/* CROs */}
          <div className="rounded-2xl bg-white shadow-lg p-6 hover:shadow-xl transition-all duration-300">
            <h3 className="text-xl font-semibold text-green-900">Contract Research Organizations (CROs)</h3>
            <p className="mt-4 text-green-800">
              Integrate Clinovia models into clinical studies to enhance analytics,
              validate biomarkers, and generate explainable research insights for sponsors.
            </p>
          </div>

          {/* Pharma */}
          <div className="rounded-2xl bg-white shadow-lg p-6 hover:shadow-xl transition-all duration-300">
            <h3 className="text-xl font-semibold text-green-900">Pharmaceutical Companies</h3>
            <p className="mt-4 text-green-800">
              Apply Clinovia’s AI for patient stratification, drug efficacy studies,
              and post-market safety monitoring in cardiology and neurology.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
