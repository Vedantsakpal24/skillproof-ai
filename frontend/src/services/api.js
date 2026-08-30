const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export const uploadResume = async (file) => {
    const formData = new FormData();
    formData.append("file", file);
    
    const response = await fetch(`${API_URL}/resume/upload`, {
        method: "POST",
        body: formData,
    });
    return response.json();
};

export const submitManualSkills = async (skills) => {
    const response = await fetch(`${API_URL}/skills/manual`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ skills }),
    });
    return response.json();
};

export const getVerifiedSkills = async (userId) => {
    const response = await fetch(`${API_URL}/skills/verified/${userId}`);
    return response.json();
};

export const setTargetRole = async (userId, role) => {
    const response = await fetch(`${API_URL}/skills/target-role/${userId}?target_role=${encodeURIComponent(role)}`, {
        method: "POST",
    });
    return response.json();
};

export const startVerification = async (userId, skillName) => {
    const response = await fetch(`${API_URL}/verifications/start/${userId}/${encodeURIComponent(skillName)}`, {
        method: "POST",
    });
    return response.json();
};

export const submitQuizAnswer = async (sessionId, questionId, selectedOption) => {
    const response = await fetch(`${API_URL}/verifications/quiz/${sessionId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question_id: questionId, selected_option: selectedOption }),
    });
    return response.json();
};

export const submitCode = async (sessionId, code, taskId = null) => {
    const response = await fetch(`${API_URL}/verifications/code/${sessionId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, task_id: taskId }),
    });
    return response.json();
};

export const submitDebug = async (sessionId, code, taskId = null) => {
    const response = await fetch(`${API_URL}/verifications/debug/${sessionId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, task_id: taskId }),
    });
    return response.json();
};

export const getMarketMatch = async (userId) => {
    const response = await fetch(`${API_URL}/market/match/${userId}`);
    return response.json();
};

export const getMarketDemand = async (userId) => {
    const response = await fetch(`${API_URL}/market/demand/${userId}`);
    return response.json();
};

export const getBestNextSkill = async (userId) => {
    const response = await fetch(`${API_URL}/recommendations/best-next-skill/${userId}`);
    return response.json();
};

export const getPersonalizedDashboard = async (userId) => {
    const response = await fetch(`${API_URL}/dashboard/${userId}`);
    if (!response.ok) throw new Error("Failed to fetch dashboard");
    return response.json();
};

export const simulateOpportunity = async (userId, skillName) => {
    const response = await fetch(`${API_URL}/recommendations/simulate/${userId}?skill_name=${encodeURIComponent(skillName)}`, {
        method: "POST"
    });
    return response.json();
};

export const loadDemoProfile = async () => {
    const response = await fetch(`${API_URL}/demo/load`, {
        method: "POST"
    });
    return response.json();
};
