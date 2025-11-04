'use client';

import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
    children: ReactNode;
}

interface State {
    hasError: boolean;
    errorType: string | null;
}

class ChunkErrorBoundary extends Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = { hasError: false, errorType: null };
    }

    static getDerivedStateFromError(error: Error): State {
        // Check if it's a chunk loading error
        const isChunkError = error.name === 'ChunkLoadError' || 
            error.message.includes('Loading chunk') ||
            error.message.includes('ChunkLoadError') ||
            error.stack?.includes('ChunkLoadError');

        return {
            hasError: true,
            errorType: isChunkError ? 'chunk' : 'general'
        };
    }

    componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error('Error caught by boundary:', error, errorInfo);
        
        // If it's a chunk error, try to reload the page after a short delay
        if (this.state.errorType === 'chunk') {
            console.log('Chunk loading error detected, will reload page...');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        }
    }

    render() {
        if (this.state.hasError) {
            if (this.state.errorType === 'chunk') {
                return (
                    <div className="min-h-screen flex items-center justify-center bg-gray-50">
                        <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
                            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                            <h2 className="text-xl font-semibold text-gray-900 mb-2">
                                Updating Application
                            </h2>
                            <p className="text-gray-600 mb-4">
                                The application is being updated. Please wait while we reload the latest version...
                            </p>
                            <button
                                onClick={() => window.location.reload()}
                                className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
                            >
                                Reload Now
                            </button>
                        </div>
                    </div>
                );
            }

            // General error fallback
            return (
                <div className="min-h-screen flex items-center justify-center bg-gray-50">
                    <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8 text-center">
                        <div className="text-red-500 text-4xl mb-4">⚠️</div>
                        <h2 className="text-xl font-semibold text-gray-900 mb-2">
                            Something went wrong
                        </h2>
                        <p className="text-gray-600 mb-4">
                            We encountered an unexpected error. Please try refreshing the page.
                        </p>
                        <button
                            onClick={() => {
                                this.setState({ hasError: false, errorType: null });
                                window.location.reload();
                            }}
                            className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
                        >
                            Try Again
                        </button>
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ChunkErrorBoundary;