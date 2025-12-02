// frntend/app/(public)/page.tsx

import Hero from "./home-sections/Hero";
import Cardiology from "./home-sections/Cardiology";
import Neurology from "./home-sections/Neurology";
import Papers from "./home-sections/Papers";
import Who_Benefit from "./home-sections/Who_Benefit";

export default function HomePage() {
  return (
    <main className="w-full">
      <Hero />
      <Cardiology />
      <Neurology />
      <Papers />
      <Who_Benefit />
    </main>
  );
}
