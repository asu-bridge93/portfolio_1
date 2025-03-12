import { NextResponse } from "next/server"

// ストリーミングレスポンスをサポートするバックエンドの場合
export async function POST(request: Request) {
  try {
    const { input } = await request.json()

    if (!input) {
      return NextResponse.json({ error: "入力テキストが必要です" }, { status: 400 })
    }

    const ML_API_URL = process.env.ML_API_URL

    if (!ML_API_URL) {
      return NextResponse.json({ error: "ML_API_URLが設定されていません" }, { status: 500 })
    }

    // バックエンドAPIにリクエストを送信（ストリーミング対応）
    const response = await fetch(`${ML_API_URL}/stream-predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
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

    // ストリーミングレスポンスをそのまま転送
    return new Response(response.body, {
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
      },
    })
  } catch (error) {
    console.error("Error in stream-predict API:", error)
    return NextResponse.json({ error: "サーバーエラーが発生しました" }, { status: 500 })
  }
}

