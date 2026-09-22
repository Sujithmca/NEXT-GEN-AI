(function () {
    if (window.nextGenAiChatInitialized) {
        return;
    }

    const button = document.getElementById("nextgenaiChatButton");
    const windowElement = document.getElementById("nextgenaiChatWindow");
    const form = document.getElementById("nextgenaiChatForm");
    const input = document.getElementById("nextgenaiChatInput");
    const messages = document.getElementById("nextgenaiChatMessages");
    const sendButton = document.getElementById("nextgenaiSendButton");
    const typingIndicator = document.getElementById("nextgenaiTypingIndicator");

    if (!button || !windowElement || !form || !input || !messages || !sendButton || !typingIndicator) {
        return;
    }

    window.nextGenAiChatInitialized = true;
    const endpoint = form.dataset.chatEndpoint;

    function scrollToBottom() {
        messages.scrollTop = messages.scrollHeight;
    }

    function setOpen(isOpen) {
        windowElement.hidden = !isOpen;
        button.setAttribute("aria-expanded", String(isOpen));
        if (isOpen) {
            windowElement.classList.remove("is-minimized");
            input.focus();
            scrollToBottom();
        }
    }

    function addMessage(content, type, iconClass) {
        const row = document.createElement("div");
        const message = document.createElement("div");
        row.className = "nextgenai-message-row" + (type === "user" ? " user" : "");
        message.className = "nextgenai-message " + type;

        if (iconClass) {
            const icon = document.createElement("i");
            icon.className = iconClass;
            icon.setAttribute("aria-hidden", "true");
            message.appendChild(icon);
            message.appendChild(document.createTextNode(" "));
        }

        message.appendChild(document.createTextNode(content));
        row.appendChild(message);
        messages.appendChild(row);
    }

    function showTypingIndicator() {
        typingIndicator.hidden = false;
        scrollToBottom();
    }

    function hideTypingIndicator() {
        typingIndicator.hidden = true;
    }

    button.addEventListener("click", function () {
        setOpen(windowElement.hidden);
    });

    windowElement.querySelectorAll("[data-chat-action]").forEach(function (control) {
        control.addEventListener("click", function () {
            if (control.dataset.chatAction === "close") {
                setOpen(false);
                return;
            }

            windowElement.classList.toggle("is-minimized");
            if (!windowElement.classList.contains("is-minimized")) {
                input.focus();
            }
        });
    });

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const message = input.value.trim();
        if (!message) {
            return;
        }

        addMessage(message, "user");
        input.value = "";
        input.disabled = true;
        sendButton.disabled = true;
        sendButton.textContent = "Sending...";
        showTypingIndicator();

        const csrfToken = form.querySelector("[name=csrfmiddlewaretoken]").value;

        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": csrfToken
                },
                body: new URLSearchParams({ message: message })
            });

            const data = await response.json();
            if (data.success) {
                addMessage(data.message, "ai", "bi bi-stars");
            } else {
                addMessage(data.error || "Something went wrong.", "ai", "bi bi-exclamation-triangle");
            }
        } catch (error) {
            addMessage("Something went wrong. Please try again.", "ai", "bi bi-exclamation-triangle");
            console.error(error);
        } finally {
            hideTypingIndicator();
            input.disabled = false;
            sendButton.disabled = false;
            sendButton.textContent = "Send";
            input.focus();
            scrollToBottom();
        }
    });
})();
