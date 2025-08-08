@echo off
echo Warning: Proxy is enabled by default, port 10808
echo If connection fails, please check your proxy

pause

git pull

git add --all
git commit -m "添加传参"
git push -u origin main

pause