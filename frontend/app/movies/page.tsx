'use client'

import { useSearchParams } from 'next/navigation'
import { useEffect, useState, Suspense } from 'react'

// Definimos la estructura exacta que devuelve nuestro backend mejorado
type Movie = {
  movieId: number
  title: string
  genres: string
  score: number
  poster_url: string
  tmdb_id: number | null
  watch_link: string
  overview: string
}

// 1. Creamos un componente interno con la lógica (Este NO se exporta por defecto)
function MoviesContent() {
  const searchParams = useSearchParams()
  const query = searchParams.get('title')

  const [movies, setMovies] = useState<Movie[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!query) return

    setLoading(true)

    // Llamada al backend
    fetch(`https://recomendador-pelicula-s4p8.onrender.com/recommend/text?q=${encodeURIComponent(query)}`)
      .then(res => res.json())
      .then(data => {
        setMovies(data)
        setLoading(false)
      })
      .catch((err) => {
        console.error(err)
        setLoading(false)
      })
  }, [query])

  return (
    <main className="min-h-screen bg-black text-white p-10">
      <h1 className="text-3xl font-bold mb-2">
        Recomendaciones para: <span className="text-blue-400">"{query}"</span>
      </h1>

      {loading && (
        <div className="flex justify-center mt-10">
            <p className="text-white/60 animate-pulse">Buscando las mejores películas...</p>
        </div>
      )}

      {!loading && movies.length === 0 && (
        <p className="text-white/60 mt-6">
          No se encontraron resultados. Intenta con otra descripción.
        </p>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-8">
        {movies.map((movie) => (
          <div
            key={movie.movieId}
            className="bg-zinc-900 rounded-xl overflow-hidden shadow-lg hover:shadow-blue-900/20 transition-all border border-zinc-800 flex flex-col"
          >
            {/* Imagen del Poster */}
            <div className="relative h-[400px] w-full overflow-hidden">
                {movie.poster_url && !movie.poster_url.includes("Error") ? (
                <img
                    src={movie.poster_url}
                    alt={movie.title}
                    className="w-full h-full object-cover"
                />
                ) : (
                <div className="w-full h-full flex items-center justify-center bg-zinc-800 text-white/40">
                    Sin imagen
                </div>
                )}
                
                {/* Puntuación flotante */}
                <div className="absolute top-2 right-2 bg-black/80 text-yellow-400 px-2 py-1 rounded-md text-sm font-bold border border-yellow-500/50">
                    {(movie.score * 100).toFixed(0)}% Match
                </div>
            </div>

            <div className="p-4 flex flex-col flex-grow">
              <h3 className="font-bold text-xl mb-1 text-white">
                {movie.title}
              </h3>
              
              <p className="text-xs text-blue-400 mb-3 uppercase tracking-wider">
                {movie.genres.replace(/\|/g, " • ")}
              </p>

              {/* Descripción corta */}
              {movie.overview && (
                  <p className="text-sm text-zinc-400 line-clamp-3 mb-4 flex-grow">
                      {movie.overview}
                  </p>
              )}

              {/* Botón de Redirección */}
              {movie.watch_link ? (
                  <a 
                    href={movie.watch_link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-auto block w-full bg-blue-600 hover:bg-blue-700 text-white text-center py-2 rounded-lg font-medium transition-colors"
                  >
                    Ver ahora 🍿
                  </a>
              ) : (
                  <button disabled className="mt-auto w-full bg-zinc-800 text-zinc-500 py-2 rounded-lg font-medium cursor-not-allowed">
                    No disponible
                  </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </main>
  )
}

// 2. Exportamos el componente contenedor con Suspense
export default function MoviesPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-black text-white p-10">Cargando buscador...</div>}>
      <MoviesContent />
    </Suspense>
  )
}