# Jev AI Guides

Jev AI Guides is a static-exported Next.js tutorial site for Jev AI.

## Cloudflare Pages

Use the **Next.js (Static HTML Export)** framework preset:

- Build command: `npm run build`
- Build output directory: `out`
- Production branch: `main`

The project uses `output: "export"` in `next.config.mjs`. Cloudflare Pages rewrites clean URLs such as `/guide` and `/api` through `public/_redirects` to the generated `/en/...` files.

Set `NEXT_PUBLIC_SITE_URL` to the production URL if it differs from the fallback in the source, for example:

```text
NEXT_PUBLIC_SITE_URL=https://jev-ai-guide.com
```

Light Adsterra article ads are enabled in `src/components/ads/adsterra-ads.tsx`: one responsive display slot after the article body and one native slot after related guides. Avoid popunder, social bar, and forced-redirect formats on this site because they can hurt early SEO signals and user trust.

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
