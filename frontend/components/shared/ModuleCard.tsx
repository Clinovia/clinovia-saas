// components/ModuleCard.tsx
"use client";

import React from "react";

type ModuleCardProps = {
  name: string;
  description: string;
  inputs: string[];
  outputs: string[];
  href: string;
};

export default function ModuleCard({ name, description, inputs, outputs, href }: ModuleCardProps) {
  return (
    <a href={href} className="block border rounded-lg p-4 shadow hover:shadow-lg transition">
      <h3 className="text-lg font-semibold mb-2">{name}</h3>
      <p className="text-sm mb-2">{description}</p>
      <div className="mb-2">
        <strong>Inputs:</strong>
        <ul className="list-disc list-inside text-sm">
          {inputs.map((input) => (
            <li key={input}>{input}</li>
          ))}
        </ul>
      </div>
      <div>
        <strong>Outputs:</strong>
        <ul className="list-disc list-inside text-sm">
          {outputs.map((output) => (
            <li key={output}>{output}</li>
          ))}
        </ul>
      </div>
    </a>
  );
}
