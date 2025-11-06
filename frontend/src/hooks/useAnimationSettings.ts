import { useState, useEffect } from 'react';

interface AnimationSettings {
  enableStarAnimation: boolean;
}

export function useAnimationSettings() {
  const [settings, setSettings] = useState<AnimationSettings>({
    enableStarAnimation: true, // Default to true
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        // Use Next.js API proxy for client-side calls
        const response = await fetch('/api/v1/core/animation-settings/');
        if (response.ok) {
          const data = await response.json();
          setSettings(data);
        } else {
          console.warn('Failed to fetch animation settings, using defaults');
        }
      } catch (error) {
        console.error('Failed to fetch animation settings:', error);
        // Keep default settings on error
      } finally {
        setIsLoading(false);
      }
    };

    fetchSettings();
  }, []);

  return { settings, isLoading };
}