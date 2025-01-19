
import { ArrowRight, FileText, Zap, Target } from 'lucide-react'

export default function WelcomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <header className="container mx-auto px-4 py-8">
        <nav className="flex justify-between items-center">
          <div className="text-2xl font-bold text-gray-800">ResumeTailor</div>
          <div className="space-x-4">
            <button variant="ghost">Login</button>
            <button>Sign Up</button>
          </div>
        </nav>
      </header>

      <main className="container mx-auto px-4 py-16">
        <section className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Craft Your Perfect Resume
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Tailor your resume to any job description in minutes. Stand out and land your dream job faster.
          </p>
          <div className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-4">
            <input 
              type="email" 
              placeholder="Enter your email" 
              className="max-w-xs"
            />
            <button size="lg">
              Get Started
              <ArrowRight className="ml-2 h-5 w-5" />
            </button>
          </div>
        </section>

        <section className="grid md:grid-cols-3 gap-8 mb-16">
          {[
            {
              icon: <FileText className="h-10 w-10 text-blue-500" />,
              title: "Smart Resume Analysis",
              description: "Our AI analyzes your resume and suggests improvements based on industry standards."
            },
            {
              icon: <Zap className="h-10 w-10 text-yellow-500" />,
              title: "Instant Tailoring",
              description: "Quickly adapt your resume to match specific job descriptions and increase your chances."
            },
            {
              icon: <Target className="h-10 w-10 text-green-500" />,
              title: "ATS-Friendly Formats",
              description: "Ensure your resume passes through Applicant Tracking Systems with our optimized formats."
            }
          ].map((feature, index) => (
            <div key={index} className="bg-white p-6 rounded-lg shadow-lg text-center">
              <div className="inline-block mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </section>

        <section className="text-center bg-blue-50 py-16 rounded-xl">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Ready to Boost Your Career?
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Join thousands of job seekers who have successfully landed their dream jobs using ResumeTailor.
          </p>
          <button size="lg">
            Start Tailoring Now
            <ArrowRight className="ml-2 h-5 w-5" />
          </button>
        </section>
      </main>

      <footer className="container mx-auto px-4 py-8 mt-16 border-t border-gray-200">
        <div className="flex justify-between items-center">
          <div className="text-sm text-gray-600">
            © {new Date().getFullYear()} ResumeTailor. All rights reserved.
          </div>
          <div className="space-x-4">
            <a href="#" className="text-sm text-gray-600 hover:text-gray-900">Privacy Policy</a>
            <a href="#" className="text-sm text-gray-600 hover:text-gray-900">Terms of Service</a>
          </div>
        </div>
      </footer>
    </div>
  )
}

