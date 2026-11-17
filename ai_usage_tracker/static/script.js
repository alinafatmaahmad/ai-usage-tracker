
const questionInput = document.getElementById("question");
const answerBox = document.getElementById("answer");
const loading = document.getElementById("loading");

const askBtn = document.getElementById("askBtn");
const streamBtn = document.getElementById("streamBtn");

function setLoading(value) {
    loading.classList.toggle("hidden", !value);

    askBtn.disabled = value;
    streamBtn.disabled = value;
}

function resetMetrics() {
    document.getElementById("inputTokens").textContent = "0";
    document.getElementById("outputTokens").textContent = "0";
    document.getElementById("totalTokens").textContent = "0";
    document.getElementById("latency").textContent = "0 s";
    document.getElementById("cost").textContent = "$0.000000";
}

// Normal API request
async function askAI() {

    const question = questionInput.value.trim();

    if (!question) {
        alert("Please enter a question.");
        return;
    }

    setLoading(true);
    resetMetrics();
    answerBox.textContent = "Generating answer...";

    try {

        const response = await fetch("/ask", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Request failed");
        }

        answerBox.textContent = data.answer;

        document.getElementById("inputTokens").textContent =
            data.input_tokens;

        document.getElementById("outputTokens").textContent =
            data.output_tokens;

        document.getElementById("totalTokens").textContent =
            data.total_tokens;

        document.getElementById("latency").textContent =
            data.latency_seconds + " s";

        document.getElementById("cost").textContent =
            "$" + Number(data.cost_usd).toFixed(6);

    } catch (error) {

        answerBox.textContent = "Error: " + error.message;

    } finally {

        setLoading(false);

    }
}


// Streaming API request
async function streamAI() {

    const question = questionInput.value.trim();

    if (!question) {
        alert("Please enter a question.");
        return;
    }

    setLoading(true);
    resetMetrics();

    answerBox.textContent = "";

    try {

        const response = await fetch("/stream", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || "Streaming failed");
        }

        if (!response.body) {
            throw new Error("Streaming is not supported.");
        }

        const reader = response.body.getReader();

        const decoder = new TextDecoder();

        while (true) {

            const { done, value } = await reader.read();

            if (done) {
                break;
            }

            const chunk = decoder.decode(value, {
                stream: true
            });

            answerBox.textContent += chunk;
        }

        answerBox.textContent += decoder.decode();

    } catch (error) {

        answerBox.textContent +=
            "\nError: " + error.message;

    } finally {

        setLoading(false);

    }
}
