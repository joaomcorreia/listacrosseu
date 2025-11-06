export default function MaintenancePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 flex items-center justify-center p-4">
      <div className="max-w-md mx-auto text-center bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 shadow-2xl">
        <div className="text-6xl mb-6 animate-pulse">🔧</div>
        <div className="text-white mb-2">
          <h1 className="text-2xl font-bold mb-4">ListAcross EU</h1>
          <h2 className="text-xl font-semibold mb-4">We're Making Things Better!</h2>
        </div>
        
        <div className="bg-white/20 rounded-lg p-4 mb-6">
          <p className="text-white/90 font-medium mb-2">Maintenance in Progress</p>
          <p className="text-white/80 text-sm">Our team is working hard to improve your experience. We'll be back online shortly!</p>
        </div>
        
        <p className="text-white/80 text-sm mb-4">
          We're updating our systems to serve you better. This maintenance is necessary to ensure optimal performance and security.
        </p>
        
        <div className="flex items-center justify-center space-x-2 text-white/80 mb-6">
          <span className="animate-spin text-lg">⚙️</span>
          <span className="text-sm">Expected downtime: Minimal</span>
        </div>
        
        <div className="text-white/70 text-xs">
          <p className="mb-1">Need immediate assistance?</p>
          <p className="font-medium">📧 support@listacrosseu.com</p>
          <p className="mt-2">Thank you for your patience!</p>
        </div>
      </div>
      
      <script
        dangerouslySetInnerHTML={{
          __html: `
            // Auto-refresh every 30 seconds to check if maintenance is over
            setTimeout(function() {
              window.location.reload();
            }, 30000);
          `,
        }}
      />
    </div>
  );
}