export default function Navigation() {
  return (
    <nav className="bg-white/95 backdrop-blur-sm shadow-lg border-b border-blue-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-20">
          {/* Logo Section */}
          <div className="flex items-center">
            <a href="/" className="group flex items-center space-x-3">
              {/* EU-themed Logo */}
              <div className="relative">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl flex items-center justify-center shadow-lg">
                  <span className="text-white font-bold text-sm">EU</span>
                </div>
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-gradient-to-br from-amber-400 to-amber-500 rounded-full flex items-center justify-center">
                  <span className="text-white text-xs">★</span>
                </div>
              </div>
              <div className="flex flex-col">
                <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
                  ListAcrossEU
                </span>
                <span className="text-xs text-slate-500 -mt-1">European Business Directory</span>
              </div>
            </a>
          </div>

          {/* Navigation Links */}
          <div className="hidden lg:flex items-center space-x-8">
            <a
              href="/en/categories"
              className="group flex items-center space-x-2 text-slate-700 hover:text-blue-600 px-4 py-2 rounded-xl hover:bg-blue-50 transition-all duration-200 font-medium"
            >
              <span>📂</span>
              <span>Categories</span>
            </a>
            <a
              href="/en/businesses"
              className="group flex items-center space-x-2 text-slate-700 hover:text-blue-600 px-4 py-2 rounded-xl hover:bg-blue-50 transition-all duration-200 font-medium"
            >
              <span>🏢</span>
              <span>Businesses</span>
            </a>

            {/* Language Selector */}
            <div className="flex items-center space-x-1 bg-slate-50 rounded-xl p-1">
              <a href="/en" className="flex items-center space-x-1 px-3 py-2 rounded-lg text-sm font-medium text-slate-600 hover:text-blue-600 hover:bg-white transition-all">
                <span>🇬🇧</span>
                <span className="hidden xl:block">EN</span>
              </a>
              <a href="/de" className="flex items-center space-x-1 px-3 py-2 rounded-lg text-sm font-medium text-slate-600 hover:text-blue-600 hover:bg-white transition-all">
                <span>🇩🇪</span>
                <span className="hidden xl:block">DE</span>
              </a>
              <a href="/fr" className="flex items-center space-x-1 px-3 py-2 rounded-lg text-sm font-medium text-slate-600 hover:text-blue-600 hover:bg-white transition-all">
                <span>🇫🇷</span>
                <span className="hidden xl:block">FR</span>
              </a>
              <a href="/es" className="flex items-center space-x-1 px-3 py-2 rounded-lg text-sm font-medium text-slate-600 hover:text-blue-600 hover:bg-white transition-all">
                <span>🇪🇸</span>
                <span className="hidden xl:block">ES</span>
              </a>
              <a href="/nl" className="flex items-center space-x-1 px-3 py-2 rounded-lg text-sm font-medium text-slate-600 hover:text-blue-600 hover:bg-white transition-all">
                <span>🇳🇱</span>
                <span className="hidden xl:block">NL</span>
              </a>
              <a href="/pt" className="flex items-center space-x-1 px-3 py-2 rounded-lg text-sm font-medium text-slate-600 hover:text-blue-600 hover:bg-white transition-all">
                <span>🇵🇹</span>
                <span className="hidden xl:block">PT</span>
              </a>
            </div>
          </div>

          {/* Mobile Menu Button */}
          <div className="lg:hidden">
            <button className="p-2 rounded-xl text-slate-600 hover:text-blue-600 hover:bg-blue-50 transition-all">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Gradient Border */}
      <div className="h-1 bg-gradient-to-r from-blue-500 via-blue-600 to-amber-500"></div>
    </nav>
  );
}