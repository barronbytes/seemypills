const { VITE_API_BASE_URL } = import.meta.env;

const API_BASE_URL = VITE_API_BASE_URL;

export async function postFormData<TResponse>(path: string, formData: FormData): Promise<TResponse> {
    const response = await fetch(`${API_BASE_URL}${path}`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        throw new Error(`Request to ${path} failed with status ${response.status}`);
    }

    return (await response.json()) as TResponse;
}
