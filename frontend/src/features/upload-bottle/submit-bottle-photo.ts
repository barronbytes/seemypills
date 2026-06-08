import { postFormData } from '../../core/api-client';
import { bottleUploadResponseSchema } from '../../shared/types/bottle';

export async function submitBottlePhoto(file: File, status: HTMLElement, result: HTMLElement): Promise<void> {
    const formData = new FormData();
    formData.append('file', file);

    status.textContent = 'Uploading photo…';
    result.textContent = '';

    try {
        const json = await postFormData<unknown>('/bottles/', formData);
        const { payload } = bottleUploadResponseSchema.parse(json);
        status.textContent = 'Upload complete.';
        result.textContent = payload.brand_name;
    } catch (err) {
        console.error('Bottle photo upload failed:', err);
        status.textContent = 'Upload failed. Try again with a clearer photo.';
    }
}
