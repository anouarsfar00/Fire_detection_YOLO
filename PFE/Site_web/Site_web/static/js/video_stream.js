// Connexion WebSocket (assume ws:// pour développement local)
const socket = new WebSocket("ws://" + window.location.host + "/ws/fire/");

// Dès que le WebSocket s'ouvre, on envoie le nom de la caméra (fixe ou dynamique)
socket.onopen = function () {
    console.log("Connexion WebSocket ouverte");

    // TODO : remplacer par le nom de la caméra sélectionnée dynamiquement
    const camName = "Camera_1";

    socket.send(JSON.stringify({
        cam_name: camName
    }));
};

socket.onmessage = function (event) {
    const data = JSON.parse(event.data);

    // Affichage du flux vidéo
    if (data.frame) {
        const imgElement = document.getElementById("video-stream");
        imgElement.src = `data:image/jpeg;base64,${data.frame}`;
    }

    // Affichage des détections
    if (data.detections) {
        const detectionList = document.getElementById("detection-results");
        detectionList.innerHTML = ""; // Reset
        data.detections.forEach(det => {
            const li = document.createElement("li");
            li.classList.add("list-group-item");
            li.textContent = `${det.class_name} (${Math.round(det.confidence * 100)}%)`;
            detectionList.appendChild(li);
        });
    }

    if (data.error) {
        alert("Erreur : " + data.error);
    }
};

socket.onerror = function (error) {
    console.error("WebSocket erreur :", error);
};

socket.onclose = function () {
    console.log("Connexion WebSocket fermée");
};
