# Backend for OutdoorFusion

Gebruik van de onion architectuure: 
> Why????
- Rest api
    - Communicates with the dashboard
    - Should act like a CMS  (Content Management System) for the dashboard.
    - Upload data is possible via csv.
    - Trigger a scraper run.
    - Can send plots inherited from the machine learning pipeline to diagnose and debug.
- 	External Connections.
    - Can receive data from an external server and parse the data from analyzing.
- 	Scrapers
    - Scrape 3 websites and store data in Redis or Db
    - Should trigger the data cleaning pipeline.
- 	Data Cleaning 
    - Should be automatic. 
    - schema should be allowed to be edited by the user via the dashboard.
- 	Machine leaning
    - Should be automatic and scheduled.
    - Creates predictions correctly from the data provided.
    - Can create internal plots.
- 	Frontend
    - Non-responsive
    - Interactief, live dashboard
    - Moet alle relevante data laten zien
    - Dashboard in webomgeving

