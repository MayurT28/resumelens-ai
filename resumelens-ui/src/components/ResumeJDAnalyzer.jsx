import { useState } from "react";

export default function ResumeJDAnalyzer() {

    const [file, setFile] = useState(null);
    const [jobDescription, setJobDescription] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);


    const handleSubmit = async (e) => {

        e.preventDefault();

        if (!file) {
            alert("Upload a resume first");
            return;
        }

        if (!jobDescription.trim()) {
            alert("Paste job description");
            return;
        }

        try {

            setLoading(true);

            const formData = new FormData();

            formData.append("file", file);
            formData.append("job_description", jobDescription);

            const response = await fetch(
                "http://127.0.0.1:8000/analyze-match/",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data = await response.json();
            console.log("MATCH RESULT FROM BACKEND:", data);
            setResult(data);

        } catch (err) {

            console.error(err);
            alert("Analysis failed");

        } finally {

            setLoading(false);

        }

    };

    const getRoleAlignmentLabel = (score) => {
        if (score === 1) return "Strong Match";
        if (score >= 0.5) return "Partial Match";
        return "Weak Match";
    };

    return (

        <div className="min-h-screen bg-slate-50 px-6 py-8">

            <h1 className="text-3xl font-bold text-indigo-600 mb-6">
                Resume + Job Description Analyzer
            </h1>


            {/* INPUT PANEL */}
            <div className="bg-white rounded-2xl shadow p-6">

                <form onSubmit={handleSubmit} className="space-y-4">

                    <input
                        type="file"
                        accept=".pdf"
                        onChange={(e) => setFile(e.target.files[0])}
                        className="w-full border rounded-lg p-2"
                    />

                    <textarea
                        rows="6"
                        placeholder="Paste job description..."
                        value={jobDescription}
                        onChange={(e) => setJobDescription(e.target.value)}
                        className="w-full border rounded-lg p-3"
                    />

                    <button
                        type="submit"
                        className="w-full bg-indigo-600 text-white py-3 rounded-xl"
                    >
                        {loading ? "Analyzing..." : "Analyze Resume Match"}
                    </button>

                </form>

            </div>


            {/* RESULTS */}
            {result && result.match_score !== undefined && (

                <div className="mt-10 bg-white rounded-2xl shadow p-6 space-y-6">

                    {/* MATCH SCORE */}
                    <div>

                        <h2 className="font-semibold mb-2">
                            Match Score
                        </h2>

                        <div className="w-full bg-gray-200 h-3 rounded-full">

                            <div
                                className="bg-indigo-600 h-3 rounded-full"
                                style={{ width: `${result.match_score}%` }}
                            />

                        </div>

                        <p className="mt-1 text-sm text-gray-600">
                            {result.match_score}%
                        </p>

                    </div>


                    {/* ROLE ALIGNMENT */}
                    <div>

                        <h2 className="font-semibold mb-2">
                            Role Alignment
                        </h2>

                        <div className="flex items-center gap-3">

                            <span className="text-sm">
                                Resume Role: <strong>{result.resume_role}</strong>
                            </span>

                            <span className="text-sm">
                                JD Role: <strong>{result.jd_role}</strong>
                            </span>

                            <span className="px-3 py-1 rounded-full text-xs bg-indigo-100 text-indigo-700 font-medium">
                                {getRoleAlignmentLabel(result.role_alignment)}
                            </span>

                        </div>

                    </div>


                    {/* MATCHED SKILLS */}
                    {result.matched_skills?.length > 0 && (

                        <div>

                            <h2 className="font-semibold mb-2">
                                Matched Skills
                            </h2>

                            <div className="flex flex-wrap gap-2">

                                {result.matched_skills.map((skill, i) => (

                                    <span
                                        key={i}
                                        className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm"
                                    >
                                        {skill}
                                    </span>

                                ))}

                            </div>

                        </div>

                    )}


                    {/* MISSING SKILLS */}
                    {result.missing_skills?.length > 0 && (

                        <div>

                            <h2 className="font-semibold mb-2">
                                Missing Skills
                            </h2>

                            <div className="flex flex-wrap gap-2">

                                {result.missing_skills.map((skill, i) => (

                                    <span
                                        key={i}
                                        className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm"
                                    >
                                        {skill}
                                    </span>

                                ))}

                            </div>

                        </div>

                    )}


                    {/* SEMANTIC SIMILARITY */}
                    {result.semantic_similarity_score !== undefined && (

                        <div>

                            <h2 className="font-semibold mb-2">
                                Semantic Similarity
                            </h2>

                            <p>
                                {(result.semantic_similarity_score * 100).toFixed(1)}%
                            </p>

                        </div>

                    )}


                    {/* SEMANTIC MATCHES */}
                    {result.semantic_skill_matches?.length > 0 && (

                        <div>

                            <h2 className="font-semibold mb-2">
                                Semantic Skill Matches
                            </h2>

                            <ul className="list-disc ml-6 text-sm">

                                {result.semantic_skill_matches.map((match, i) => (

                                    <li key={i}>
                                        <strong>{match.resume_skill.toUpperCase()}</strong>
                                        {" ↔ "}
                                        <strong>{match.jd_skill.toUpperCase()}</strong>
                                        {" "}
                                        ({(match.similarity * 100).toFixed(0)}% semantic match)
                                    </li>

                                ))}

                            </ul>

                        </div>

                    )}


                    {/* RECOMMENDED SKILLS */}
                    {result.recommended_skills?.length > 0 && (

                        <div>

                            <h2 className="font-semibold mb-2">
                                Recommended Skills to Learn
                            </h2>

                            <div className="flex flex-wrap gap-2">

                                {result.recommended_skills.map((skill, i) => (

                                    <span
                                        key={i}
                                        className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm"
                                    >
                                        {skill}
                                    </span>

                                ))}

                            </div>

                        </div>

                    )}

                </div>

            )}

        </div>

    );

}