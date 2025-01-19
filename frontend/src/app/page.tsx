"use client";
import { ArrowRight, FileText, Zap, Target } from "lucide-react";

import { redirect } from "next/navigation";

export default function WelcomePage() {
  const goToDashboard = () => {
    redirect("/dashboard");
  };
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <header className="container mx-auto px-4 py-8">
        <nav className="flex items-center justify-between">
          <div className="text-2xl font-bold text-gray-800">WorkBringer</div>
          <div className="space-x-4">
            <button>Login</button>
            <button>Sign Up</button>
          </div>
        </nav>
      </header>

      <main className="container mx-auto px-4 py-16">
        <section className="mb-16 text-center">
          <h1 className="mb-6 text-4xl font-bold text-gray-900 md:text-6xl">
            Tailor your resume without AI content
          </h1>
          <p className="mx-auto mb-8 max-w-2xl text-xl text-gray-600">
            Journey before destination, innovation before application.
          </p>
          <div className="flex flex-col items-center justify-center space-y-4 sm:flex-row sm:space-x-4 sm:space-y-0"></div>
        </section>

        <section className="mb-16 grid gap-8 md:grid-cols-3">
          {[
            {
              icon: <FileText className="h-10 w-10 text-blue-500" />,
              title: "Smart Resume Analysis",
              description:
                "Our AI analyzes your resume and suggests improvements based on industry standards.",
            },
            {
              icon: <Zap className="h-10 w-10 text-yellow-500" />,
              title: "Instant Tailoring",
              description:
                "Quickly adapt your resume to match specific job descriptions and increase your chances.",
            },
            {
              icon: <Target className="h-10 w-10 text-green-500" />,
              title: "ATS-Friendly Formats",
              description:
                "Ensure your resume passes through Applicant Tracking Systems with our optimized formats.",
            },
          ].map((feature, index) => (
            <div
              key={index}
              className="rounded-lg bg-white p-6 text-center shadow-lg"
            >
              <div className="mb-4 inline-block">{feature.icon}</div>
              <h3 className="mb-2 text-xl font-semibold">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </section>

        <section className="rounded-xl bg-blue-50 py-16 text-center">
          <h2 className="mb-4 text-3xl font-bold text-gray-900">
            Ready to Boost Your Career?
          </h2>
          <p className="mx-auto mb-8 max-w-2xl text-xl text-gray-600">
            Join thousands of job seekers who have successfully landed their
            dream jobs using ResumeTailor.
          </p>

          <button
            className="inline-flex items-center rounded-lg bg-blue-600 px-6 py-3 text-white hover:bg-blue-700"
            onClick={goToDashboard}
          >
            Start Tailoring Now
            <ArrowRight className="ml-2 h-5 w-5" />
          </button>
        </section>
      </main>

      <footer className="container mx-auto mt-16 border-t border-gray-200 px-4 py-8">
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-600">
            © {new Date().getFullYear()} WorkBringer. All rights reserved.
          </div>
          <div className="space-x-4">
            <a href="#" className="text-sm text-gray-600 hover:text-gray-900">
              Privacy Policy
            </a>
            <a href="#" className="text-sm text-gray-600 hover:text-gray-900">
              Terms of Service
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
