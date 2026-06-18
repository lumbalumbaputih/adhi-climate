"""
build_dataset.py: clean IBTrACS South Indian Ocean data for the WA cyclone
analysis and flag WA-affecting systems.

Inputs : data/raw/ibtracs.SI.list.v04r01.csv   (IBTrACS v04r01, SI basin)
Outputs: data/ibtracs_clean.csv   one row per storm, all SI, seasons 1985-2024
         data/ibtracs_wa.csv      subset within 500 km of the WA coast
         data/ibtracs_obs_wa.csv  per-observation track for WA storms (for RI)

Conventions
-----------
* Season: IBTrACS labels Southern-Hemisphere seasons by the calendar year in
  which Jan-Jun falls (season 1985 = Jul 1984 - Jun 1985). We keep 1985-2024
  = 40 seasons.
* Winds are in knots as stored by IBTrACS. USA_WIND is 1-min sustained;
  BOM_WIND is 10-min sustained; they are NOT interchangeable.
* Pressure is hPa (mb).
* "WA-affecting" = the storm track passes within 500 km (great-circle) of any
  reference point on the WA coast from the north Kimberley to the Mid West.
"""
import numpy as np
import pandas as pd

RAW = "data/raw/ibtracs.SI.list.v04r01.csv"

# WA coastline reference points (lat, lon), north Kimberley -> Mid West.
# Spacing < ~250 km so a 500 km proximity test has no gaps.
WA_COAST = np.array([
    (-13.7, 126.6),   # Kalumburu / north Kimberley
    (-14.9, 125.7),   # Kuri Bay
    (-16.4, 123.1),   # Cape Leveque
    (-17.96, 122.24), # Broome
    (-19.0, 121.3),   # Eighty Mile Beach
    (-20.31, 118.61), # Port Hedland
    (-20.74, 116.85), # Karratha / Dampier
    (-21.67, 115.10), # Onslow
    (-21.93, 114.13), # Exmouth (North West Cape)
    (-23.11, 113.77), # Coral Bay
    (-24.88, 113.66), # Carnarvon
    (-25.5, 113.4),   # Shark Bay (outer)
    (-27.71, 114.16), # Kalbarri
    (-28.77, 114.61), # Geraldton (Mid West)
    (-30.30, 115.04), # Jurien Bay (southern Mid West extent)
])
WA_PROXIMITY_KM = 500.0


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0088
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))


def min_dist_to_wa(lat, lon):
    """Minimum great-circle distance (km) from a point to the WA coast set."""
    d = haversine_km(lat, lon, WA_COAST[:, 0], WA_COAST[:, 1])
    return np.nanmin(d)


def load_obs():
    cols = ['SID', 'SEASON', 'BASIN', 'SUBBASIN', 'NAME', 'ISO_TIME', 'NATURE',
            'LAT', 'LON', 'WMO_WIND', 'WMO_PRES', 'USA_WIND', 'USA_PRES',
            'USA_SSHS', 'BOM_WIND', 'BOM_PRES']
    df = pd.read_csv(RAW, usecols=cols, skiprows=[1], low_memory=False,
                     na_values=[' ', '', '  ', '   '])
    df['SEASON'] = pd.to_numeric(df['SEASON'], errors='coerce')
    for c in ['LAT', 'LON', 'WMO_WIND', 'WMO_PRES', 'USA_WIND', 'USA_PRES',
              'USA_SSHS', 'BOM_WIND', 'BOM_PRES']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df['ISO_TIME'] = pd.to_datetime(df['ISO_TIME'], errors='coerce')
    df = df[(df.SEASON >= 1985) & (df.SEASON <= 2024)].copy()
    # distance to WA for every observation
    df['dist_wa_km'] = [min_dist_to_wa(la, lo) if np.isfinite(la) and np.isfinite(lo)
                        else np.nan for la, lo in zip(df.LAT, df.LON)]
    return df


def peak_row(group, wind_col):
    """Return the observation at peak intensity for a wind column, or None."""
    g = group.dropna(subset=[wind_col])
    if g.empty:
        return None
    return g.loc[g[wind_col].idxmax()]


def build():
    obs = load_obs()

    rows = []
    for sid, g in obs.groupby('SID'):
        g = g.sort_values('ISO_TIME')
        rec = {
            'sid': sid,
            'season': int(g.SEASON.iloc[0]),
            'name': str(g.NAME.iloc[0]).strip().title() if pd.notna(g.NAME.iloc[0]) else 'UNNAMED',
            'n_obs': len(g),
            'min_dist_wa_km': np.nanmin(g.dist_wa_km) if g.dist_wa_km.notna().any() else np.nan,
            # BOM 10-min wind (headline metric)
            'peak_bom_wind_kt': g.BOM_WIND.max(),
            'min_bom_pres_hpa': g.BOM_PRES.min(),
            # USA 1-min wind (most complete; defines Saffir-Simpson)
            'peak_usa_wind_kt': g.USA_WIND.max(),
            'min_usa_pres_hpa': g.USA_PRES.min(),
            'peak_usa_sshs': g.USA_SSHS.max(),
            # WMO (official agency mix)
            'peak_wmo_wind_kt': g.WMO_WIND.max(),
            'min_wmo_pres_hpa': g.WMO_PRES.min(),
        }
        # date and location of BOM-wind peak (fallback to USA peak for location)
        pr = peak_row(g, 'BOM_WIND')
        if pr is None:
            pr = peak_row(g, 'USA_WIND')
        if pr is not None:
            rec['date_peak'] = pr.ISO_TIME
            rec['lat_peak'] = pr.LAT
            rec['lon_peak'] = pr.LON
        else:
            rec['date_peak'] = g.ISO_TIME.iloc[len(g) // 2]
            rec['lat_peak'] = g.LAT.median()
            rec['lon_peak'] = g.LON.median()
        rec['wa_affecting'] = bool(rec['min_dist_wa_km'] <= WA_PROXIMITY_KM) \
            if np.isfinite(rec['min_dist_wa_km']) else False
        rows.append(rec)

    storms = pd.DataFrame(rows).sort_values(['season', 'date_peak']).reset_index(drop=True)
    storms['decade'] = pd.cut(storms.season, [1984, 1994, 2004, 2014, 2024],
                              labels=['1985-94', '1995-04', '2005-14', '2015-24'])

    storms.to_csv('data/ibtracs_clean.csv', index=False)
    wa = storms[storms.wa_affecting].copy()
    wa.to_csv('data/ibtracs_wa.csv', index=False)

    # per-observation track for WA storms (rapid-intensification step)
    wa_sids = set(wa.sid)
    obs_wa = obs[obs.SID.isin(wa_sids)].sort_values(['SID', 'ISO_TIME'])
    obs_wa.to_csv('data/ibtracs_obs_wa.csv', index=False)

    return storms, wa, obs


if __name__ == "__main__":
    storms, wa, obs = build()
    print("Storms (all SI, 1985-2024):", len(storms))
    print("WA-affecting storms:", len(wa))
    print("Wrote data/ibtracs_clean.csv, data/ibtracs_wa.csv, data/ibtracs_obs_wa.csv")
