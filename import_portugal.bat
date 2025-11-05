@echo off
REM Portuguese Business Import Script
REM Import businesses from major Portuguese cities (20 per city)

echo 🇵🇹 Starting Portuguese Business Import
echo 📊 Target: Major Portuguese cities with 20 businesses each
echo 🎯 Avoiding banks, focusing on diverse business types
echo.

cd /d C:\projects\listacrosseu

REM Counter variables
set total_imported=0
set city_count=0

REM Major Portuguese cities (starting with top 10 for initial test)
set cities[0]=Lisboa, Portugal
set cities[1]=Porto, Portugal
set cities[2]=Coimbra, Portugal
set cities[3]=Braga, Portugal
set cities[4]=Faro, Portugal
set cities[5]=Aveiro, Portugal
set cities[6]=Leiria, Portugal
set cities[7]=Setúbal, Portugal
set cities[8]=Viseu, Portugal
set cities[9]=Évora, Portugal

REM Business queries (avoiding banks)
set queries[0]=restaurants
set queries[1]=cafes
set queries[2]=pharmacies
set queries[3]=supermarkets
set queries[4]=hotels

echo Starting import process...
echo.

REM Process first 5 cities as test batch
for /L %%i in (0,1,4) do (
    set /a city_count+=1
    call :process_city %%i
    timeout /t 3 /nobreak >nul
)

echo.
echo 🎉 PORTUGUESE IMPORT TEST BATCH COMPLETED!
echo 📊 Cities processed: %city_count%
echo 📈 Check Django admin to see imported businesses
echo.
echo 🚀 Ready to continue with more cities if results look good!
goto :end

:process_city
set idx=%1
if %idx%==0 set current_city=Lisboa, Portugal
if %idx%==1 set current_city=Porto, Portugal
if %idx%==2 set current_city=Coimbra, Portugal
if %idx%==3 set current_city=Braga, Portugal
if %idx%==4 set current_city=Faro, Portugal

echo [%city_count%] 🏙️ Processing: %current_city%

REM Try different business types
python manage.py import_google_places --query "restaurants in %current_city%" --region pt
timeout /t 2 /nobreak >nul

python manage.py import_google_places --query "cafes in %current_city%" --region pt  
timeout /t 2 /nobreak >nul

python manage.py import_google_places --query "shops in %current_city%" --region pt
timeout /t 2 /nobreak >nul

python manage.py import_google_places --query "pharmacies in %current_city%" --region pt
timeout /t 2 /nobreak >nul

echo   ✅ %current_city% completed
echo.
goto :eof

:end
pause