import React, { useEffect, useState } from "react";
import ResumeAnalyzer from "./ResumeAnalyzer";
import RoleClassifier from "./RoleClassifier";
import CareerTrajectory from "./CareerTrajectory";
import ProfileInsights from "./ProfileInsights";
import ResumeIntelligence from "./ResumeIntelligence";
import ResumeJDAnalyzer from "./ResumeJDAnalyzer";

export default function Layout({ children }) {
    const [storedResumes, setStoredResumes] = useState([]);
    const [open, setOpen] = useState(true);
    const [activePage, setActivePage] = useState("matcher");

    useEffect(() => {
        fetch("http://localhost:8000/list-resumes/")
            .then((res) => res.json())
            .then((data) => {
                setStoredResumes(data.resumes);
            })
            .catch((err) => {
                console.error("Failed loading resumes:", err);
            });
    }, []);

    return (
        <div className="flex min-h-screen bg-slate-50">

            {/* SIDEBAR */}
            <aside
                className={`${open ? "w-64" : "w-16"
                    } transition-all duration-300 bg-white shadow-md flex flex-col`}
            >
                <div className="p-4 font-bold text-indigo-600 text-lg">
                    ResumeLens
                </div>

                <nav className="flex flex-col gap-2 px-3">

                    <button
                        onClick={() => setActivePage("matcher")}
                        className="text-left px-3 py-2 rounded-lg hover:bg-indigo-50"
                    >
                        Analyze Resume
                    </button>

                    <button
                        onClick={() => setActivePage("intelligence")}
                        className="text-left px-3 py-2 rounded-lg hover:bg-indigo-50"
                    >
                        Resume Intelligence Report
                    </button>

                    <button
                        onClick={() => setActivePage("resumeMatch")}
                        className="text-left px-3 py-2 rounded-lg hover:bg-indigo-50"
                    >
                        Resume + JD Analyzer
                    </button>

                    <input
                        type="file"
                        accept=".pdf"
                        onChange={async (e) => {
                            const file = e.target.files[0];
                            if (!file) return;

                            const formData = new FormData();
                            formData.append("file", file);

                            const response = await fetch(
                                "http://localhost:8000/upload-resume/",
                                {
                                    method: "POST",
                                    body: formData,
                                }
                            );

                            if (response.ok) {

                                alert("Resume uploaded successfully!");

                                // refresh sidebar resume list
                                fetch("http://localhost:8000/list-resumes/")
                                    .then((res) => res.json())
                                    .then((data) => {
                                        setStoredResumes(data.resumes);
                                    });

                            } else {

                                alert("Upload failed");

                            }
                        }}
                        className="hidden"
                        id="resumeUpload"
                    />

                    <label
                        htmlFor="resumeUpload"
                        className="cursor-pointer text-left px-3 py-2 rounded-lg hover:bg-indigo-50"
                    >
                        Upload Resume
                    </label>

                    <h2 className="text-sm font-semibold mt-6 mb-3 text-gray-500">
                        Stored Resumes
                    </h2>

                    <div className="flex flex-col gap-2">

                        {storedResumes.map((resume, index) => (

                            <div
                                key={index}
                                className="p-2 rounded-lg hover:bg-indigo-50 cursor-pointer"
                            >
                                <div
                                    className="text-sm font-medium truncate"
                                    title={resume.filename}
                                >
                                    {resume.filename}
                                </div>

                                <div
                                    className="text-xs text-gray-500 truncate"
                                    title={resume.predicted_role}
                                >
                                    {resume.predicted_role}
                                </div>
                            </div>

                        ))}

                    </div>

                </nav>

                <div className="mt-auto p-3">
                    <button
                        onClick={() => setOpen(!open)}
                        className="text-sm text-gray-500"
                    >
                        Toggle
                    </button>
                </div>
            </aside>


            {/* MAIN CONTENT */}
            <main className="flex-1 px-6 py-8">

                {activePage === "matcher" && <ResumeAnalyzer />}

                {activePage === "intelligence" && <ResumeIntelligence />}

                {activePage === "resumeMatch" && <ResumeJDAnalyzer />}

            </main>

        </div>
    );
}
