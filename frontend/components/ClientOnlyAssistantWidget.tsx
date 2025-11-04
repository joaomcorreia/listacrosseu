"use client";

import { useEffect, useState } from "react";
import PublicAssistantWidget from "./PublicAssistantWidget";

export default function ClientOnlyAssistantWidget({ initialLang = "en", isLoggedIn = false }: { initialLang?: string; isLoggedIn?: boolean }) {
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
    }, []);

    if (!mounted) {
        return null; // Return nothing on server-side render
    }

    return <PublicAssistantWidget initialLang={initialLang} isLoggedIn={isLoggedIn} />;
}