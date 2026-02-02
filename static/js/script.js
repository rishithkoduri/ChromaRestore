document.addEventListener("DOMContentLoaded", () => {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");
    const previewContainer = document.getElementById("preview-container");
    const imgOriginal = document.getElementById("img-original");
    const imgResult = document.getElementById("img-result");
    const btnConvert = document.getElementById("btn-convert");
    const btnDownload = document.getElementById("btn-download");
    const loader = document.getElementById("loader");
    const themeToggle = document.getElementById("theme-toggle");

    themeToggle.addEventListener("click", () => {
        const isDark = document.body.getAttribute("data-theme") === "dark";
        document.body.setAttribute("data-theme", isDark ? "light" : "dark");
        themeToggle.textContent = isDark ? "🌙" : "☀";
    });

    dropZone.addEventListener("click", () => fileInput.click());

    fileInput.addEventListener("change", (e) => handleFile(e.target.files[0]));

    function handleFile(file) {
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (e) => {
            imgOriginal.src = e.target.result;
            imgResult.src = "";
            previewContainer.style.display = "block";
            btnDownload.classList.add("disabled");
            imgResult.style.display = "none";
        };
        reader.readAsDataURL(file);
    }

    btnConvert.addEventListener("click", async () => {
        const file = fileInput.files[0];
        if (!file) return alert("Please select an image first.");

        btnConvert.disabled = true;
        btnConvert.textContent = "Processing...";
        imgResult.style.display = "none";
        loader.style.display = "block";

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("/convert", {
                method: "POST",
                body: formData
            });
            const data = await response.json();

            if (data.error) throw new Error(data.error);

            imgResult.src = data.result + "?t=" + new Date().getTime();
            imgResult.style.display = "block";
            btnDownload.href = "/download/" + data.filename;
            btnDownload.classList.remove("disabled");

        } catch (error) {
            alert("Error: " + error.message);
        } finally {
            loader.style.display = "none";
            btnConvert.disabled = false;
            btnConvert.textContent = "✨ Convert & Upscale";
        }
    });
});