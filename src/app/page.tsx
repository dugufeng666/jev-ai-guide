import Link from "next/link";

export default function RootPage() {
  return (
    <main className="mx-auto grid min-h-screen max-w-3xl place-items-center px-4 py-16 text-center">
      <div>
        <h1 className="text-4xl font-extrabold tracking-tight text-foreground">Jev AI Guides</h1>
        <p className="mt-4 text-muted-foreground">Continue to the Jev AI guide hub.</p>
        <Link className="mt-6 inline-flex rounded-lg bg-foreground px-5 py-3 text-sm font-semibold text-background" href="/en">
          Open Jev AI Guides
        </Link>
      </div>
    </main>
  );
}
