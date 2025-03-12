import MLModelForm from "../components/ml-model-form"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "ML Model Interface",
  description: "Interface for interacting with a machine learning model",
}

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold mb-8 text-center">ML Model Interface</h1>
        <MLModelForm />
      </div>
    </main>
  )
}

