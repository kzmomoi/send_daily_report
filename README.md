# send_daily_report

日報のめんどいところを自動で作ってくれるスクリプト。  
gmailにログインしてメール送信する。 

## 概要
定数部分だけ独自で設定する。  
googleのアカウント設定から2段階認証を有効にし、アプリパスワードを生成する。  
GMAIL_PASSWORDにはそのパスワードを設定。  
パスワードとかコミットしないように気をつけてね。  
gmailの設定で、「安全性の低いアプリのアクセス」を有効にすれば、gmailと同じパスワードでもメール送信できるが、セキュリティ的に非推奨なのでアプリのパスワードを使う形式にしている。  
