import { useState, useEffect } from 'react';
import { siteSettingsAPI, SiteSettings } from '../lib/siteSettings';

export function useSiteSettings() {
    const [settings, setSettings] = useState<SiteSettings | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        loadSettings();
    }, []);

    const loadSettings = async () => {
        try {
            setLoading(true);
            setError(null);
            const data = await siteSettingsAPI.getSettings();
            setSettings(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to load site settings');
            console.error('Error loading site settings:', err);
        } finally {
            setLoading(false);
        }
    };

    const refreshSettings = () => {
        loadSettings();
    };

    return {
        settings,
        loading,
        error,
        refreshSettings
    };
}