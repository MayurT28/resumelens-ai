import { useState } from "react";
import axios from "axios";

export default function ResumeAnalyzer() {

    const [jobDescription, setJobDescription] = useState("");
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);


    const handleSubmit = async (e) => {

        e.preventDefault();

        if (!jobDescription.trim()) {
            alert("Please paste a job description");
            return;
        }

        try {

            setLoading(true);

            const response = await axios.post(
                "http://127.0.0.1:8000/rank-resumes-for-job/",
                null,
                {
                    params: {
                        job_description: jobDescription,
                    },
                }
            );

            setResults(response.data);

        } catch (error) {

            console.error("FULL ERROR:", error);
            console.error("SERVER RESPONSE:", error.response);

            alert("Error analyzing resumes — check console");

        } finally {

            setLoading(false);

        }
    };


    return (

        <div className="min-h-screen bg-slate-50 px-4 sm:px-6 lg:px-12 py-8">

            {/* Header */}
            <h1 className="text-3xl sm:text-4xl font-bold text-center mb-2 text-indigo-600">
                AI Resume Matcher
            </h1>

            <p className="text-center text-gray-600 max-w-2xl mx-auto mb-6">
                Paste a job description and ResumeLens will automatically select the most relevant
                resume from your stored candidate profiles using semantic skill matching,
                role alignment scoring, and domain intelligence.
            </p>

            <div className="bg-yellow-50 border border-yellow-300 text-yellow-800 px-4 py-3 rounded-xl text-center mb-6">
                ⚠ Upload resumes from the sidebar first to activate AI matching
            </div>


            {/* Input Card */}
            <div className="w-full mx-auto bg-white shadow-md rounded-2xl p-6 lg:p-8">

                <h2 className="text-xl font-semibold mb-4">
                    Find the Best Resume for This Job Description
                </h2>

                <form onSubmit={handleSubmit} className="space-y-4">

                    <textarea
                        rows="6"
                        value={jobDescription}
                        onChange={(e) => setJobDescription(e.target.value)}
                        className="w-full border rounded-lg p-3"
                        placeholder="Paste job description here..."
                    />

                    <button
                        type="submit"
                        className="w-full bg-indigo-600 text-white py-3 rounded-xl hover:bg-indigo-700 transition"
                    >
                        {loading ? "Analyzing..." : "Find Best Resume Match"}
                    </button>

                </form>

            </div>


            {/* RESULTS */}
            {results && results.ranked_resumes?.length > 0 && (

                <div className="mt-12 w-full max-w-6xl mx-auto space-y-8">


                    {/* TOP MATCH */}
                    <div className="bg-white shadow-xl rounded-2xl p-8 border-l-4 border-indigo-600">

                        <h2 className="text-2xl font-bold mb-2">
                            Top Resume Match
                        </h2>

                        <h3 className="text-lg font-semibold">
                            {results.ranked_resumes[0].filename}
                        </h3>

                        <p className="text-indigo-600 font-bold text-xl">
                            Score: {results.ranked_resumes[0].final_score}%
                        </p>


                        {/* SCORE BREAKDOWN */}
                        <div className="mt-4 space-y-2">

                            {Object.entries(results.ranked_resumes[0].score_breakdown)
                                .map(([label, value], index) => {

                                    const percentage = Math.round(value * 100);

                                    return (

                                        <div key={index}>

                                            <div className="flex justify-between text-sm font-medium">
                                                <span className="capitalize">
                                                    {label.replace("_", " ")}
                                                </span>

                                                <span>{percentage}%</span>
                                            </div>

                                            <div className="w-full bg-gray-200 rounded-full h-2 mt-1">

                                                <div
                                                    className="bg-indigo-600 h-2 rounded-full"
                                                    style={{ width: `${percentage}%` }}
                                                />

                                            </div>

                                        </div>

                                    );

                                })}

                        </div>


                        {/* MATCHED SKILLS */}
                        <div className="mt-4">

                            <p className="font-medium">
                                Matched Skills
                            </p>

                            <div className="flex flex-wrap gap-2 mt-2 text-xs sm:text-sm">

                                {results.ranked_resumes[0].matched_skills.map((skill, i) => (

                                    <span
                                        key={i}
                                        className="bg-green-100 text-green-700 px-3 py-1 rounded-full"
                                    >
                                        {skill}
                                    </span>

                                ))}

                            </div>

                        </div>


                        {/* MISSING SKILLS */}
                        {results.ranked_resumes[0].missing_skills.length > 0 && (

                            <div className="mt-4">

                                <p className="font-medium">
                                    Missing Skills
                                </p>

                                <div className="flex flex-wrap gap-2 mt-2">

                                    {results.ranked_resumes[0].missing_skills.map((skill, i) => (

                                        <span
                                            key={i}
                                            className="bg-red-100 text-red-700 px-3 py-1 rounded-full"
                                        >
                                            {skill}
                                        </span>

                                    ))}

                                </div>

                            </div>

                        )}


                        {/* EXPLANATION */}
                        <p className="mt-4 text-gray-700 leading-relaxed text-sm sm:text-base">
                            {results.ranked_resumes[0].ranking_explanation}
                        </p>


                        {/* EXPLANATION SOURCE */}
                        <div className="text-xs text-indigo-500 mt-2">

                            Explanation generated by:

                            {" "}

                            {results?.ranked_resumes?.[0]?.explanation_source === "llm"
                                ? "Local LLaMA model"
                                : "Rule-based engine"}

                        </div>

                    </div>



                    {/* OTHER RESUMES */}
                    {results.ranked_resumes.length > 1 && (

                        <details className="bg-white shadow-lg rounded-2xl p-6 lg:p-8">

                            <summary className="cursor-pointer text-lg font-semibold">
                                View Other Resume Comparisons
                            </summary>

                            <div className="mt-4 space-y-6">

                                {results.ranked_resumes.slice(1).map((resume, index) => (

                                    <div
                                        key={index}
                                        className="border-t pt-4"
                                    >

                                        <h3 className="font-semibold">
                                            {resume.filename}
                                        </h3>

                                        <p className="text-indigo-600 font-bold">
                                            Score: {resume.final_score}%
                                        </p>

                                        <p className="mt-2 text-gray-700">
                                            {resume.ranking_explanation}
                                        </p>

                                    </div>

                                ))}

                            </div>

                        </details>

                    )}

                </div>

            )}

        </div>

    );

}