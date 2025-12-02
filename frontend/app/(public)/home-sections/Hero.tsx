import Image from "next/image";
import Link from "next/link";

export default function Hero() {
  return (
    <section className="relative w-full h-screen">
      {/* Background image */}
      <div className="absolute inset-0">
        <Image
          src="/images/ai_doctor.png"
          alt="AI Doctor"
          fill
          className="object-cover"
          priority
        />
        <div className="absolute inset-0 bg-black/50"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center justify-center h-full px-6 animate-fadeIn text-center">
        <div className="mt-20 md:mt-32 max-w-3xl">
          <h1 className="text-5xl md:text-6xl font-bold text-white leading-tight drop-shadow-lg">
            Transforming Healthcare with AI
          </h1>

          <p className="mt-6 text-lg md:text-xl text-gray-200 leading-relaxed text-center">
            Accelerate diagnosis, improve patient outcomes, and empower clinicians 
            with AI-driven insights for cardiology and neurology — built on real-world data.
          </p>

          {/* Call-to-action button → updated link */}
          <Link
            href="/explore"
            className="mt-10 inline-block bg-green-800 hover:bg-[#1B4D3E] text-white font-semibold px-8 py-3 rounded-full text-lg shadow-lg transition-transform hover:scale-105"
          >
            Start Free Trial
          </Link>
        </div>

        {/* Disclaimer at bottom */}
        <p className="absolute bottom-6 text-sm text-gray-300">
          *Our AI tools are for research use only and not approved for clinical diagnosis.
        </p>
      </div>
    </section>
  );
}
