import { useState } from "react";

export default function CareerTrajectory() {

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
                "http://127.0.0.1:8000/career-trajectory/",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data = await response.json();
            setResult(data);

        } catch (error) {
            console.error(error);
            alert("Career prediction failed");
        }
        finally {
            setLoading(false);
        }
    };

    return (

        <div className="max-w-4xl mx-auto">

            <h1 className="text-2xl font-bold text-indigo-600 mb-6">
                Career Trajectory Prediction
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
                    {loading ? "Analyzing..." : "Predict Career Path"}
                </button>

            </form>


            {result && (

                <div className="mt-8 bg-white p-6 rounded-xl shadow space-y-6">

                    <div>
                        <strong>Current Role:</strong>
                        <div className="text-indigo-600 font-semibold mt-1">
                            {result.current_role}
                        </div>
                    </div>


                    <div>
                        <strong>Next Recommended Roles:</strong>
                        <div className="flex flex-wrap gap-2 mt-2">
                            {result.next_roles?.map((role, i) => (
                                <span
                                    key={i}
                                    className="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm"
                                >
                                    {role}
                                </span>
                            ))}
                        </div>
                    </div>


                    <div>
                        <strong>Adjacent Roles:</strong>
                        <div className="flex flex-wrap gap-2 mt-2">
                            {result.adjacent_roles?.map((role, i) => (
                                <span
                                    key={i}
                                    className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm"
                                >
                                    {role}
                                </span>
                            ))}
                        </div>
                    </div>


                    <div>
                        <strong>Long-Term Roles:</strong>
                        <div className="flex flex-wrap gap-2 mt-2">
                            {result.long_term_roles?.map((role, i) => (
                                <span
                                    key={i}
                                    className="bg-yellow-100 text-yellow-700 px-3 py-1 rounded-full text-sm"
                                >
                                    {role}
                                </span>
                            ))}
                        </div>
                    </div>

                </div>

            )}

        </div>
    );
}