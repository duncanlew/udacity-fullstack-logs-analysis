#!/usr/bin/env python3
import sys

import psycopg2

most_popular_articles_query = '''
        select
            title,
            count(*) as views from articles,
            log
        where
            log.path like concat('%', articles.slug , '%') and
            log.status = '200 OK'
        group by title
        order by views desc
        limit 3;'''

most_popular_article_author_query = '''
        select
            authors.name,
            count(*) as views
        from
            articles,
            authors,
            log
        where
            articles.author = authors.id and
            log.path like concat('%', articles.slug , '%') and
            log.status = '200 OK'
        group by authors.name
        order by views desc;'''

error_stat_query = '''
    select
        datum,
        percent
    from
        (select
            datum,
            error_requests,
            total_requests,
            round(error_requests * 100.0 / total_requests, 1) as percent
        from
            stats_per_day)
        as stats_per_day
        where percent > 1.0;'''

if __name__ == '__main__':
    try:
        db = psycopg2.connect(database='news')
    except psycopg2.Error as e:
        print("Unable to connect to the database")
        print(e.pgerror)
        print(e.diag.message_detail)
        sys.exit(1)

    cursor = db.cursor()

    print("What are the most popular three articles of all time?")
    cursor.execute(most_popular_articles_query)
    articles = cursor.fetchall()
    for article in articles:
        print("{0} -- {1} views".format(article[0], article[1]))

    print("\nWho are the most popular article authors of all time?")
    cursor.execute(most_popular_article_author_query)
    authors = cursor.fetchall()
    for author in authors:
        print("{0} -- {1} views".format(author[0], author[1]))

    print("\nOn which days did more than 1% of requests lead to errors?")
    cursor.execute(error_stat_query)
    error_stats = cursor.fetchall()
    for error_stat in error_stats:
        print("{0} -- {1} % errors".format(error_stat[0], error_stat[1]))

    db.close()
