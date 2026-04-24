import { useState } from "react";

export default function ResumeIntelligence() {

    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);

    const [roleData, setRoleData] = useState(null);
    const [trajectoryData, setTrajectoryData] = useState(null);
    const [profileData, setProfileData] = useState(null);


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

            // Run all endpoints in parallel
            const [roleRes, trajectoryRes, profileRes] =
                await Promise.all([
                    fetch("http://127.0.0.1:8000/classify-role/", {
                        method: "POST",
                        body: formData
                    }),
                    fetch("http://127.0.0.1:8000/career-trajectory/", {
                        method: "POST",
                        body: formData
                    }),
                    fetch("http://127.0.0.1:8000/analyze-resume-profile/", {
                        method: "POST",
                        body: formData
                    })
                ]);

            const roleJson = await roleRes.json();
            const trajectoryJson = await trajectoryRes.json();
            const profileJson = await profileRes.json();

            setRoleData(roleJson);
            setTrajectoryData(trajectoryJson);
            setProfileData(profileJson);

        } catch (err) {

            console.error(err);
            alert("Resume intelligence failed");

        } finally {

            setLoading(false);

        }
    };


    return (

        <div className="max-w-6xl mx-auto">

            <h1 className="text-2xl font-bold text-indigo-600 mb-6">
                Resume Intelligence Report
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
                    {loading ? "Analyzing..." : "Generate Intelligence Report"}
                </button>

            </form>


            {(roleData || trajectoryData || profileData) && (

                <div className="mt-8 space-y-6">

                    {/* PRIMARY ROLE */}
                    {roleData?.primary_role && (
                        <div className="bg-white p-6 rounded-xl shadow">
                            <strong>Primary Role:</strong>
                            <div className="text-indigo-600 font-semibold mt-1">
                                {roleData.primary_role}
                            </div>
                        </div>
                    )}


                    {/* SECONDARY ROLES */}
                    {roleData?.secondary_roles?.length > 0 && (
                        <div className="bg-white p-6 rounded-xl shadow">
                            <strong>Secondary Roles:</strong>
                            <div className="flex flex-wrap gap-2 mt-2">
                                {roleData.secondary_roles.map((r, i) => (
                                    <span
                                        key={i}
                                        className="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm"
                                    >
                                        {r}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}


                    {/* NEXT ROLES */}
                    {trajectoryData?.next_roles?.length > 0 && (
                        <div className="bg-white p-6 rounded-xl shadow">
                            <strong>Next Career Roles:</strong>
                            <div className="flex flex-wrap gap-2 mt-2">
                                {trajectoryData.next_roles.map((r, i) => (
                                    <span
                                        key={i}
                                        className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm"
                                    >
                                        {r}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}


                    {/* ADJACENT ROLES */}
                    {trajectoryData?.adjacent_roles?.length > 0 && (
                        <div className="bg-white p-6 rounded-xl shadow">
                            <strong>Adjacent Roles:</strong>
                            <div className="flex flex-wrap gap-2 mt-2">
                                {trajectoryData.adjacent_roles.map((r, i) => (
                                    <span
                                        key={i}
                                        className="bg-yellow-100 text-yellow-700 px-3 py-1 rounded-full text-sm"
                                    >
                                        {r}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}


                    {/* LONG TERM ROLES */}
                    {trajectoryData?.long_term_roles?.length > 0 && (
                        <div className="bg-white p-6 rounded-xl shadow">
                            <strong>Long-Term Roles:</strong>
                            <div className="flex flex-wrap gap-2 mt-2">
                                {trajectoryData.long_term_roles.map((r, i) => (
                                    <span
                                        key={i}
                                        className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm"
                                    >
                                        {r}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}


                    {/* STRONG DOMAINS */}
                    {profileData?.strong_domains?.length > 0 && (
                        <div className="bg-white p-6 rounded-xl shadow">
                            <strong>Strong Domains:</strong>
                            <div className="flex flex-wrap gap-2 mt-2">
                                {profileData.strong_domains.map((d, i) => (
                                    <span
                                        key={i}
                                        className="bg-green-100 text-green-700 px-3 py-1 rounded-full text-sm"
                                    >
                                        {d}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}


                    {/* WEAK DOMAINS */}
                    {profileData?.weak_domains?.length > 0 && (
                        <div className="bg-white p-6 rounded-xl shadow">
                            <strong>Weak Domains:</strong>
                            <div className="flex flex-wrap gap-2 mt-2">
                                {profileData.weak_domains.map((d, i) => (
                                    <span
                                        key={i}
                                        className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm"
                                    >
                                        {d}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}


                    {/* SKILL UPGRADES */}
                    {profileData?.recommended_skill_upgrades?.length > 0 && (
                        <div className="bg-white p-6 rounded-xl shadow">
                            <strong>Recommended Skill Upgrades:</strong>
                            <div className="flex flex-wrap gap-2 mt-2">
                                {profileData.recommended_skill_upgrades.map((s, i) => (
                                    <span
                                        key={i}
                                        className="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-sm"
                                    >
                                        {s}
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