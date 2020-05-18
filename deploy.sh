git add .
git commit -m "implove"

expect -c "
spawn git push
expect \"Username\"
send \"kanon07\n\"
expect \"password\"
send \"wakamekanonn13\n\"
"
