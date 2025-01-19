"use client";
import React, { useState, useEffect } from "react";
import { redirect } from "next/navigation";
import { set } from "zod";

export default function ResumeGenerator() {
  const [pdfName, setPdfName] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [statusMessage, setStatusMessage] = useState("");

  const handlePdfNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPdfName(e.target.value);
  };

  const handleJobDescriptionChange = (
    e: React.ChangeEvent<HTMLTextAreaElement>,
  ) => {
    setJobDescription(e.target.value);
  };
  const onGenRequest = async () => {
    if (!pdfName || !jobDescription) {
      setStatusMessage("Please fill in all fields");
      return;
    }
    setStatusMessage("Generating resume...");
    const response = await fetch("/generate", {
      method: "post",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        filename: pdfName,
        jobinfo: jobDescription,
      }),
    });
    const blurb = await response.blob();
    const url = URL.createObjectURL(blurb);
    const a = document.createElement("a");
    const contentDisposition = response.headers.get("Content-Disposition");
    const filenameMatch = contentDisposition?.match(/filename="(.+)"/);
    const filename = filenameMatch ? filenameMatch[1] : "default.pdf";
    a.href = url;
    a.download = filename || "default.pdf"; // Use the filename from the backend
    document.body.appendChild(a);
    a.click();
      document.body.removeChild(a);
      setStatusMessage("Resume generated successfully!");
  };
  

  const goToDash = () => {
    redirect("/dashboard");
  };
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-400 via-pink-500 to-red-500 px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-4 flex justify-end">
        <button
          onClick={goToDash}
          className="transform rounded-md bg-gradient-to-r from-purple-600 to-pink-600 px-4 py-2 font-semibold text-white transition duration-300 ease-in-out hover:-translate-y-1 hover:scale-105 hover:from-purple-700 hover:to-pink-700"
        >
          Return to Hub
        </button>
      </div>
      <div className="absolute left-4 top-4"></div>
      <div className="mx-auto max-w-3xl">
        <div className="rounded-lg bg-white/90 shadow-xl backdrop-blur-sm">
          <div className="space-y-1 rounded-lg p-6 sm:p-10">
            <div className="flex justify-center">
              <div className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-center text-3xl font-bold text-transparent">
                Resume Auto-Generator
              </div>
            </div>
            <div className="max-w-3/4 mx-auto break-words text-center text-gray-600">
              <div>
                You will spend a lot of time here bash applying, so we made it
                pink!``
              </div>
            </div>
          </div>
          <div className="flex w-full items-center justify-center rounded-lg bg-white p-4 shadow-md">
            <form className="w-full space-y-6">
              <div>
                <label
                  htmlFor="pdfName"
                  className="block bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-sm font-medium text-gray-700 text-transparent"
                >
                  PDF Name
                </label>
                <input
                  type="text"
                  id="pdfName"
                  name="pdfName"
                  placeholder="Enter the name for your PDF, .pdf is not needed"
                  onChange={handlePdfNameChange}
                  className="mt-1 w-full rounded-md border border-gray-300 focus:border-pink-500 focus:ring-pink-500"
                />
              </div>
              <div>
                <label
                  htmlFor="jobDescription"
                  className="block bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-sm font-medium text-gray-700 text-transparent"
                >
                  Job Description
                </label>
                <textarea
                  id="jobDescription"
                  name="jobDescription"
                  rows={10}
                  placeholder="Yes, it is this simple: paste it in and click generate!"
                  onChange={handleJobDescriptionChange}
                  className="mt-1 w-full rounded-md border border-gray-300 focus:border-pink-500 focus:ring-pink-500"
                />
              </div>
            </form>
          </div>
          <div className="p-4">
            <button
              className="w-full transform rounded-md bg-gradient-to-r from-purple-600 to-pink-600 px-4 py-2 font-semibold text-white transition duration-300 ease-in-out hover:-translate-y-1 hover:scale-105 hover:from-purple-700 hover:to-pink-700"
              onClick={onGenRequest}
            >
              Generate Resume
            </button>
          </div>
          <div className="p-4">
            <div>
              <label
                htmlFor="statusMessage"
                className="block bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-sm font-medium text-gray-700 text-transparent"
              >
                Status Message
              </label>
              <textarea
                id="statusMessage"
                name="statusMessage"
                rows={3}
                readOnly
                value={statusMessage}
                className="mt-1 w-full rounded-md border border-gray-300 focus:border-pink-500 focus:ring-pink-500"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
