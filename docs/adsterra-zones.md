# Adsterra Zone Configuration

The site supports seven ad placements. All zone keys and native script URLs are embedded directly in `src/components/ads/adsterra-ads.tsx`.

| Placement | Size | Current configuration |
| --- | --- | --- |
| Leaderboard | 728x90 | Existing zone in `src/components/ads/adsterra-ads.tsx` |
| Banner | 468x60 | Native Adsterra script |
| Rectangle | 300x250 | Existing zone in `src/components/ads/adsterra-ads.tsx` |
| Tall rail | 160x600 | Native Adsterra script |
| Short rail | 160x300 | Native Adsterra script |
| Sticky | 320x50 | Native Adsterra script |
| Native | Native | Existing native script in `src/components/ads/adsterra-ads.tsx` |

The 320x50 placement is site-wide and can be closed by the visitor. The 160px rail selects 160x600 on wide desktop screens and 160x300 on smaller desktop screens.
