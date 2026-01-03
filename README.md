# 🇮🇪 Ireland Time-Based Energy Tariffs

A Home Assistant custom integration that provides **day / night / peak electricity pricing**
for **import and export**, fully compatible with the **Energy Dashboard**.

Designed for Irish electricity tariffs, but configurable for any provider.

---

## ✨ Features

- ✅ Day / Night / Peak pricing
- ✅ Separate import & export rates
- ✅ Fully Energy Dashboard compatible
- ✅ UI-based configuration (no YAML)
- ✅ HACS installable
- ✅ Works with smart meters & batteries

---

## ⚙️ Configuration

After installing via HACS:

1. Go to **Settings → Devices & Services**
2. Click **Add Integration**
3. Search for **Ireland Time-Based Energy Tariffs**
4. Enter your tariff details:
   - Import: Night / Day / Peak rates
   - Export: Night / Day / Peak rates
   - Time windows

---

## 🔌 Energy Dashboard Setup

Use the generated sensors:

- **Import cost sensor**
  - `sensor.ireland_energy_import_rate`
- **Export value sensor**
  - `sensor.ireland_energy_export_rate`

Go to:
Settings → Energy → Electricity Grid

Select the sensors above.

---

## 🇮🇪 Default Tariff Assumptions

| Period | Typical Time |
|------|-------------|
| Night | 23:00 – 08:00 |
| Day | 08:00 – 17:00 |
| Peak | 17:00 – 19:00 |

All times and prices are fully configurable.

---

## 📦 Installation (HACS)

1. HACS → Integrations
2. Add custom repository:
3. Install
4. Restart Home Assistant

---

## 🛣️ Roadmap

- ⏭️ Weekday / weekend tariffs
- ⏭️ Supplier presets (Electric Ireland, Bord Gáis, Energia)
- ⏭️ Multiple peak windows
- ⏭️ Seasonal tariffs

---

## 🧑‍💻 Author

Created by **Diaz Xavier, based in Sligo, Ireland who owns a small digital marketing company called Sevenoways Innovations**  
Community-driven, open-source 🇮🇪
