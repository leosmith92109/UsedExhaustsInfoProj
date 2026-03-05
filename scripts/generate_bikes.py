#!/usr/bin/env python3
"""Generate USDM bike generation records (2000+)."""

from __future__ import annotations

import csv
import pathlib
import re
from dataclasses import dataclass
from typing import Iterable

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "data" / "raw" / "bikes.csv"


@dataclass(frozen=True)
class Generation:
    label: str
    year_start: int
    year_end: int


@dataclass(frozen=True)
class BikeModel:
    make: str
    model: str
    category: str
    generations: tuple[Generation, ...]
    notes: str = "USDM"


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def models() -> Iterable[BikeModel]:
    data: list[BikeModel] = [
        BikeModel("Honda", "CBR600RR", "Sport/Supersport", (Generation("PC37", 2003, 2006), Generation("PC40", 2007, 2012), Generation("PC40 Refresh", 2013, 2016), Generation("Current", 2021, 2026))),
        BikeModel("Honda", "CBR1000RR", "Sport/Supersport", (Generation("SC57", 2004, 2007), Generation("SC59", 2008, 2011), Generation("SC59 Refresh", 2012, 2016), Generation("SC77", 2017, 2019), Generation("SC82", 2020, 2026))),
        BikeModel("Honda", "CBR650R", "Sport/Supersport", (Generation("RH03", 2019, 2023), Generation("E-Clutch Era", 2024, 2026))),
        BikeModel("Honda", "CBR500R", "Sport/Supersport", (Generation("Launch", 2013, 2015), Generation("Midcycle", 2016, 2018), Generation("Euro5", 2019, 2021), Generation("Current", 2022, 2026))),
        BikeModel("Honda", "CBR300R", "Sport/Supersport", (Generation("Launch", 2015, 2018), Generation("ABS", 2019, 2026))),
        BikeModel("Honda", "Africa Twin CRF1000L", "Adventure/Dual-sport", (Generation("Launch", 2016, 2017), Generation("Adventure Sports", 2018, 2019))),
        BikeModel("Honda", "Africa Twin CRF1100L", "Adventure/Dual-sport", (Generation("Launch", 2020, 2023), Generation("Current", 2024, 2026))),
        BikeModel("Honda", "NX500", "Adventure/Dual-sport", (Generation("Launch", 2024, 2026))),
        BikeModel("Honda", "CB500X", "Adventure/Dual-sport", (Generation("Launch", 2013, 2018), Generation("Refresh", 2019, 2021), Generation("Final", 2022, 2023))),
        BikeModel("Honda", "CRF450R", "Dirt/Off-road", (Generation("EFI", 2009, 2012), Generation("2nd EFI", 2013, 2016), Generation("DOHC", 2017, 2020), Generation("Current", 2021, 2026))),
        BikeModel("Honda", "CRF250R", "Dirt/Off-road", (Generation("Launch", 2004, 2009), Generation("EFI", 2010, 2013), Generation("Current", 2014, 2026))),
        BikeModel("Honda", "CRF450RL", "Dirt/Off-road", (Generation("Launch", 2019, 2026))),
        BikeModel("Honda", "Rebel 500", "Cruiser/Harley-style", (Generation("Launch", 2017, 2019), Generation("Refresh", 2020, 2022), Generation("Current", 2023, 2026))),
        BikeModel("Honda", "Rebel 1100", "Cruiser/Harley-style", (Generation("Launch", 2021, 2024), Generation("SE DCT Era", 2025, 2026))),
        BikeModel("Honda", "Gold Wing", "Cruiser/Harley-style", (Generation("GL1800 Early", 2001, 2011), Generation("GL1800 Mid", 2012, 2017), Generation("Current", 2018, 2026))),
        BikeModel("Yamaha", "YZF-R1", "Sport/Supersport", (Generation("5VY", 2004, 2006), Generation("Crossplane", 2009, 2014), Generation("Current Chassis", 2015, 2019), Generation("Euro5", 2020, 2026))),
        BikeModel("Yamaha", "YZF-R6", "Sport/Supersport", (Generation("2003", 2003, 2005), Generation("2006", 2006, 2007), Generation("2008", 2008, 2016), Generation("R6 Track", 2017, 2026))),
        BikeModel("Yamaha", "YZF-R7", "Sport/Supersport", (Generation("Launch", 2022, 2026))),
        BikeModel("Yamaha", "YZF-R3", "Sport/Supersport", (Generation("Launch", 2015, 2018), Generation("Refresh", 2019, 2026))),
        BikeModel("Yamaha", "MT-10", "Sport/Supersport", (Generation("Launch", 2017, 2021), Generation("Current", 2022, 2026))),
        BikeModel("Yamaha", "MT-09", "Sport/Supersport", (Generation("Gen1", 2014, 2016), Generation("Gen2", 2017, 2020), Generation("Gen3", 2021, 2023), Generation("Current", 2024, 2026))),
        BikeModel("Yamaha", "MT-07", "Sport/Supersport", (Generation("FZ-07", 2015, 2017), Generation("MT-07", 2018, 2020), Generation("Current", 2021, 2026))),
        BikeModel("Yamaha", "Tenere 700", "Adventure/Dual-sport", (Generation("US Launch", 2021, 2023), Generation("Current", 2024, 2026))),
        BikeModel("Yamaha", "Super Tenere", "Adventure/Dual-sport", (Generation("XT1200Z", 2012, 2013), Generation("ES Era", 2014, 2020))),
        BikeModel("Yamaha", "WR250R", "Adventure/Dual-sport", (Generation("Launch", 2008, 2020))),
        BikeModel("Yamaha", "YZ450F", "Dirt/Off-road", (Generation("Steel", 2003, 2009), Generation("Aluminum", 2010, 2013), Generation("Reverse Head", 2014, 2022), Generation("Current", 2023, 2026))),
        BikeModel("Yamaha", "YZ250F", "Dirt/Off-road", (Generation("Launch", 2001, 2013), Generation("Reverse Head", 2014, 2018), Generation("Current", 2019, 2026))),
        BikeModel("Yamaha", "Bolt R-Spec", "Cruiser/Harley-style", (Generation("Launch", 2014, 2022))),
        BikeModel("Yamaha", "V Star 1300", "Cruiser/Harley-style", (Generation("Launch", 2007, 2017))),
        BikeModel("Kawasaki", "Ninja ZX-10R", "Sport/Supersport", (Generation("2004", 2004, 2005), Generation("2006", 2006, 2010), Generation("2011", 2011, 2015), Generation("2016", 2016, 2020), Generation("Current", 2021, 2026))),
        BikeModel("Kawasaki", "Ninja ZX-6R", "Sport/Supersport", (Generation("2003", 2003, 2004), Generation("636", 2005, 2006), Generation("599", 2007, 2008), Generation("2009", 2009, 2012), Generation("636 Return", 2013, 2018), Generation("Current", 2019, 2026))),
        BikeModel("Kawasaki", "Ninja 1000SX", "Sport/Supersport", (Generation("Ninja 1000", 2011, 2016), Generation("Refresh", 2017, 2019), Generation("SX", 2020, 2026))),
        BikeModel("Kawasaki", "Ninja 650", "Sport/Supersport", (Generation("ER-6f", 2006, 2011), Generation("2012", 2012, 2016), Generation("Current", 2017, 2026))),
        BikeModel("Kawasaki", "Ninja 400", "Sport/Supersport", (Generation("Launch", 2018, 2026))),
        BikeModel("Kawasaki", "Versys 650", "Adventure/Dual-sport", (Generation("Launch", 2008, 2009), Generation("2010", 2010, 2014), Generation("2015", 2015, 2021), Generation("Current", 2022, 2026))),
        BikeModel("Kawasaki", "Versys 1000", "Adventure/Dual-sport", (Generation("Launch", 2015, 2018), Generation("Current", 2019, 2026))),
        BikeModel("Kawasaki", "KLR650", "Adventure/Dual-sport", (Generation("Gen2", 2008, 2018), Generation("Gen3", 2022, 2026))),
        BikeModel("Kawasaki", "KX450", "Dirt/Off-road", (Generation("Carb", 2006, 2008), Generation("EFI", 2009, 2015), Generation("Current", 2016, 2026))),
        BikeModel("Kawasaki", "KX250", "Dirt/Off-road", (Generation("Launch", 2004, 2020), Generation("Current", 2021, 2026))),
        BikeModel("Kawasaki", "Vulcan S", "Cruiser/Harley-style", (Generation("Launch", 2015, 2026))),
        BikeModel("Kawasaki", "Vulcan 1700 Vaquero", "Cruiser/Harley-style", (Generation("Launch", 2011, 2024))),
        BikeModel("Suzuki", "GSX-R1000", "Sport/Supersport", (Generation("K1", 2001, 2002), Generation("K3", 2003, 2004), Generation("K5", 2005, 2006), Generation("K7", 2007, 2008), Generation("L0", 2009, 2016), Generation("L7", 2017, 2026))),
        BikeModel("Suzuki", "GSX-R750", "Sport/Supersport", (Generation("K1", 2000, 2003), Generation("K4", 2004, 2005), Generation("K6", 2006, 2007), Generation("K8", 2008, 2010), Generation("L1", 2011, 2026))),
        BikeModel("Suzuki", "GSX-R600", "Sport/Supersport", (Generation("K1", 2001, 2003), Generation("K4", 2004, 2005), Generation("K6", 2006, 2007), Generation("K8", 2008, 2010), Generation("L1", 2011, 2026))),
        BikeModel("Suzuki", "Hayabusa", "Sport/Supersport", (Generation("Gen1", 2000, 2007), Generation("Gen2", 2008, 2020), Generation("Gen3", 2022, 2026))),
        BikeModel("Suzuki", "GSX-8R", "Sport/Supersport", (Generation("Launch", 2024, 2026))),
        BikeModel("Suzuki", "SV650", "Sport/Supersport", (Generation("Fuel Injected", 2003, 2012), Generation("Hiatus Return", 2017, 2026))),
        BikeModel("Suzuki", "V-Strom 650", "Adventure/Dual-sport", (Generation("DL650", 2004, 2011), Generation("L2", 2012, 2016), Generation("XT Era", 2017, 2024))),
        BikeModel("Suzuki", "V-Strom 1000", "Adventure/Dual-sport", (Generation("DL1000", 2002, 2013), Generation("Return", 2014, 2019))),
        BikeModel("Suzuki", "V-Strom 1050", "Adventure/Dual-sport", (Generation("Launch", 2020, 2026))),
        BikeModel("Suzuki", "DR-Z400S", "Adventure/Dual-sport", (Generation("Launch", 2000, 2026))),
        BikeModel("Suzuki", "RM-Z450", "Dirt/Off-road", (Generation("Launch", 2008, 2017), Generation("Current", 2018, 2026))),
        BikeModel("Suzuki", "RM-Z250", "Dirt/Off-road", (Generation("Launch", 2004, 2018), Generation("Current", 2019, 2026))),
        BikeModel("Suzuki", "Boulevard M109R", "Cruiser/Harley-style", (Generation("Launch", 2006, 2026))),
        BikeModel("Suzuki", "Boulevard C50", "Cruiser/Harley-style", (Generation("Launch", 2005, 2019))),
        BikeModel("KTM", "1290 Super Duke R", "Sport/Supersport", (Generation("Launch", 2014, 2016), Generation("2.0", 2017, 2019), Generation("Current", 2020, 2026))),
        BikeModel("KTM", "890 Duke R", "Sport/Supersport", (Generation("Launch", 2020, 2023), Generation("Current", 2024, 2026))),
        BikeModel("KTM", "390 Duke", "Sport/Supersport", (Generation("Launch", 2015, 2016), Generation("2017", 2017, 2023), Generation("Current", 2024, 2026))),
        BikeModel("KTM", "RC 390", "Sport/Supersport", (Generation("Launch", 2015, 2019), Generation("Current", 2022, 2026))),
        BikeModel("KTM", "790 Adventure", "Adventure/Dual-sport", (Generation("Launch", 2019, 2020))),
        BikeModel("KTM", "890 Adventure", "Adventure/Dual-sport", (Generation("Launch", 2021, 2023), Generation("Current", 2024, 2026))),
        BikeModel("KTM", "1290 Super Adventure", "Adventure/Dual-sport", (Generation("T", 2015, 2020), Generation("Current", 2021, 2026))),
        BikeModel("KTM", "690 Enduro R", "Adventure/Dual-sport", (Generation("EFI", 2009, 2011), Generation("Updated", 2012, 2018), Generation("Current", 2019, 2026))),
        BikeModel("KTM", "450 SX-F", "Dirt/Off-road", (Generation("RFS", 2000, 2006), Generation("XC4", 2007, 2012), Generation("Current", 2013, 2026))),
        BikeModel("KTM", "250 SX-F", "Dirt/Off-road", (Generation("Launch", 2006, 2012), Generation("Current", 2013, 2026))),
        BikeModel("KTM", "500 EXC-F", "Dirt/Off-road", (Generation("Launch", 2012, 2016), Generation("Current", 2017, 2026))),
        BikeModel("KTM", "350 EXC-F", "Dirt/Off-road", (Generation("Launch", 2012, 2016), Generation("Current", 2017, 2026))),
        BikeModel("KTM", "1290 Super Adventure S", "Adventure/Dual-sport", (Generation("Launch", 2017, 2020), Generation("Current", 2021, 2026))),
        BikeModel("BMW", "S1000RR", "Sport/Supersport", (Generation("K46", 2010, 2014), Generation("K46 Refresh", 2015, 2018), Generation("K67", 2019, 2022), Generation("Current", 2023, 2026))),
        BikeModel("BMW", "M1000RR", "Sport/Supersport", (Generation("Launch", 2021, 2022), Generation("Current", 2023, 2026))),
        BikeModel("BMW", "R1250GS", "Adventure/Dual-sport", (Generation("Launch", 2019, 2023), Generation("Current", 2024, 2026))),
        BikeModel("BMW", "R1200GS", "Adventure/Dual-sport", (Generation("Hexhead", 2004, 2009), Generation("Camhead", 2010, 2012), Generation("LC", 2013, 2018))),
        BikeModel("BMW", "F850GS", "Adventure/Dual-sport", (Generation("Launch", 2019, 2023), Generation("Current", 2024, 2026))),
        BikeModel("BMW", "F900GS", "Adventure/Dual-sport", (Generation("Launch", 2024, 2026))),
        BikeModel("BMW", "F800GS", "Adventure/Dual-sport", (Generation("Launch", 2009, 2012), Generation("Refresh", 2013, 2018), Generation("Adventure Final", 2019, 2023))),
        BikeModel("BMW", "G310GS", "Adventure/Dual-sport", (Generation("Launch", 2018, 2026))),
        BikeModel("BMW", "R nineT", "Sport/Supersport", (Generation("Launch", 2014, 2020), Generation("Current", 2021, 2026))),
        BikeModel("BMW", "R18", "Cruiser/Harley-style", (Generation("Launch", 2021, 2026))),
        BikeModel("Ducati", "Panigale V4", "Sport/Supersport", (Generation("Launch", 2018, 2021), Generation("Current", 2022, 2026))),
        BikeModel("Ducati", "Panigale 1299", "Sport/Supersport", (Generation("Launch", 2015, 2017))),
        BikeModel("Ducati", "Panigale 1199", "Sport/Supersport", (Generation("Launch", 2012, 2014))),
        BikeModel("Ducati", "Streetfighter V4", "Sport/Supersport", (Generation("Launch", 2020, 2022), Generation("Current", 2023, 2026))),
        BikeModel("Ducati", "Monster 1200", "Sport/Supersport", (Generation("Launch", 2014, 2021))),
        BikeModel("Ducati", "Monster", "Sport/Supersport", (Generation("937", 2022, 2026))),
        BikeModel("Ducati", "SuperSport 950", "Sport/Supersport", (Generation("Launch", 2017, 2020), Generation("Current", 2021, 2026))),
        BikeModel("Ducati", "Multistrada 1200", "Adventure/Dual-sport", (Generation("Launch", 2010, 2014), Generation("DVT", 2015, 2017))),
        BikeModel("Ducati", "Multistrada 1260", "Adventure/Dual-sport", (Generation("Launch", 2018, 2020))),
        BikeModel("Ducati", "Multistrada V4", "Adventure/Dual-sport", (Generation("Launch", 2021, 2023), Generation("Current", 2024, 2026))),
        BikeModel("Ducati", "DesertX", "Adventure/Dual-sport", (Generation("Launch", 2022, 2026))),
        BikeModel("Ducati", "Hypermotard 950", "Sport/Supersport", (Generation("Launch", 2019, 2026))),
        BikeModel("Ducati", "Scrambler Icon", "Cruiser/Harley-style", (Generation("800", 2015, 2022), Generation("Current", 2023, 2026))),
        BikeModel("Ducati", "Diavel 1260", "Cruiser/Harley-style", (Generation("Launch", 2019, 2022))),
        BikeModel("Ducati", "Diavel V4", "Cruiser/Harley-style", (Generation("Launch", 2023, 2026))),
        BikeModel("Triumph", "Daytona 675", "Sport/Supersport", (Generation("Launch", 2006, 2012), Generation("R", 2013, 2017))),
        BikeModel("Triumph", "Street Triple 675", "Sport/Supersport", (Generation("Launch", 2008, 2012), Generation("Current 675", 2013, 2016))),
        BikeModel("Triumph", "Street Triple 765", "Sport/Supersport", (Generation("Launch", 2017, 2022), Generation("Current", 2023, 2026))),
        BikeModel("Triumph", "Speed Triple 1050", "Sport/Supersport", (Generation("Launch", 2005, 2015), Generation("R/S", 2016, 2020))),
        BikeModel("Triumph", "Speed Triple 1200 RS", "Sport/Supersport", (Generation("Launch", 2021, 2026))),
        BikeModel("Triumph", "Tiger 800", "Adventure/Dual-sport", (Generation("Launch", 2011, 2014), Generation("XRx Era", 2015, 2017), Generation("Final", 2018, 2020))),
        BikeModel("Triumph", "Tiger 900", "Adventure/Dual-sport", (Generation("Launch", 2020, 2023), Generation("Current", 2024, 2026))),
        BikeModel("Triumph", "Tiger 1200", "Adventure/Dual-sport", (Generation("Explorer", 2012, 2021), Generation("Current", 2022, 2026))),
        BikeModel("Triumph", "Scrambler 1200", "Adventure/Dual-sport", (Generation("Launch", 2019, 2026))),
        BikeModel("Triumph", "Trident 660", "Sport/Supersport", (Generation("Launch", 2021, 2026))),
        BikeModel("Triumph", "Bonneville T120", "Cruiser/Harley-style", (Generation("Current", 2016, 2026))),
        BikeModel("Triumph", "Rocket 3", "Cruiser/Harley-style", (Generation("Classic", 2004, 2017), Generation("Current", 2020, 2026))),
        BikeModel("Triumph", "Speed Twin 1200", "Cruiser/Harley-style", (Generation("Launch", 2019, 2026))),
        BikeModel("Harley-Davidson", "Sportster 883", "Cruiser/Harley-style", (Generation("Rubber Mount", 2004, 2020))),
        BikeModel("Harley-Davidson", "Sportster 1200", "Cruiser/Harley-style", (Generation("Rubber Mount", 2004, 2021))),
        BikeModel("Harley-Davidson", "Sportster S", "Cruiser/Harley-style", (Generation("Launch", 2021, 2026))),
        BikeModel("Harley-Davidson", "Nightster", "Cruiser/Harley-style", (Generation("Launch", 2022, 2026))),
        BikeModel("Harley-Davidson", "Pan America 1250", "Adventure/Dual-sport", (Generation("Launch", 2021, 2026))),
        BikeModel("Harley-Davidson", "Street Glide", "Cruiser/Harley-style", (Generation("Twin Cam", 2006, 2016), Generation("Milwaukee-Eight", 2017, 2023), Generation("Current", 2024, 2026))),
        BikeModel("Harley-Davidson", "Road Glide", "Cruiser/Harley-style", (Generation("Twin Cam", 2000, 2016), Generation("Milwaukee-Eight", 2017, 2023), Generation("Current", 2024, 2026))),
        BikeModel("Harley-Davidson", "Low Rider S", "Cruiser/Harley-style", (Generation("Dyna", 2016, 2017), Generation("Softail", 2020, 2026))),
        BikeModel("Harley-Davidson", "Fat Bob", "Cruiser/Harley-style", (Generation("Dyna", 2008, 2017), Generation("Softail", 2018, 2026))),
        BikeModel("Harley-Davidson", "Breakout", "Cruiser/Harley-style", (Generation("Twin Cam", 2013, 2017), Generation("Softail", 2018, 2026))),
        BikeModel("Harley-Davidson", "Heritage Classic", "Cruiser/Harley-style", (Generation("Twin Cam", 2000, 2017), Generation("Softail", 2018, 2026))),
        BikeModel("Indian", "Scout", "Cruiser/Harley-style", (Generation("Launch", 2015, 2024), Generation("Current", 2025, 2026))),
        BikeModel("Indian", "Scout Bobber", "Cruiser/Harley-style", (Generation("Launch", 2018, 2024), Generation("Current", 2025, 2026))),
        BikeModel("Indian", "Chief", "Cruiser/Harley-style", (Generation("Thunder Stroke", 2014, 2021), Generation("Current", 2022, 2026))),
        BikeModel("Indian", "Chieftain", "Cruiser/Harley-style", (Generation("Launch", 2014, 2018), Generation("Current", 2019, 2026))),
        BikeModel("Indian", "Roadmaster", "Cruiser/Harley-style", (Generation("Launch", 2015, 2018), Generation("Current", 2019, 2026))),
        BikeModel("Indian", "Challenger", "Cruiser/Harley-style", (Generation("Launch", 2020, 2026))),
        BikeModel("Indian", "Springfield", "Cruiser/Harley-style", (Generation("Launch", 2016, 2026))),
        BikeModel("Indian", "FTR", "Sport/Supersport", (Generation("Launch", 2019, 2021), Generation("Current", 2022, 2026))),
        BikeModel("Husqvarna", "FE 350", "Dirt/Off-road", (Generation("Launch", 2014, 2019), Generation("Current", 2020, 2026))),
        BikeModel("Husqvarna", "FE 501", "Dirt/Off-road", (Generation("Launch", 2014, 2019), Generation("Current", 2020, 2026))),
        BikeModel("Husqvarna", "FC 450", "Dirt/Off-road", (Generation("Launch", 2014, 2018), Generation("Current", 2019, 2026))),
        BikeModel("Husqvarna", "FC 250", "Dirt/Off-road", (Generation("Launch", 2014, 2018), Generation("Current", 2019, 2026))),
        BikeModel("Husqvarna", "TE 300i", "Dirt/Off-road", (Generation("Launch", 2018, 2023), Generation("Current", 2024, 2026))),
        BikeModel("Husqvarna", "Norden 901", "Adventure/Dual-sport", (Generation("Launch", 2022, 2026))),
        BikeModel("Husqvarna", "Svartpilen 401", "Sport/Supersport", (Generation("Launch", 2018, 2023), Generation("Current", 2024, 2026))),
        BikeModel("Husqvarna", "Vitpilen 401", "Sport/Supersport", (Generation("Launch", 2018, 2023), Generation("Current", 2024, 2026))),
        BikeModel("GasGas", "MC 450F", "Dirt/Off-road", (Generation("Launch", 2021, 2026))),
        BikeModel("GasGas", "MC 250F", "Dirt/Off-road", (Generation("Launch", 2021, 2026))),
        BikeModel("GasGas", "EX 450F", "Dirt/Off-road", (Generation("Launch", 2021, 2026))),
        BikeModel("GasGas", "EX 350F", "Dirt/Off-road", (Generation("Launch", 2021, 2026))),
        BikeModel("GasGas", "EC 300", "Dirt/Off-road", (Generation("Launch", 2021, 2026))),
        BikeModel("Aprilia", "RSV4", "Sport/Supersport", (Generation("Launch", 2010, 2014), Generation("RF/RR", 2015, 2020), Generation("Current", 2021, 2026))),
        BikeModel("Aprilia", "Tuono V4", "Sport/Supersport", (Generation("Launch", 2012, 2016), Generation("1100", 2017, 2020), Generation("Current", 2021, 2026))),
        BikeModel("Aprilia", "RS 660", "Sport/Supersport", (Generation("Launch", 2021, 2023), Generation("Current", 2024, 2026))),
        BikeModel("Aprilia", "Tuono 660", "Sport/Supersport", (Generation("Launch", 2021, 2023), Generation("Current", 2024, 2026))),
        BikeModel("Aprilia", "Tuareg 660", "Adventure/Dual-sport", (Generation("Launch", 2022, 2026))),
        BikeModel("Aprilia", "Dorsoduro 900", "Sport/Supersport", (Generation("Launch", 2018, 2020))),
        BikeModel("Aprilia", "Shiver 900", "Sport/Supersport", (Generation("Launch", 2018, 2020))),
        BikeModel("Moto Guzzi", "V7", "Cruiser/Harley-style", (Generation("Classic", 2009, 2016), Generation("III", 2017, 2020), Generation("850", 2021, 2026))),
        BikeModel("Moto Guzzi", "V9 Bobber", "Cruiser/Harley-style", (Generation("Launch", 2017, 2020), Generation("Current", 2021, 2026))),
        BikeModel("Moto Guzzi", "V85 TT", "Adventure/Dual-sport", (Generation("Launch", 2020, 2023), Generation("Current", 2024, 2026))),
        BikeModel("Moto Guzzi", "Stelvio", "Adventure/Dual-sport", (Generation("1200", 2009, 2017), Generation("1042", 2024, 2026))),
        BikeModel("Moto Guzzi", "California 1400", "Cruiser/Harley-style", (Generation("Launch", 2013, 2020))),
        BikeModel("Moto Guzzi", "MGX-21", "Cruiser/Harley-style", (Generation("Launch", 2017, 2020))),
    ]
    return data


def main() -> None:
    rows: list[dict[str, str | int]] = []
    for item in models():
        generations = item.generations if isinstance(item.generations, tuple) else (item.generations,)
        for gen in generations:
            start = max(gen.year_start, 2000)
            end = gen.year_end
            if end < 2000:
                continue
            bike_id = slugify(f"{item.make}-{item.model}-{gen.label}-{start}-{end}")
            rows.append(
                {
                    "bike_id": bike_id,
                    "make": item.make,
                    "model": item.model,
                    "generation": gen.label,
                    "year_start": start,
                    "year_end": end,
                    "bike_category": item.category,
                    "us_market": "yes",
                    "notes": item.notes,
                }
            )

    rows.sort(key=lambda r: (str(r["make"]), str(r["model"]), int(r["year_start"]), int(r["year_end"])))
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "bike_id",
                "make",
                "model",
                "generation",
                "year_start",
                "year_end",
                "bike_category",
                "us_market",
                "notes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} bikes to {OUT_PATH}")


if __name__ == "__main__":
    main()
