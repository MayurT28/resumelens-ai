import { useState } from "react";

export default function RoleClassifier() {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!file) {
            alert("Please upload a resume");
            return;
        }

        try {
            setLoading(true);

            const formData = new FormData();
            formData.append("file", file);

            const response = await fetch(
                "http://127.0.0.1:8000/classify-role/",
                {
                    method: "POST",
                    body: formData,
                }
            );

            const data = await response.json();
            setResult(data);

        } catch (error) {
            console.error(error);
            alert("Error analyzing role");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto">

            <h1 className="text-2xl font-bold text-indigo-600 mb-6">
                Resume Role Intelligence
            </h1>

            {/* Upload */}
            <form onSubmit={handleSubmit} className="bg-white p-6 rounded-xl shadow space-y-4">

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
                    {loading ? "Analyzing..." : "Analyze Role"}
                </button>

            </form>

            {/* Results */}
            {result && (
                <div className="mt-8 bg-white p-6 rounded-xl shadow">

                    <h2 className="text-xl font-semibold mb-4">
                        Role Prediction
                    </h2>

                    <p className="mb-2">
                        <strong>Primary Role:</strong> {result.primary_role}
                    </p>

                    {result.secondary_roles?.length > 0 && (
                        <div className="mb-4">
                            <strong>Secondary Roles:</strong>
                            <ul className="list-disc ml-6">
                                {result.secondary_roles.map((role, i) => (
                                    <li key={i}>{role}</li>
                                ))}
                            </ul>
                        </div>
                    )}

                    {result.recommended_skills_for_role?.length > 0 && (
                        <div>
                            <strong>Recommended Skills:</strong>
                            <div className="flex flex-wrap gap-2 mt-2">
                                {result.recommended_skills_for_role.map((skill, i) => (
                                    <span
                                        key={i}
                                        className="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm"
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