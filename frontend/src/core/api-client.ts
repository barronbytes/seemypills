const { VITE_API_BASE_URL } = import.meta.env;

const API_BASE_URL = VITE_API_BASE_URL;

export async function postFormData<TResponse>(path: string, formData: FormData): Promise<TResponse> {

    // Normalizes url
    const cleanPath = path.startsWith('/') ? path.slice(1) : path;
    const targetUrl = `${API_BASE_URL}${API_BASE_URL.endsWith('/') ? '' : '/'}${cleanPath}`;

    const response = await fetch(targetUrl, {
        method: 'POST',
        body: formData,
        // Browser will handle Content-Type
    });

    if (!response.ok) {
        throw new Error(`Request to ${path} failed with status ${response.status}`);
    }

    return (await response.json()) as TResponse;
}
