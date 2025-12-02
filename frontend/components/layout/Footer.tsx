// components/Footer.tsx
export default function Footer() {
  return (
    <footer className="py-10 px-6 bg-white border-t w-full text-center mt-20">
      <p className="text-gray-600">
        © {new Date().getFullYear()} Clinovia Inc. All rights reserved.
      </p>
      <p className="mt-2 text-sm text-gray-500">
        Contact us: <a href="mailto:contact@clinovia.ai" className="underline">contact@clinovia.ai</a>
      </p>
    </footer>
  );
}
