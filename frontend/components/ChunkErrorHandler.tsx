'use client';

import { useEffect } from 'react';

export function useChunkErrorHandler() {
    useEffect(() => {
        // Handle unhandled promise rejections (often chunk loading errors)
        const handleUnhandledRejection = (event: PromiseRejectionEvent) => {
            const error = event.reason;
            
            // Check if it's a chunk loading error
            const isChunkError = 
                error?.name === 'ChunkLoadError' ||
                error?.message?.includes('Loading chunk') ||
                error?.message?.includes('ChunkLoadError') ||
                error?.stack?.includes('ChunkLoadError');

            if (isChunkError) {
                console.log('Chunk loading error detected, reloading page...');
                event.preventDefault(); // Prevent the error from being logged to console
                
                // Show a brief loading message and reload
                const loadingDiv = document.createElement('div');
                loadingDiv.innerHTML = `
                    <div style="
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100vw;
                        height: 100vh;
                        background: rgba(0, 0, 0, 0.8);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        z-index: 9999;
                        color: white;
                        font-family: system-ui, -apple-system, sans-serif;
                    ">
                        <div style="text-align: center;">
                            <div style="
                                width: 40px;
                                height: 40px;
                                border: 3px solid #f3f3f3;
                                border-top: 3px solid #3498db;
                                border-radius: 50%;
                                animation: spin 1s linear infinite;
                                margin: 0 auto 16px;
                            "></div>
                            <div style="font-size: 18px; font-weight: 500;">Updating...</div>
                        </div>
                        <style>
                            @keyframes spin {
                                0% { transform: rotate(0deg); }
                                100% { transform: rotate(360deg); }
                            }
                        </style>
                    </div>
                `;
                document.body.appendChild(loadingDiv);
                
                // Reload after a brief delay
                setTimeout(() => {
                    window.location.reload();
                }, 500);
            }
        };

        // Handle general JavaScript errors
        const handleError = (event: ErrorEvent) => {
            const error = event.error;
            
            const isChunkError = 
                error?.name === 'ChunkLoadError' ||
                error?.message?.includes('Loading chunk') ||
                error?.message?.includes('ChunkLoadError') ||
                event.message?.includes('ChunkLoadError');

            if (isChunkError) {
                console.log('Chunk loading error detected in error handler, reloading page...');
                window.location.reload();
            }
        };

        // Add event listeners
        window.addEventListener('unhandledrejection', handleUnhandledRejection);
        window.addEventListener('error', handleError);

        // Cleanup
        return () => {
            window.removeEventListener('unhandledrejection', handleUnhandledRejection);
            window.removeEventListener('error', handleError);
        };
    }, []);
}

// Component version of the hook for easier integration
export default function ChunkErrorHandler() {
    useChunkErrorHandler();
    return null;
}