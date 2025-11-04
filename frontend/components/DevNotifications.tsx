'use client';

import { useState, useEffect } from 'react';

interface ToastProps {
    message: string;
    type: 'info' | 'warning' | 'error' | 'success';
    duration?: number;
    onClose: () => void;
}

function Toast({ message, type, duration = 4000, onClose }: ToastProps) {
    useEffect(() => {
        const timer = setTimeout(onClose, duration);
        return () => clearTimeout(timer);
    }, [duration, onClose]);

    const colors = {
        info: 'bg-blue-500',
        warning: 'bg-yellow-500', 
        error: 'bg-red-500',
        success: 'bg-green-500'
    };

    return (
        <div className={`fixed top-4 right-4 ${colors[type]} text-white px-4 py-2 rounded-lg shadow-lg z-50 max-w-sm animate-in slide-in-from-top`}>
            <div className="flex items-center justify-between">
                <span className="text-sm">{message}</span>
                <button 
                    onClick={onClose}
                    className="ml-3 text-white hover:text-gray-200"
                >
                    ×
                </button>
            </div>
        </div>
    );
}

export function useDevNotifications() {
    const [notifications, setNotifications] = useState<Array<{
        id: string;
        message: string;
        type: 'info' | 'warning' | 'error' | 'success';
    }>>([]);

    const addNotification = (message: string, type: 'info' | 'warning' | 'error' | 'success' = 'info') => {
        const id = Math.random().toString(36).substr(2, 9);
        setNotifications(prev => [...prev, { id, message, type }]);
    };

    const removeNotification = (id: string) => {
        setNotifications(prev => prev.filter(n => n.id !== id));
    };

    useEffect(() => {
        // Only show notifications in development
        if (process.env.NODE_ENV !== 'development') return;

        const handleChunkRetry = () => {
            addNotification('Retrying chunk load...', 'warning');
        };

        const handleChunkSuccess = () => {
            addNotification('Chunk loaded successfully', 'success');
        };

        const handleChunkFailure = () => {
            addNotification('Chunk loading failed, reloading page...', 'error');
        };

        // Listen for custom events (these would be dispatched by our error handlers)
        window.addEventListener('chunk-retry', handleChunkRetry);
        window.addEventListener('chunk-success', handleChunkSuccess);
        window.addEventListener('chunk-failure', handleChunkFailure);

        return () => {
            window.removeEventListener('chunk-retry', handleChunkRetry);
            window.removeEventListener('chunk-success', handleChunkSuccess);
            window.removeEventListener('chunk-failure', handleChunkFailure);
        };
    }, []);

    const NotificationContainer = () => (
        <div className="fixed top-4 right-4 z-50 space-y-2">
            {notifications.map(notification => (
                <Toast
                    key={notification.id}
                    message={notification.message}
                    type={notification.type}
                    onClose={() => removeNotification(notification.id)}
                />
            ))}
        </div>
    );

    return { addNotification, NotificationContainer };
}

export default function DevNotifications() {
    const { NotificationContainer } = useDevNotifications();
    
    // Only render in development
    if (process.env.NODE_ENV !== 'development') {
        return null;
    }

    return <NotificationContainer />;
}