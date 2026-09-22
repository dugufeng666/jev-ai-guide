const ADSTERRA_ENABLED = process.env.NEXT_PUBLIC_ADSTERRA_ENABLED === "1";
const ADSTERRA_KEY = process.env.NEXT_PUBLIC_ADSTERRA_BANNER_KEY;
const ADSTERRA_DOMAIN = process.env.NEXT_PUBLIC_ADSTERRA_SCRIPT_DOMAIN || "www.highperformanceformat.com";
const ADSTERRA_WIDTH = Number(process.env.NEXT_PUBLIC_ADSTERRA_BANNER_WIDTH || "728");
const ADSTERRA_HEIGHT = Number(process.env.NEXT_PUBLIC_ADSTERRA_BANNER_HEIGHT || "90");

function isValidDimension(value: number) {
  return Number.isFinite(value) && value > 0 && value <= 1200;
}

export function AdsterraDisplayAd({ className = "" }: { className?: string }) {
  if (!ADSTERRA_ENABLED || !ADSTERRA_KEY) return null;

  const width = isValidDimension(ADSTERRA_WIDTH) ? ADSTERRA_WIDTH : 728;
  const height = isValidDimension(ADSTERRA_HEIGHT) ? ADSTERRA_HEIGHT : 90;
  const src = `https://${ADSTERRA_DOMAIN}/${ADSTERRA_KEY}/invoke.js`;
  const atOptions = {
    key: ADSTERRA_KEY,
    format: "iframe",
    height,
    width,
    params: {},
  };

  return (
    <aside
      className={`my-10 overflow-hidden rounded-2xl border border-border bg-card/50 p-3 text-center ${className}`}
      aria-label="Sponsored content"
    >
      <div className="mb-2 text-[10px] font-semibold uppercase tracking-[0.22em] text-muted-foreground">
        Sponsored
      </div>
      <div className="mx-auto flex max-w-full justify-center overflow-hidden">
        <script
          dangerouslySetInnerHTML={{
            __html: `window.atOptions = ${JSON.stringify(atOptions)};`,
          }}
        />
        <script src={src} async />
      </div>
    </aside>
  );
}
