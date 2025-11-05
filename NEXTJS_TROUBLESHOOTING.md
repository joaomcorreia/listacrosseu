# Next.js Development Server Troubleshooting Commands

## Quick Reference for Common Issues

### Port Conflicts
```cmd
:: Check what's using port 3000
netstat -ano | findstr :3000

:: Kill specific process by PID
taskkill /PID <PID_NUMBER> /F

:: Kill all processes on port 3000 (be careful!)
for /f "tokens=5" %a in ('netstat -ano ^| findstr :3000') do taskkill /PID %a /F
```

### Cache Issues
```cmd
:: Clean Next.js cache and node_modules cache
cd /d c:\projects\listacrosseu\frontend
npm run clean

:: Full cache clear with node_modules reinstall
cd /d c:\projects\listacrosseu\frontend
rmdir /s /q node_modules
rmdir /s /q .next
del package-lock.json
npm install
```

### Dependency Problems
```cmd
:: Update Next.js and dependencies
cd /d c:\projects\listacrosseu\frontend
npm update

:: Check for vulnerabilities
npm audit

:: Fix vulnerabilities (use with caution)
npm audit fix

:: Reinstall specific packages
npm uninstall next react react-dom
npm install next react react-dom
```

### Server Startup Issues
```cmd
:: Start with verbose logging
cd /d c:\projects\listacrosseu\frontend
npm run dev -- --verbose

:: Start on alternative port
npm run dev:3001

:: Check Node.js version compatibility
node --version
npm --version

:: Clear npm cache
npm cache clean --force
```

### File System Issues
```cmd
:: Check file permissions and locks
cd /d c:\projects\listacrosseu\frontend
dir /a

:: Remove temporary files
del /q /s *.tmp
del /q /s *.lock

:: Check disk space
dir c:\ /-c
```

### Process Management
```cmd
:: List all Node.js processes
tasklist | findstr node

:: List all processes on common development ports
netstat -ano | findstr ":300"
netstat -ano | findstr ":800"

:: Kill all Node.js processes (nuclear option)
taskkill /IM node.exe /F

:: Check if services are running
sc query | findstr -i "node\|npm"
```

### Network and Proxy Issues
```cmd
:: Test Django backend connectivity
curl http://127.0.0.1:8000/api/v1/
ping 127.0.0.1

:: Check proxy configuration
cd /d c:\projects\listacrosseu\frontend
type next.config.js | findstr -i proxy

:: Reset network stack (requires admin)
netsh winsock reset
netsh int ip reset
```

### VS Code Integration
```cmd
:: Open project in VS Code
cd /d c:\projects\listacrosseu
code .

:: Run tasks from command line
cd /d c:\projects\listacrosseu
code --folder-uri file:///c:/projects/listacrosseu --command "workbench.action.tasks.runTask" "Start Next.js Frontend"
```

## Startup Sequence
1. Check port availability: `netstat -ano | findstr :3000`
2. Navigate to frontend: `cd /d c:\projects\listacrosseu\frontend`
3. Verify dependencies: `npm list --depth=0`
4. Clean if needed: `npm run clean`
5. Start server: `npm run dev:3000` or use `start-frontend.cmd`

## Emergency Recovery
If nothing works, nuclear reset:
```cmd
cd /d c:\projects\listacrosseu\frontend
taskkill /IM node.exe /F
rmdir /s /q node_modules
rmdir /s /q .next
rmdir /s /q .turbo
del package-lock.json
npm cache clean --force
npm install
npm run dev:3000
```