import { useState } from "react";

export default function ProfileInsights() {

    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {

        e.preventDefault();

        if (!file) {
            alert("Upload a resume first");
            return;
        }

        try {

            setLoading(true);

            const formData = new FormData();
            formData.append("file", file);

            const response = await fetch(
                "http://127.0.0.1:8000/analyze-resume-profile/",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data = await response.json();
            setResult(data);

        } catch (error) {

            console.error(error);
            alert("Profile analysis failed");

        } finally {

            setLoading(false);

        }
    };


    return (

        <div className="max-w-4xl mx-auto">

            <h1 className="text-2xl font-bold text-indigo-600 mb-6">
                Resume Profile Insights
            </h1>


            <form
                onSubmit={handleSubmit}
                className="bg-white p-6 rounded-xl shadow space-y-4"
            >

                <input
                    type="file"
                    accept=".pdf"
                    onChange={(e) => setFile(e.target.files[0])}
                    className="w-full border p-2 rounded"
                />

                <button
                    type="submit"
                    className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700"
                >
                    {loading ? "Analyzing..." : "Analyze Resume Profile"}
                </button>

            </form>


            {result && (

                <div className="mt-8 bg-white p-6 rounded-xl shadow space-y-6">

                    {/* Primary Role */}
                    <div>
                        <strong>Primary Role:</strong>
                        <div className="text-indigo-600 font-semibold mt-1">
                            {result.primary_role}
                        </div>
                    </div>


                    {/* Secondary Roles */}
                    {result.secondary_roles?.length > 0 && (
                        <div>
                            <strong>Secondary Roles:</strong>
                            <div className="flex flex-wrap gap-2 mt-2">
                                {result.secondary_roles.map((role, i) => (
                                    <span
                                        key={i}
                                        className="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm"
                                    >
                                        {role}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}


                    {/* Strong Domains */}
                    {result.strong_domains?.length > 0 && (
                        <div>
                            <strong>Strong Domains:</strong>
                            <div className="flex flex-wrap gap-2 mt-2">
                                {result.strong_domains.map((domain, i) => (
                                    <span
                                        key={i}
                                        className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm"
                                    >
                                        {domain}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}


                    {/* Weak Domains */}
                    {result.weak_domains?.length > 0 && (
                        <div>
                            <strong>Weak Domains:</strong>
                            <div className="flex flex-wrap gap-2 mt-2">
                                {result.weak_domains.map((domain, i) => (
                                    <span
                                        key={i}
                                        className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm"
                                    >
                                        {domain}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}


                    {/* Growth Roles */}
                    {result.recommended_growth_roles?.length > 0 && (
                        <div>
                            <strong>Recommended Growth Roles:</strong>
                            <div className="flex flex-wrap gap-2 mt-2">
                                {result.recommended_growth_roles.map((role, i) => (
                                    <span
                                        key={i}
                                        className="bg-yellow-100 text-yellow-700 px-3 py-1 rounded-full text-sm"
                                    >
                                        {role}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}


                    {/* Skill Upgrades */}
                    {result.recommended_skill_upgrades?.length > 0 && (
                        <div>
                            <strong>Skill Upgrades:</strong>
                            <div className="flex flex-wrap gap-2 mt-2">
                                {result.recommended_skill_upgrades.map((skill, i) => (
                                    <span
                                        key={i}
                                        className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm"
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