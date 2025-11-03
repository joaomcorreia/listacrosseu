'use client';

import { useEffect } from 'react';
import { useSiteSettings } from '../hooks/useSiteSettings';

export default function DynamicFavicon() {
  const { settings } = useSiteSettings();

  useEffect(() => {
    if (settings?.favicon_url) {
      // Update the favicon in the document head
      let favicon = document.querySelector<HTMLLinkElement>('link[rel="icon"]');
      
      if (!favicon) {
        favicon = document.createElement('link');
        favicon.rel = 'icon';
        document.head.appendChild(favicon);
      }
      
      favicon.href = settings.favicon_url;
      
      // Also update shortcut icon if it exists
      const shortcutIcon = document.querySelector<HTMLLinkElement>('link[rel="shortcut icon"]');
      if (shortcutIcon) {
        shortcutIcon.href = settings.favicon_url;
      }
    }
  }, [settings?.favicon_url]);

  return null; // This component doesn't render anything visible
}