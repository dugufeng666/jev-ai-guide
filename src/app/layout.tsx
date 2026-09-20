import "./globals.css";
import Script from "next/script";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Script
        src="https://www.googletagmanager.com/gtag/js?id=G-92XSVMK0KT"
        strategy="afterInteractive"
      />
      <Script id="google-analytics" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', 'G-92XSVMK0KT');
        `}
      </Script>
      {children}
    </>
  );
}
