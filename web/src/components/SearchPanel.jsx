import ShareButton from './ShareButton'
import ResultsList from './ResultsList'

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
      </div>

      <div className="panel__section">
        <label className="panel__label">Tu posición de salida</label>
        <button
          className="btn btn--secondary"
          onClick={requestGeo}
          disabled={geoLoading}
        >
          {geoLoading ? 'Localizando…' : '📍 Usar mi ubicación GPS'}
        </button>
        {origin && (
          <p className="panel__coords">
            {origin.lat.toFixed(4)}, {origin.lng.toFixed(4)}
            <span className="panel__coords-hint"> · o haz clic en el mapa</span>
          </p>
        )}
        {!origin && (
          <p className="panel__hint">Haz clic en el mapa o usa el GPS</p>
        )}
        {geoError && <p className="panel__error">{geoError}</p>}
      </div>

      <div className="panel__section">
        <label className="panel__label">
          Tiempo máximo de desplazamiento: <strong>{maxMinutes} min</strong>
        </label>
        <input
          type="range"
          min={30}
          max={300}
          step={10}
          value={maxMinutes}
          onChange={e => setMaxMinutes(+e.target.value)}
          className="panel__slider"
        />
        <div className="panel__slider-labels">
          <span>30 min</span><span>5h</span>
        </div>
      </div>

      <button
        className="btn btn--primary"
        onClick={onCalculate}
        disabled={!origin || loading}
      >
        {loading ? 'Calculando…' : 'Calcular mejores sitios'}
      </button>

      {error && <p className="panel__error">{error}</p>}

      <ResultsList results={results} onSiteClick={onSiteClick} />

      <ShareButton
        origin={origin}
        maxMinutes={maxMinutes}
        topSite={results?.top?.[0]}
      />

      <div className="panel__section panel__layers">
        <label className="panel__label">Capas del mapa</label>
        <label className="panel__checkbox">
          <input type="checkbox" checked={showBand} onChange={e => setShowBand(e.target.checked)} />
          Banda de totalidad
        </label>
        <label className="panel__checkbox">
          <input type="checkbox" checked={showSites} onChange={e => setShowSites(e.target.checked)} />
          Sitios de observación
        </label>
      </div>
    </div>
  )
}
