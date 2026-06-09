import { z } from 'zod';

export const bottleResponseSchema = z.object({
    id: z.uuid(),
    brand_name: z.string(),
});

export type BottleResponse = z.infer<typeof bottleResponseSchema>;

export const bottleUploadResponseSchema = z.object({
    success: z.boolean(),
    payload: bottleResponseSchema,
});

export type BottleUploadResponse = z.infer<typeof bottleUploadResponseSchema>;
