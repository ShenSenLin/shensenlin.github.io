git config --global http.proxy "socks5://127.0.0.1:10808"
git config --global https.proxy "socks5://127.0.0.1:10808"

git pull

git add --all
git commit -m "none"
git push -u origin main

git config --global --unset http.proxy
git config --global --unset https.proxy

pause