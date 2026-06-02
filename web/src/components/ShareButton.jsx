import { useState } from 'react'

export default function ShareButton({ origin, maxMinutes, topSite }) {
  const [copied, setCopied] = useState(false)

  if (!origin) return null

  const url = new URL(window.location.href)
  url.search = ''
  url.searchParams.set('lat', origin.lat.toFixed(5))
  url.searchParams.set('lng', origin.lng.toFixed(5))
  url.searchParams.set('maxmin', maxMinutes)
  const shareUrl = url.toString()

  const whatsappText = topSite
    ? `Voy a ver el eclipse del 12 de agosto desde ${topSite.espacio} (${topSite.duracion_totalidad} de totalidad). ¿Te apuntas? Calcula tu ruta 👉 ${shareUrl}`
    : `Calcula desde dónde ver el eclipse solar del 12 de agosto 👉 ${shareUrl}`

  const handleCopy = async () => {
    await navigator.clipboard.writeText(shareUrl)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="share">
      <button className="share__btn share__btn--copy" onClick={handleCopy}>
        {copied ? '✓ Copiado' : '🔗 Copiar enlace'}
      </button>
      <a
        className="share__btn share__btn--whatsapp"
        href={`https://wa.me/?text=${encodeURIComponent(whatsappText)}`}
        target="_blank"
        rel="noopener noreferrer"
      >
        WhatsApp
      </a>
      <a
        className="share__btn share__btn--twitter"
        href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(whatsappText)}`}
        target="_blank"
        rel="noopener noreferrer"
      >
        X / Twitter
      </a>
    </div>
  )
}
