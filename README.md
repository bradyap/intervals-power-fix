# Intervals.icu Power File Modification Tool

Intervals.icu only recognizes specific field names in `.FIT` files for power and cadence data. If your device records these values under non-standard field names, Intervals.icu may not process them correctly.

This tool accepts an activity URL, downloads the associated `.FIT` file, updates unsupported power and cadence field names to compatible ones, and then re-uploads the corrected activity to your Intervals.icu account. The fields that are edited are defined at the top of `__main__.py` as `FIND_REPLACE`.  

## API Key

You can find your Intervals.icu API key in **Settings** under **Developer Settings**. Select **View** next to **API Key**.