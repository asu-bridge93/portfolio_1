import { NextResponse } from "next/server"

export async function POST(request: Request) {
  try {
    // リクエストボディからデータを取得
    const { input } = await request.json()

    if (!input) {
      return NextResponse.json({ error: "入力テキストが必要です" }, { status: 400 })
    }

    // バックエンドの機械学習モデルAPIのURLを環境変数から取得
    const ML_API_URL = process.env.ML_API_URL

    if (!ML_API_URL) {
      return NextResponse.json({ error: "ML_API_URLが設定されていません" }, { status: 500 })
    }

    // バックエンドAPIにリクエストを送信
    const response = await fetch(`${ML_API_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // 必要に応じて認証トークンを追加
        ...(process.env.ML_API_KEY && { Authorization: `Bearer ${process.env.ML_API_KEY}` }),
      },
      body: JSON.stringify({ input }),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      return NextResponse.json(
        { error: errorData.message || "バックエンドAPIからのレスポンスエラー" },
        { status: response.status },
      )
    }

    // バックエンドからのレスポンスを取得
    const data = await response.json()

    // フロントエンドにレスポンスを返す
    return NextResponse.json({ result: data.prediction || data.result || data })
  } catch (error) {
    console.error("Error in predict API:", error)
    return NextResponse.json({ error: "サーバーエラーが発生しました" }, { status: 500 })
  }
}

