# for_slack

Slackのスラッシュコマンドから日報を送信できるやつ。  

## 構成
* Lambda  
    * ロジック実装部分。  
    * requestsをimportしたいのでzipしてアップロードなりする。  

* API Gateway  
    * POSTメソッドで作成する。  
    * 「APIキーの必要性」や「リクエストの検証」はなくてOK。  Slackから送られてくるTokenで、Lambdaの中で認証する。  
    * Slackからのリクエストパラメータは「application/x-www-form-urlencoded」で送られてくる。  
    Lambdaはjsonで受け取ろうとするため、そこの変換をしないとダメ。  
    「統合リクエスト」のマッピングテンプレートを設定する。  
    参考 http://tech.feedforce.jp/aws-lambda.html

* Slack
    * Slash Commandsをインストール  
https://slack.com/apps/A0F82E8CA-slash-commands?next_id=0  
メソッドはPOST。URLはAPI Gateway。あとはなんでもいい。  
    * Webhookもインストール  
    スラッシュコマンドだと送信したメッセージの履歴が残らないので、ロジック部分でSlackのDMにスラッシュコマンドに送ったメッセージと同じ内容をPOSTしている。  
    メール送信部分の処理で5秒くらいかかる。API Gatewayの仕様として、3秒以上処理時間がかかるとこんなエラーになる。  
    `/nippou はエラー「operation_timeout」により失敗しました`  
    回避策はありそうだけど、まあメールは送信できるしおｋ。