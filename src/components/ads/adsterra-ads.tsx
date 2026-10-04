"use client";

import { useEffect, useRef, useState } from "react";

type DisplayZone = { key: string; width: number; height: number; scriptSrc: string };

const zones = {
  leaderboard: { key: "3d4c8fdef84d7cafc13bd71259af9629", width: 728, height: 90, scriptSrc: "https://www.highrevenueformat.com/3d4c8fdef84d7cafc13bd71259af9629/invoke.js" },
  banner: { key: "3939046193d92adc0c53374263354a3e", width: 468, height: 60, scriptSrc: "https://bicea.org/22/3939046193d92adc0c53374263354a3e" },
  rectangle: { key: "5a57fe79f61cc6bdf5a2c84c51360adc", width: 300, height: 250, scriptSrc: "https://www.highrevenueformat.com/5a57fe79f61cc6bdf5a2c84c51360adc/invoke.js" },
  railTall: { key: "7aee6c604af4a7106f372e54c911d539", width: 160, height: 600, scriptSrc: "https://bicea.org/22/7aee6c604af4a7106f372e54c911d539" },
  railShort: { key: "952e6a1279eee64cfa843921c10605a2", width: 160, height: 300, scriptSrc: "https://bicea.org/22/952e6a1279eee64cfa843921c10605a2" },
  sticky: { key: "3ef32bfa6e4620d78b1105074b04670c", width: 320, height: 50, scriptSrc: "https://bicea.org/22/3ef32bfa6e4620d78b1105074b04670c" },
} satisfies Record<string, DisplayZone>;

const NATIVE_CONTAINER_ID = "container-f7368d5f793f0a39b99252143afca64f";
const NATIVE_SCRIPT_SRC = "https://pl31453397.profitableratecpmnetwork.com/f7368d5f793f0a39b99252143afca64f/invoke.js";

function SponsoredFrame({ children, className = "", label = "Sponsored" }: { children: React.ReactNode; className?: string; label?: string }) {
  return <aside className={`my-10 overflow-hidden rounded-2xl border border-border bg-card/50 p-3 text-center ${className}`} aria-label="Sponsored content"><div className="mb-2 text-[10px] font-semibold uppercase tracking-[0.22em] text-muted-foreground">{label}</div>{children}</aside>;
}

function DisplayAd({ zone, label = "Sponsored" }: { zone: DisplayZone; label?: string }) {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!ref.current || !zone.key) return;
    ref.current.innerHTML = "";
    const config = document.createElement("script");
    config.text = `window.atOptions = ${JSON.stringify({ key: zone.key, format: "iframe", height: zone.height, width: zone.width, params: {} })};`;
    const invoke = document.createElement("script");
    invoke.src = zone.scriptSrc;
    invoke.async = true;
    ref.current.append(config, invoke);
  }, [zone]);
  if (!zone.key) return null;
  return <SponsoredFrame label={label}><div className="mx-auto flex max-w-full justify-center overflow-hidden"><div ref={ref} style={{ width: zone.width, minHeight: zone.height }} /></div></SponsoredFrame>;
}

export function AdsterraLeaderboardAd() { return <DisplayAd zone={zones.leaderboard} />; }
export function Adsterra468Ad() { return <DisplayAd zone={zones.banner} />; }
export function AdsterraRectangleAd() { return <DisplayAd zone={zones.rectangle} />; }

export function AdsterraSidebarAd() {
  const [zone, setZone] = useState<DisplayZone | null>(null);
  useEffect(() => {
    const update = () => setZone(window.matchMedia("(min-width: 1280px)").matches ? zones.railTall : zones.railShort);
    update();
    window.addEventListener("resize", update);
    return () => window.removeEventListener("resize", update);
  }, []);
  return zone ? <DisplayAd zone={zone} label="Sponsored" /> : null;
}

export function AdsterraStickyAd() {
  const [open, setOpen] = useState(true);
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!open || !ref.current || !zones.sticky.key) return;
    const config = document.createElement("script");
    config.text = `window.atOptions = ${JSON.stringify({ key: zones.sticky.key, format: "iframe", height: 50, width: 320, params: {} })};`;
    const invoke = document.createElement("script");
    invoke.src = zones.sticky.scriptSrc;
    invoke.async = true;
    ref.current.append(config, invoke);
  }, [open]);
  if (!open || !zones.sticky.key) return null;
  return <div className="fixed inset-x-0 bottom-0 z-[70] flex justify-center bg-background/90 px-2 py-1 shadow-[0_-4px_20px_rgba(0,0,0,0.2)] backdrop-blur"><div className="relative max-w-full"><span className="absolute -top-4 left-0 text-[9px] uppercase tracking-wider text-muted-foreground">Sponsored</span><div ref={ref} className="h-[50px] w-[320px] max-w-[calc(100vw-3rem)] overflow-hidden" /><button type="button" onClick={() => setOpen(false)} aria-label="Close advertisement" className="absolute -right-5 top-0 h-4 w-4 text-xs leading-none text-muted-foreground hover:text-foreground">×</button></div></div>;
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
    return () => script.remove();
  }, []);
  return <SponsoredFrame className="mt-12" label="More resources"><div ref={ref} className="mx-auto max-w-full overflow-hidden"><div id={NATIVE_CONTAINER_ID} /></div></SponsoredFrame>;
}

/** Kept for existing imports; new placements should use a named size. */
export function AdsterraResponsiveDisplayAd() { return <AdsterraRectangleAd />; }
