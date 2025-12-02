"use client";

import Link from "next/link";

const sidebar = [
  {
    title: "Cardiology",
    href: "/protected/cardiology",
    items: [
      { title: "ASCVD", href: "/protected/cardiology/ascvd" },
      { title: "Blood Pressure Categorization", href: "/protected/cardiology/bp-category" },
      { title: "Cha2ds2vasc", href: "/protected/cardiology/cha2ds2vasc" },
      { title: "ECG Interpreter", href: "/protected/cardiology/ecg-interpreter" },
      { title: "Echonet EF Prediction", href: "/protected/cardiology/ejection-fraction" },
    ],
  },
  {
    title: "Neurology / Alzheimer",
    href: "/protected/alzheimer",
    items: [
      { title: "Risk Screener", href: "/protected/alzheimer/riskScreener" },
      {
        title: "Diagnosis",
        children: [
          { title: "Screening", href: "/protected/alzheimer/diagnosisScreening" },
          { title: "Basic Features", href: "/protected/alzheimer/diagnosisBasic" },
          { title: "Extended Features", href: "/protected/alzheimer/diagnosisExtended" },
        ],
      },
      {
        title: "Prognosis (2yr)",
        children: [
          { title: "Basic Features", href: "/protected/alzheimer/prognosis2yrBasic" },
          { title: "Extended Features", href: "/protected/alzheimer/prognosis2yrExtended" },
        ],
      },
    ],
  },
];

export default function Sidebar() {
  return (
    <aside className="w-64 h-screen p-4 border-r bg-white">
      <nav className="space-y-6">
        {sidebar.map((section) => (
          <div key={section.title}>
            {/* MAKE THE SECTION TITLE CLICKABLE */}
            <Link
              href={section.href}
              className="font-semibold text-lg mb-2 block hover:underline"
            >
              {section.title}
            </Link>

            <ul className="ml-2 space-y-1">
              {section.items.map((item) =>
                item.children ? (
                  <li key={item.title}>
                    <span className="font-medium">{item.title}</span>
                    <ul className="ml-4 mt-1 space-y-1">
                      {item.children.map((child) => (
                        <li key={child.title}>
                          <Link
                            href={child.href}
                            className="text-blue-600 hover:underline text-sm"
                          >
                            {child.title}
                          </Link>
                        </li>
                      ))}
                    </ul>
                  </li>
                ) : (
                  <li key={item.title}>
                    <Link
                      href={item.href}
                      className="text-blue-600 hover:underline"
                    >
                      {item.title}
                    </Link>
                  </li>
                )
              )}
            </ul>
          </div>
        ))}
      </nav>
    </aside>
  );
}
