import ShareButton from './ShareButton'
import ResultsList from './ResultsList'

function formatMinutes(mins) {
  const h = Math.floor(mins / 60)
  const m = mins % 60
  if (h === 0) return `${m} min`
  if (m === 0) return `${h}h`
  return `${h}h ${m}min`
}

const ELPAIS_URL = 'https://elpais.com/ciencia/2026-06-02/mapa-de-sitios-oficiales-para-ver-el-eclipse-total-de-sol-el-pais-actualiza-el-unico-buscador-de-puntos-de-observacion.html'

export default function SearchPanel({
  origin, setOrigin,
  maxMinutes, setMaxMinutes,
  showBand, setShowBand,
  showSites, setShowSites,
  results, loading, error,
  onCalculate,
  onSiteClick,
  geoLoading, geoError, requestGeo,
}) {
  return (
    <div className="panel">

      <div className="panel__header">
        <h1 className="panel__title">Eclipse Solar 2026</h1>
        <p className="panel__subtitle">12 de agosto · España</p>
        <p className="panel__desc">
          ¿Cuál es el mejor sitio cerca de ti para ver el eclipse?
          Nosotros calculamos la mejor opción para ti.
        </p>
      </div>

      <div className="calc-block">

        <div className="calc-step">
          <span className="calc-step__num">1</span>
          <div className="calc-step__body">
            <p className="calc-step__label">Dinos de dónde sales</p>
            <button className="btn btn--secondary" onClick={requestGeo} disabled={geoLoading}>
              {geoLoading ? 'Localizando…' : '📍 Usar mi ubicación GPS'}
            </button>
            {origin
              ? <p className="panel__coords">{origin.lat.toFixed(4)}, {origin.lng.toFixed(4)}<span className="panel__coords-hint"> · o haz clic en el mapa</span></p>
              : <p className="panel__hint">Haz clic en el mapa o usa el GPS</p>
            }
            {geoError && <p className="panel__error">{geoError}</p>}
          </div>
        </div>

        <div className="calc-step">
          <span className="calc-step__num">2</span>
          <div className="calc-step__body">
            <p className="calc-step__label">¿Cuánto tiempo te quieres desplazar? <strong>{formatMinutes(maxMinutes)}</strong></p>
            <input
              type="range" min={15} max={300} step={15}
              value={maxMinutes}
              onChange={e => setMaxMinutes(+e.target.value)}
              className="panel__slider"
            />
            <div className="panel__slider-labels"><span>15 min</span><span>5h</span></div>
          </div>
        </div>

        <div className="calc-step calc-step--action">
          <span className="calc-step__num">3</span>
          <div className="calc-step__body">
            <button className="btn btn--primary btn--full" onClick={onCalculate} disabled={!origin || loading}>
              {loading ? 'Calculando…' : 'Calcular'}
            </button>
          </div>
        </div>

        {error && <p className="panel__error panel__error--pad">{error}</p>}

        <ResultsList results={results} onSiteClick={onSiteClick} />

      </div>

      <ShareButton origin={origin} maxMinutes={maxMinutes} topSite={results?.top?.[0]} />

      <div className="panel__layers">
        <p className="panel__layers-title">Capas del mapa</p>
        <label className="panel__checkbox">
          <input type="checkbox" checked={showBand} onChange={e => setShowBand(e.target.checked)} />
          Banda de totalidad
        </label>
        <label className="panel__checkbox">
          <input type="checkbox" checked={showSites} onChange={e => setShowSites(e.target.checked)} />
          Sitios oficiales de observación&nbsp;
          <a href={ELPAIS_URL} target="_blank" rel="noopener noreferrer" className="panel__link">(fuente: El País ↗)</a>
        </label>
      </div>

    </div>
  )
}
