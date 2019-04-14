::for /f "tokens=1 delims= " %i% in ('dir /b /s /a-d setup.py') do (set SET_UP_PY=%%i)
::python %SET_UP_PY% sdist
cd ..
python setup.py sdist
