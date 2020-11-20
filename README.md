# Django with Scrapy

1. Build the image:
   docker-compose build
2. Run the container:
   docker-compose up -d
3. Build the new image and spin up the two containers:
   docker-compose up -d --build
4. Check the Django tables were created:
   docker-compose exec db psql --username=postgres --dbname=best_movie
5. Check that the volume was created as well by running:
   docker volume inspect pgdata
6. if the container fails to start, check for errors in the logs via:
   docker-compose -f docker-compose.prod.yml logs -f.
7. run env
   .\env\Scripts\activate

