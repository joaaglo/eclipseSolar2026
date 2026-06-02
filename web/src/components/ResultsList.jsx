import { formatTravel } from '../utils/ranking'

export default function ResultsList({ results, onSiteClick }) {
  if (!results) return null
  const { top, bonus } = results

  if (top.length === 0 && bonus.length === 0) {
    return (
      <div className="results-empty">
        No hay sitios accesibles con ese tiempo. Prueba con más minutos.
      </div>
    )
  }

  return (
    <div className="results">
      {top.length > 0 && (
        <>
          <h3 className="results-title">Mejores sitios</h3>
          {top.map((site, i) => (
            <SiteCard key={site.espacio} site={site} rank={i + 1} onClick={() => onSiteClick(site)} />
          ))}
        </>
      )}

      {bonus.length > 0 && (
        <>
          <h3 className="results-title results-title--bonus">
            Con 10 minutos más llegarías a…
          </h3>
          {bonus.map(site => (
            <SiteCard key={site.espacio} site={site} bonus onClick={() => onSiteClick(site)} />
          ))}
        </>
      )}

      <p className="results-disclaimer">
        Tiempos calculados con OSRM en condiciones de tráfico estándar. No refleja
        tráfico real el 12 de agosto ni disponibilidad de plazas. Datos de sitios:
        El País / IGN.
      </p>
    </div>
  )
}

function SiteCard({ site, rank, bonus, onClick }) {
  return (
    <div className={`site-card ${bonus ? 'site-card--bonus' : ''}`} onClick={onClick}>
      <div className="site-card__header">
        {rank && <span className="site-card__rank">{rank}</span>}
        <div className="site-card__name">{site.espacio}</div>
      </div>
      <div className="site-card__meta">
        <span>{site.municipio}</span>
        <div className="site-card__dur-block">
          <span className="site-card__dur-label">eclipse total</span>
          <span className="site-card__duration">🌑 {site.duracion_totalidad}</span>
        </div>
      </div>
      <div className="site-card__travel">
        🚗 {formatTravel(site.travelSecs)}&nbsp;·&nbsp;🅿️ {site.parking}
      </div>
    </div>
  )
}
