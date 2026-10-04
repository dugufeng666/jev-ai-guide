# Adsterra Zone Configuration

The site supports seven ad placements. The existing zones are kept in the ad component; the four new zone IDs must be created in the Adsterra dashboard for `jev-ai-guide.com` and added as Cloudflare Pages environment variables.

| Placement | Size | Current configuration |
| --- | --- | --- |
| Leaderboard | 728x90 | Existing zone in `src/components/ads/adsterra-ads.tsx` |
| Banner | 468x60 | `NEXT_PUBLIC_ADSTERRA_468_KEY` |
| Rectangle | 300x250 | Existing zone in `src/components/ads/adsterra-ads.tsx` |
| Tall rail | 160x600 | `NEXT_PUBLIC_ADSTERRA_160X600_KEY` |
| Short rail | 160x300 | `NEXT_PUBLIC_ADSTERRA_160X300_KEY` |
| Sticky | 320x50 | `NEXT_PUBLIC_ADSTERRA_320X50_KEY` |
| Native | Native | Existing native script in `src/components/ads/adsterra-ads.tsx` |

The 320x50 placement is site-wide and can be closed by the visitor. The 160px rail selects 160x600 on wide desktop screens and 160x300 on smaller desktop screens. Missing keys are intentionally skipped until the matching Adsterra zone is created.
