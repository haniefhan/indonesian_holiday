import web
import datetime

render = web.template.render("templates/")
urls = ("/", "index", "/api/(.*)", "api")

year_from = 2013
year_limit = datetime.datetime.now().year + 4


def parseToJson(datas):
    import json

    return json.dumps(datas)


class index:
    def GET(self):
        return web.template.render("templates/").index(
            link=web.ctx.homedomain,
            year_now=datetime.datetime.now().year,
            year_from=year_from,
            year_limit=year_limit,
        )


class api:
    def GET(self, year):
        if len(year) == 4 and (
            int(year) >= year_from and int(year) <= year_limit
                ):
            import requests
            from bs4 import BeautifulSoup

            url = "https://www.liburnasional.com/kalender-" + year + "/"
            page = requests.get(url)

            soup = BeautifulSoup(page.content, "html.parser")

            holidays = soup.select(
                "table.libnas-kalender-table \
                span.libnas-holiday-calendar-detail \
                div.libnas-calendar-holiday-title"
            )

            datas = []

            for holiday in holidays:
                n = holiday.find("a", attrs={"itemprop": "url"})
                d = holiday.find("time", attrs={"itemprop": "startDate"})

                name = n.get_text()
                date = d.get("datetime")

                # parse the date
                # source: 2020-1-7
                # expected: 2020-01-07

                dt = list(map(int, date.split("-")))
                # split data, then change to integer
                date = datetime.datetime(dt[0], dt[1], dt[2]).strftime(
                    "%Y-%m-%d"
                )
                # end parse date

                data = {"name": name, "date": date}
                datas.append(data)

            web.header('Content-Type', 'application/json')
            return parseToJson(datas)
        elif len(year) == 4 and (
            int(year) < year_from or int(year) > year_limit
                ):
            return "Hanya tersedia data hari libur dari tahun 2013 hingga tahun 2024"
        else:
            return "Silahkan masukan tahun yang valid (yyyy)"


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
