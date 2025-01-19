"use client";
import { FileText, Edit, ArrowRight } from "lucide-react";
import { redirect } from "next/navigation";

export default function Dashboard() {
  const goToGen = () => {
    redirect("/resume/generate");
  };
  const goToBuild = () => {
    redirect("/resume/build");
  };
  const goHome = () => {
    redirect("/");
  };
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <header className="container mx-auto px-4 py-8">
        <nav className="flex items-center justify-between">
          <button
            className="text-2xl font-bold text-gray-800 hover:text-gray-900"
            onClick={goHome}
          >
            WorkBringer
          </button>
          <div className="space-x-4">
            <button>Dashboard</button>
            <button>Profile</button>
            <button>Logout</button>
          </div>
        </nav>
      </header>

      <main className="container mx-auto px-4 py-16">
        <h1 className="mb-8 text-center text-3xl font-bold text-gray-900 md:text-4xl">
          WorkBringer Hub: Home to all your resume needs
        </h1>

        <div className="mb-16 grid gap-8 md:grid-cols-2">
          <div className="space-y-6">
            <button
              className="h-32 w-full rounded-lg bg-orange-200 text-xl font-semibold hover:bg-orange-300"
              onClick={goToGen}
            >
              <FileText className="mr-4 h-8 w-8" />
              Generate New Resume
              <ArrowRight className="ml-4 h-6 w-6" />
            </button>
            <div className="rounded-lg bg-white p-6 shadow-lg">
              <h2 className="mb-4 text-xl font-semibold">Generate Resumes</h2>
              <p className="text-gray-600">
                Start building best resumes for that 500 jobs you've always
                wanted. Throw in the job description and let us cook. We will
                make sure your resume is not seen nor rewritten by AI
              </p>
              <ul className="mt-4 space-y-2">
                <li className="flex items-center text-gray-600">
                  <ArrowRight className="mr-2 h-4 w-4 text-blue-500" />
                  Input your professional details
                </li>
                <li className="flex items-center text-gray-600">
                  <ArrowRight className="mr-2 h-4 w-4 text-blue-500" />
                  Select your target job or industry
                </li>
                <li className="flex items-center text-gray-600">
                  <ArrowRight className="mr-2 h-4 w-4 text-blue-500" />
                  Receive a tailored, ATS-friendly resume
                </li>
              </ul>
            </div>
          </div>

          <div className="space-y-6">
            <button
              className="h-32 w-full rounded-lg bg-cyan-200 text-xl font-semibold hover:bg-cyan-300"
              onClick={goToBuild}
            >
              <Edit className="mr-4 h-8 w-8" />
              Edit Existing Resume
              <ArrowRight className="ml-4 h-6 w-6" />
            </button>
            <div className="rounded-lg bg-white p-6 shadow-lg">
              <h2 className="mb-4 text-xl font-semibold">Edit Your Resume</h2>
              <p className="text-gray-600">
                Refine and update your existing resume to match new job
                opportunities. Our smart editing tools will help you optimize
                your content for maximum impact.
              </p>
              <ul className="mt-4 space-y-2">
                <li className="flex items-center text-gray-600">
                  <ArrowRight className="mr-2 h-4 w-4 text-blue-500" />
                  Upload your current resume
                </li>
                <li className="flex items-center text-gray-600">
                  <ArrowRight className="mr-2 h-4 w-4 text-blue-500" />
                  Receive suggestions for improvement
                </li>
                <li className="flex items-center text-gray-600">
                  <ArrowRight className="mr-2 h-4 w-4 text-blue-500" />
                  Tailor your resume to specific job listings
                </li>
              </ul>
            </div>
          </div>
        </div>

        <section className="rounded-xl bg-blue-50 py-12 text-center">
          <h2 className="mb-4 text-2xl font-bold text-gray-900">
            Need Help Getting Started?
          </h2>
          <p className="mx-auto mb-6 max-w-2xl text-lg text-gray-600">
            Check out our help page for details on how to best use the app
          </p>
          <button>
            Help Page
            <ArrowRight className="ml-2 h-5 w-5" />
          </button>
        </section>
      </main>

      <footer className="container mx-auto mt-16 border-t border-gray-200 px-4 py-8">
        <div className="flex flex-col items-center justify-between md:flex-row">
          <div className="mb-4 text-sm text-gray-600 md:mb-0">
            © {new Date().getFullYear()} WorkBringer. All rights reserved. Hoid was here
          </div>
          <div className="space-x-4">
            <a href="#" className="text-sm text-gray-600 hover:text-gray-900">
              Privacy Policy
            </a>
            <a href="#" className="text-sm text-gray-600 hover:text-gray-900">
              Terms of Service
            </a>
            <a href="#" className="text-sm text-gray-600 hover:text-gray-900">
              Contact Support
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
