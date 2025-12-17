'use client'

import { useRouter } from 'next/navigation'
import { useState } from 'react'

export default function Home() {
  const router = useRouter()
  const [movie, setMovie] = useState('')

  const goToRecommendations = () => {
    if (!movie.trim()) return
    router.push(`/movies?title=${encodeURIComponent(movie)}`)
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-black via-zinc-900 to-black text-white flex items-center justify-center">
      <div className="max-w-xl w-full px-6 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-6">
          recomendador de películas 🎬
        </h1>

        <p className="text-white/70 mb-8">
          escribe una película y descubre recomendaciones similares
          usando machine learning
        </p>

        <div className="flex gap-3">
          <input
            type="text"
            placeholder="ej. inception"
            className="flex-1 px-4 py-3 rounded-lg text-black outline-none"
            value={movie}
            onChange={(e) => setMovie(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && goToRecommendations()}
          />

          <button
            onClick={goToRecommendations}
            className="px-6 py-3 rounded-lg bg-white text-black font-semibold hover:bg-zinc-200 transition"
          >
            buscar
          </button>
        </div>

        <p className="text-xs text-white/40 mt-6">
          backend en fastapi · frontend en next.js · datos de tmdb
        </p>
      </div>
    </main>
  )
}
