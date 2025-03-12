"use client"

import type React from "react"
import { useState } from "react"

export default function FinancialPredictionForm() {
  const [formData, setFormData] = useState({
    income: "",
    debt: "",
    creditScore: "",
    loanAmount: ""
  })
  const [result, setResult] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (Object.values(formData).some(value => !value.trim())) {
      alert("すべてのフィールドを入力してください")
      return
    }

    setIsLoading(true)
    setResult(null)

    try {
      const response = await fetch("/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        throw new Error("APIリクエストに失敗しました")
      }

      const data = await response.json()
      setResult(data.result)
    } catch (error) {
      console.error("Error:", error)
      alert(error instanceof Error ? error.message : "予測の取得中にエラーが発生しました")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: "400px", margin: "auto", padding: "20px", border: "1px solid #ccc", borderRadius: "5px" }}>
      <h2>デフォルト予測アプリ</h2>
      <p>金融情報を入力して、デフォルト確率を予測します。</p>
      <form onSubmit={handleSubmit}>
        {Object.entries(formData).map(([key, value]) => (
          <div key={key} style={{ marginBottom: "10px" }}>
            <label htmlFor={key} style={{ display: "block", marginBottom: "5px" }}>{key}</label>
            <input
              id={key}
              name={key}
              type="number"
              placeholder={`入力してください: ${key}`}
              value={value}
              onChange={handleChange}
              style={{ width: "100%", padding: "8px", border: "1px solid #ccc", borderRadius: "4px" }}
            />
          </div>
        ))}

        {result !== null && (
          <div style={{ marginTop: "10px", padding: "10px", background: "#f4f4f4", borderRadius: "5px" }}>
            <strong>予測結果:</strong>
            <pre style={{ whiteSpace: "pre-wrap" }}>{result}</pre>
          </div>
        )}

        <button type="submit" disabled={isLoading} style={{ width: "100%", padding: "10px", background: "blue", color: "white", border: "none", borderRadius: "5px", cursor: "pointer" }}>
          {isLoading ? "処理中..." : "予測を取得"}
        </button>
      </form>
    </div>
  )
}
