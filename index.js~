// -----------------------------------------------------------------------------
// モジュールのインポート
const server = require("express")();
const line = require("@line/bot-sdk"); // Messaging APIのSDKをインポート

// -----------------------------------------------------------------------------
// パラメータ設定
const line_config = {
    channelAccessToken: process.env.LINE_ACCESS_TOKEN, // 環境変数からアクセストークンをセットしています
    channelSecret: process.env.LINE_CHANNEL_SECRET // 環境変数からChannel Secretをセットしています
};

// -----------------------------------------------------------------------------
// Webサーバー設定
server.listen(process.env.PORT || 3000);

// APIコール用インスタンス
const bot = new line.Client(line_config);

// -----------------------------------------------------------------------------
// ルーター設定
server.post('/webhook', line.middleware(line_config), (req, res, next) => {
    res.sendStatus(200);
    console.log(req.body);

	//イベント処理のプロミスを格納
	let events_processed = [];

	//オブジェクトを順次処理
	req.body.events.forEach((event) => {
		//イベントタイプがメッセージかつテキストだった場合
		if (event.type == "message" && event.message.type == "text"){
			//メッセージがこんにちはだったら
			if (event.message.text == "こんにちは"){
				//replymessageで返信し、プロミスをprocessedに格納
				events_processed.push(bot.replyMessage(event.replyToken, {
					type: "text",
					text: "これはこれは"
				}));
			}
		}
	});

	//全イベント終了時したらイベントを個数を出力
	Promise.all(events_processed).then(
		(response) => {
			console.log(`${response.length} event(s) processed.`);
		}
	);
});
