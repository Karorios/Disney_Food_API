// API client para Disney_Food_API
// Todas las peticiones usan JSON y manejo básico de errores.

const API_BASE_URL = window.location.origin;

async function handleResponse(response) {
    if (!response.ok) {
        let detail = "Error en la petición";
        try {
            const data = await response.json();
            detail = data.detail || JSON.stringify(data);
        } catch (_) {
            // ignore
        }
        throw new Error(detail);
    }
    if (response.status === 204) return null;
    return response.json();
}

// ---- Utilidad para toasts Bulma ----
export function showToast(message, type = "is-danger") {
    const containerId = "toast-container";
    let container = document.getElementById(containerId);
    if (!container) {
        container = document.createElement("div");
        container.id = containerId;
        container.style.position = "fixed";
        container.style.top = "1rem";
        container.style.right = "1rem";
        container.style.zIndex = "9999";
        document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.className = `notification ${type}`;
    toast.textContent = message;

    const btn = document.createElement("button");
    btn.className = "delete";
    btn.addEventListener("click", () => toast.remove());
    toast.prepend(btn);

    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

// ================= RECETAS =================

export async function getRecetas() {
    const res = await fetch(`${API_BASE_URL}/recetas/find/all`);
    return handleResponse(res);
}

export async function buscarRecetasPorNombre(nombre) {
    const params = new URLSearchParams({ nombre });
    const res = await fetch(`${API_BASE_URL}/recetas/search?${params.toString()}`);
    return handleResponse(res);
}

export async function createReceta(payload) {
    const res = await fetch(`${API_BASE_URL}/recetas/crear`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
    return handleResponse(res);
}

export async function updateReceta(id, payload) {
    const res = await fetch(`${API_BASE_URL}/recetas/update/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
    return handleResponse(res);
}

export async function deleteReceta(id) {
    const res = await fetch(`${API_BASE_URL}/recetas/kill/${id}`, {
        method: "DELETE",
    });
    return handleResponse(res);
}

// ================= PELÍCULAS =================

export async function getPeliculas() {
    const res = await fetch(`${API_BASE_URL}/peliculas/find/all`);
    return handleResponse(res);
}

export async function createPelicula(payload) {
    const res = await fetch(`${API_BASE_URL}/peliculas/crear`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
    return handleResponse(res);
}

export async function updatePelicula(id, payload) {
    const res = await fetch(`${API_BASE_URL}/peliculas/update/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });
    return handleResponse(res);
}

export async function deletePelicula(id) {
    const res = await fetch(`${API_BASE_URL}/peliculas/kill/${id}`, {
        method: "DELETE",
    });
    return handleResponse(res);
}

// ================= ESTADÍSTICAS (Dashboard) =================

export async function getEstadisticas() {
    const res = await fetch(`${API_BASE_URL}/reportes/estadisticas`);
    return handleResponse(res);
}

// ================= SUPABASE: subida de imágenes =================

export async function uploadRecetaImage(file) {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${API_BASE_URL}/imagenes/recetas/upload`, {
        method: "POST",
        body: formData,
    });
    return handleResponse(res);
}


