import { afterEach, describe, expect, it, vi } from 'vitest';

import { postFormData } from '../../src/core/api-client';

function mockFetchResponse(body: unknown, init?: ResponseInit): void {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(JSON.stringify(body), init));
}

describe('postFormData', () => {
    afterEach(() => {
        vi.restoreAllMocks();
    });

    it('sends a POST request to the given path with the form data as the body', async () => {
        const formData = new FormData();
        formData.append('file', new File(['photo'], 'bottle.jpg', { type: 'image/jpeg' }));
        mockFetchResponse({ success: true, payload: { id: 'abc-123', brand_name: 'Tylenol' } }, { status: 201 });

        await postFormData('/bottles/', formData);

        const fetchMock = vi.mocked(globalThis.fetch);
        expect(fetchMock).toHaveBeenCalledTimes(1);

        const [url, init] = fetchMock.mock.calls[0];
        expect(String(url)).toContain('/bottles/');
        expect(init?.method).toBe('POST');
        expect(init?.body).toBe(formData);
    });

    it('returns the parsed JSON body when the response is successful', async () => {
        const responseBody = { success: true, payload: { id: 'abc-123', brand_name: 'Tylenol' } };
        mockFetchResponse(responseBody, { status: 201 });

        const result = await postFormData('/bottles/', new FormData());

        expect(result).toEqual(responseBody);
    });

    it('throws an explicit error naming the path and status when the response is not ok', async () => {
        mockFetchResponse({ success: false, detail: 'Uploaded file must be a valid image format.' }, { status: 400 });

        await expect(postFormData('/bottles/', new FormData()))
            .rejects.toThrow('Request to /bottles/ failed with status 400');
    });
});
