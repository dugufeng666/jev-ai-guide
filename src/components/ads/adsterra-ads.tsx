"use client";

import { useEffect, useRef, useState } from "react";

type DisplayZone = {
  key: string;
  width: number;
  height: number;
};

const DISPLAY_SCRIPT_DOMAIN = "www.highrevenueformat.com";
const DESKTOP_DISPLAY_ZONE: DisplayZone = {
  key: "3d4c8fdef84d7cafc13bd71259af9629",
  width: 728,
  height: 90,
};
const MOBILE_DISPLAY_ZONE: DisplayZone = {
  key: "5a57fe79f61cc6bdf5a2c84c51360adc",
  width: 300,
  height: 250,
};
const NATIVE_CONTAINER_ID = "container-f7368d5f793f0a39b99252143afca64f";
const NATIVE_SCRIPT_SRC = "https://pl31453397.profitableratecpmnetwork.com/f7368d5f793f0a39b99252143afca64f/invoke.js";

function SponsoredFrame({
  children,
  className = "",
  label = "Sponsored",
}: {
  children: React.ReactNode;
  className?: string;
  label?: string;
}) {
  return (
    <aside
      className={`my-10 overflow-hidden rounded-2xl border border-border bg-card/50 p-3 text-center ${className}`}
      aria-label="Sponsored content"
    >
      <div className="mb-2 text-[10px] font-semibold uppercase tracking-[0.22em] text-muted-foreground">
        {label}
      </div>
      {children}
    </aside>
  );
}

function injectDisplayAd(container: HTMLDivElement, zone: DisplayZone) {
  container.innerHTML = "";

  const configScript = document.createElement("script");
  configScript.text = `window.atOptions = ${JSON.stringify({
    key: zone.key,
    format: "iframe",
    height: zone.height,
    width: zone.width,
    params: {},
  })};`;

  const invokeScript = document.createElement("script");
  invokeScript.src = `https://${DISPLAY_SCRIPT_DOMAIN}/${zone.key}/invoke.js`;
  invokeScript.async = true;

  container.appendChild(configScript);
  container.appendChild(invokeScript);
}

export function AdsterraResponsiveDisplayAd() {
  const ref = useRef<HTMLDivElement>(null);
  const [zone, setZone] = useState<DisplayZone | null>(null);

  useEffect(() => {
    const query = window.matchMedia("(min-width: 768px)");
    const updateZone = () => setZone(query.matches ? DESKTOP_DISPLAY_ZONE : MOBILE_DISPLAY_ZONE);

    updateZone();
    query.addEventListener("change", updateZone);
    return () => query.removeEventListener("change", updateZone);
  }, []);

  useEffect(() => {
    if (!ref.current || !zone) return;
    injectDisplayAd(ref.current, zone);
  }, [zone]);

  return (
    <SponsoredFrame>
      <div className="mx-auto flex max-w-full justify-center overflow-hidden">
        <div ref={ref} style={{ width: zone?.width ?? 300, minHeight: zone?.height ?? 90 }} />
      </div>
    </SponsoredFrame>
  );
}

export function AdsterraNativeAd() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current) return;

    const script = document.createElement("script");
    script.src = NATIVE_SCRIPT_SRC;
    script.async = true;
    script.setAttribute("data-cfasync", "false");
    ref.current.appendChild(script);

    return () => {
      script.remove();
    };
  }, []);

  return (
    <SponsoredFrame className="mt-12" label="More resources">
      <div ref={ref} className="mx-auto max-w-full overflow-hidden">
        <div id={NATIVE_CONTAINER_ID} />
      </div>
    </SponsoredFrame>
  );
}
