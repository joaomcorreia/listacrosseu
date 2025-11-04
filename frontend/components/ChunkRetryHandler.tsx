'use client';

import { useEffect } from 'react';

interface RetryConfig {
    maxRetries: number;
    retryDelay: number;
    reloadOnFinalFailure: boolean;
}

const defaultConfig: RetryConfig = {
    maxRetries: 3,
    retryDelay: 1000,
    reloadOnFinalFailure: true
};

export function useChunkRetryHandler(config: Partial<RetryConfig> = {}) {
    const finalConfig = { ...defaultConfig, ...config };
    
    useEffect(() => {
        // Store original fetch function
        const originalFetch = window.fetch;
        const retryAttempts = new Map<string, number>();

        // Override fetch to handle chunk loading retries
        window.fetch = async (input: RequestInfo | URL, init?: RequestInit) => {
            const url = typeof input === 'string' ? input : input.toString();
            
            // Only handle chunk-related requests
            if (!url.includes('/_next/static/chunks/') && !url.includes('.js')) {
                return originalFetch(input, init);
            }

            const currentAttempts = retryAttempts.get(url) || 0;
            
            try {
                const response = await originalFetch(input, init);
                
                // If successful, reset retry count
                if (response.ok) {
                    retryAttempts.delete(url);
                    return response;
                }
                
                // If response is not ok and we haven't exceeded max retries
                if (currentAttempts < finalConfig.maxRetries) {
                    retryAttempts.set(url, currentAttempts + 1);
                    console.log(`Retrying chunk load (${currentAttempts + 1}/${finalConfig.maxRetries}): ${url}`);
                    
                    // Wait before retrying
                    await new Promise(resolve => setTimeout(resolve, finalConfig.retryDelay));
                    
                    // Retry the request
                    return window.fetch(input, init);
                } else {
                    // Max retries exceeded
                    console.error(`Failed to load chunk after ${finalConfig.maxRetries} retries: ${url}`);
                    if (finalConfig.reloadOnFinalFailure) {
                        console.log('Reloading page due to chunk loading failure...');
                        window.location.reload();
                    }
                    return response;
                }
            } catch (error) {
                // Network error or other fetch error
                if (currentAttempts < finalConfig.maxRetries) {
                    retryAttempts.set(url, currentAttempts + 1);
                    console.log(`Retrying chunk load after error (${currentAttempts + 1}/${finalConfig.maxRetries}): ${url}`, error);
                    
                    // Wait before retrying
                    await new Promise(resolve => setTimeout(resolve, finalConfig.retryDelay));
                    
                    // Retry the request
                    return window.fetch(input, init);
                } else {
                    // Max retries exceeded
                    console.error(`Failed to load chunk after ${finalConfig.maxRetries} retries: ${url}`, error);
                    if (finalConfig.reloadOnFinalFailure) {
                        console.log('Reloading page due to chunk loading failure...');
                        window.location.reload();
                    }
                    throw error;
                }
            }
        };

        // Cleanup function
        return () => {
            window.fetch = originalFetch;
        };
    }, [finalConfig.maxRetries, finalConfig.retryDelay, finalConfig.reloadOnFinalFailure]);
}

// Component version for easier integration
export default function ChunkRetryHandler(props: Partial<RetryConfig> = {}) {
    useChunkRetryHandler(props);
    return null;
}