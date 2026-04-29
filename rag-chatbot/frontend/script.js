/**
 * University Chatbot Frontend Logic
 * Features:
 * - Authentication (LocalStorage Session)
 * - Dark Mode Support
 * - Sidebar Chatbot Interactivity
 * - RAG API Integration
 */

const API_URL = "http://127.0.0.1:8000/chat";

document.addEventListener("DOMContentLoaded", () => {
    // Determine which page we are on
    const isLoginPage = window.location.pathname.includes("login.html");
    const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";

    // 1. --- AUTHENTICATION LOGIC ---
    if (!isLoginPage && !isLoggedIn) {
        window.location.href = "login.html";
        return;
    }

    if (isLoginPage && isLoggedIn) {
        window.location.href = "index.html";
        return;
    }

    // 2. --- LOGIN PAGE LOGIC ---
    if (isLoginPage) {
        const loginForm = document.getElementById("login-form");
        const guestBtn = document.getElementById("guest-btn");
        const errorMessage = document.getElementById("error-message");

        if (loginForm) {
            loginForm.addEventListener("submit", (e) => {
                e.preventDefault();
                const email = document.getElementById("email").value;
                const password = document.getElementById("password").value;

                if (email && password) {
                    localStorage.setItem("isLoggedIn", "true");
                    window.location.href = "index.html";
                } else {
                    errorMessage.style.display = "block";
                }
            });
        }

        if (guestBtn) {
            guestBtn.addEventListener("click", () => {
                localStorage.setItem("isLoggedIn", "true");
                window.location.href = "index.html";
            });
        }
    }

    // 3. --- MAIN PAGE LOGIC (index.html) ---
    if (!isLoginPage) {
        // Elements
        const themeToggle = document.getElementById("theme-toggle");
        const logoutBtn = document.getElementById("logout-btn");
        const chatPanel = document.getElementById("chat-panel");
        const openChatBtn = document.getElementById("open-chat");
        const chatHeroBtn = document.getElementById("start-chat-hero");
        const closeChatBtn = document.getElementById("close-chat");
        const chatInput = document.getElementById("chat-input");
        const sendBtn = document.getElementById("send-btn");
        const chatMessages = document.getElementById("chat-messages");
        const typingStatus = document.getElementById("typing-status");

        // --- THEME MANAGEMENT ---
        const savedTheme = localStorage.getItem("theme") || "light";
        document.body.setAttribute("data-theme", savedTheme);
        updateThemeIcon(savedTheme);

        if (themeToggle) {
            themeToggle.addEventListener("click", () => {
                const currentTheme = document.body.getAttribute("data-theme");
                const newTheme = currentTheme === "light" ? "dark" : "light";
                document.body.setAttribute("data-theme", newTheme);
                localStorage.setItem("theme", newTheme);
                updateThemeIcon(newTheme);
            });
        }

        function updateThemeIcon(theme) {
            const icon = themeToggle.querySelector("i");
            if (theme === "dark") {
                icon.classList.replace("fa-moon", "fa-sun");
            } else {
                icon.classList.replace("fa-sun", "fa-moon");
            }
        }

        // --- AUTH: LOGOUT ---
        if (logoutBtn) {
            logoutBtn.addEventListener("click", () => {
                localStorage.clear();
                window.location.href = "login.html";
            });
        }

        // --- CHAT INTERFACE ---
        const toggleChat = (show) => {
            if (show) chatPanel.classList.add("active");
            else chatPanel.classList.remove("active");
        };

        if (openChatBtn) openChatBtn.addEventListener("click", () => toggleChat(true));
        if (chatHeroBtn) chatHeroBtn.addEventListener("click", () => toggleChat(true));
        if (closeChatBtn) closeChatBtn.addEventListener("click", () => toggleChat(false));

        // --- CHAT API LOGIC ---
        const appendMessage = (text, role, isError = false) => {
            const msgDiv = document.createElement("div");
            msgDiv.classList.add("message");
            msgDiv.classList.add(role === "user" ? "user-message" : "bot-message");
            if (isError) msgDiv.style.color = "#dc3545";
            msgDiv.innerText = text;
            chatMessages.appendChild(msgDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        };

        const handleChatSend = async () => {
            const query = chatInput.value.trim();
            if (!query) return;

            appendMessage(query, "user");
            chatInput.value = "";
            typingStatus.style.display = "block";
            
            // Disable input while loading
            chatInput.disabled = true;
            sendBtn.disabled = true;

            try {
                const response = await fetch(API_URL, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query: query })
                });

                const data = await response.json();
                typingStatus.style.display = "none";

                if (response.ok) {
                    appendMessage(data.answer, "bot");
                } else {
                    const error = data.detail || "Server error occurred.";
                    appendMessage(`Error: ${error}`, "bot", true);
                }
            } catch (err) {
                typingStatus.style.display = "none";
                appendMessage("Connection error. Is the backend running at " + API_URL + "?", "bot", true);
                console.error("Chat Error:", err);
            } finally {
                chatInput.disabled = false;
                sendBtn.disabled = false;
                chatInput.focus();
            }
        };

        if (sendBtn) sendBtn.addEventListener("click", handleChatSend);
        if (chatInput) {
            chatInput.addEventListener("keydown", (e) => {
                if (e.key === "Enter") handleChatSend();
            });
        }
    }
});
