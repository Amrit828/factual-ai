const API_BASE_URL = 'http://localhost:8000/api';

export const verifyArticle = async (text) => {
    try {
        const response = await fetch(`${API_BASE_URL}/verify_article`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Error verifying article:", error);
        throw error;
    }
};

export const verifyClaim = async (claimText) => {
    try {
        const response = await fetch(`${API_BASE_URL}/verify_claim`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ claim_text: claimText }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error("Error verifying claim:", error);
        throw error;
    }
};
