'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useCallback } from 'react';

export function useNavigationErrorHandler() {
    const router = useRouter();

    const handleChunkError = useCallback((error: Error) => {
        const isChunkError = 
            error?.name === 'ChunkLoadError' ||
            error?.message?.includes('Loading chunk') ||
            error?.message?.includes('ChunkLoadError') ||
            error?.stack?.includes('ChunkLoadError');

        if (isChunkError) {
            console.log('Navigation chunk error detected, reloading page...');
            window.location.reload();
            return true; // Indicates error was handled
        }
        return false; // Error not handled
    }, []);

    // Safe navigation function with chunk error handling
    const safeNavigate = useCallback((path: string) => {
        try {
            router.push(path);
        } catch (error) {
            if (!handleChunkError(error as Error)) {
                // If it's not a chunk error, try to navigate again
                console.warn('Navigation error, retrying...', error);
                setTimeout(() => {
                    try {
                        router.push(path);
                    } catch (retryError) {
                        console.error('Failed to navigate after retry:', retryError);
                        // As last resort, use window.location
                        window.location.href = path;
                    }
                }, 100);
            }
        }
    }, [router, handleChunkError]);

    useEffect(() => {
        // Listen for route change errors
        const handleRouteChangeError = (err: Error) => {
            handleChunkError(err);
        };

        // Note: Next.js 13+ App Router doesn't expose route change events in the same way
        // The error boundary and global error handler will catch most cases
        
        return () => {
            // Cleanup if needed
        };
    }, [handleChunkError]);

    return {
        safeNavigate,
        handleChunkError
    };
}