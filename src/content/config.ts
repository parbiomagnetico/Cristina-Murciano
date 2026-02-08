import { defineCollection, z } from 'astro:content';

const blogCollection = defineCollection({
    type: 'content',
    schema: z.object({
        title: z.string(),
        date: z.string(),
        image: z.string(),
        image_alt: z.string().optional(),
        excerpt: z.string(),
        category: z.string().optional(),
        tags: z.array(z.string()).optional(),
        active: z.boolean().default(true),
        optimized: z.boolean().default(false),
    }),
});

const servicesCollection = defineCollection({
    type: 'content',
    schema: z.object({
        title: z.string(),
        shortDescription: z.string(),
        image: z.string(),
        image_alt: z.string().optional(),
        categoryLabel: z.string().optional(),
    }),
});

export const collections = {
    'blog': blogCollection,
    'services': servicesCollection,
};
