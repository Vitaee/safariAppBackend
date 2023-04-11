import aiohttp, re, logging, asyncio
from bs4 import BeautifulSoup
from asgiref.sync import sync_to_async
from safari.models import Safari

class ScraperBot:
    def __init__(self) -> None:
        "Initializing globally used variables."
        self.headers = { 'User-Agent': 'Mozilla/5.0 (Linux; Android 11; RMX2101 Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.5359.128 Mobile Safari/537.36 Line/12.21.1/IAB' }
        self.base_url_home = "https://www.safaribookings.com/tours/page/"
        
        self.url_overview = "https://www.safaribookings.com/tours/t"
        self.url_day_by_day = "https://www.safaribookings.com/day/t"
        self.url_inclusions = "https://www.safaribookings.com/inclusions/t"
        self.url_getting_there = "https://www.safaribookings.com/gettingthere/t"

    async def scrape_resource_links(self):
        async with aiohttp.ClientSession() as session:
            for counter in range(1, 2):
                async with session.get(f"{self.base_url_home}{counter}") as response:
                    html_content = await response.text()
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    tours = soup.find_all('li', attrs={'class': 'col-t-6'})

                    for tour in tours:
                        url = tour.find('a', class_="list__item")['href']
                        data_over_view = await self.scrape_overview_details(session, url.split('t')[-1])
                        
                        if data_over_view != 'Tour is unavailable':
                            tour_id = url.split('t')[-1]
                            tasks = [
                                self.scrape_day_by_day_details(session, tour_id),
                                self.scrape_inclusions_details(session, tour_id),
                                self.scrape_getting_there_details(session, tour_id),
                            ]
                            data_day_by_day, data_inclusions, data_getting_there = await asyncio.gather(*tasks)
                        
                            data_merged =  data_over_view | { 'day_by_day': data_day_by_day } | { 'inclusions_data': data_inclusions } | { 'getting_there_data': data_getting_there }
                            
                            await sync_to_async(Safari.objects.create)(**data_merged)

    async def scrape_overview_details(self, session, source_link_number):
        """
        this function will scrape:
        - route_data 
        - tour_features
        - activities & transportations
        - accommodation & meals
        """
        async with session.get(f"{self.url_overview}{source_link_number}") as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')

            if soup.find('span', class_='hide show-ti'):
                    logging.debug("[LOG] Tour is unavailable -- ", self.url_overview+source_link_number )
                    return "Tour is unavailable."

            data_on_db = None
            try:
                data_on_db = await sync_to_async(Safari.objects.get)(url=f"{self.url_overview}{source_link_number}")
            except Safari.DoesNotExist:
                pass

            if data_on_db:
                return "Tour is unavailable"

            temp_json = { 'tour_data': {}}
            route_data = {}
            day_count = 0
            
            if soup.find('div', class_='tour__route-list-inner'):
                for i in soup.find('div',class_='tour__route-list-inner').find('table', class_='route__flow avoid-break-p').find_all('tr')[1:]:
                    try:
                        route_data[f"day_{day_count}"] = { "days": i.find_all('td')[0].text ,"days_route" : i.find_all('td')[1].text }
                    except: route_data[f"day_{day_count}"] = {"days" : "No Data!", "days_route": "No Data!" }
                    day_count += 1

            tour_features = {}
            feature_count = 0
            if soup.find('div', class_='tour__content__block tour__content__block--consider avoid-break-p'):
                for i in soup.find('div' , class_='tour__content__block tour__content__block--consider avoid-break-p').find('div',class_='row').find_all('div'):
                    if i.find('h4'):
                        tour_features[f"feature_{feature_count}"] = { "title": i.find('h4').text, "description" : i.find('p').text }
                        feature_count += 1
            

            accomodations = {}
            accomodation_count = 0
            if soup.find('div', class_='tour__content__block tour__content__block--accommodations avoid-break-p'):
                for i in soup.find('div', class_='tour__content__block tour__content__block--accommodations avoid-break-p').find('ul').find_all('li')[2:]:
                    accomodations[f"accomodation_{accomodation_count}"] = { 
                        "day" : i.find('div').text, 
                        "accommodation": { 
                            "title": i.find_all('div')[1].find('a').text.strip() if i.find_all('div')[1].find('a') else i.find_all('div')[1].text.strip().replace("\n", ""), 
                            "description":  i.find_all('div')[1].find('span', class_='hide-t txt--italic').previousSibling.text.strip() if len(i.find_all('div')[1].find('span', class_='hide-t txt--italic').previousSibling.text) > 1 else "(No accommodation)" , 
                            "image": i.find_all('div')[1].find('div').find('a').find('img')['src'] if i.find_all('div')[1].find('div') else i.find_all('div')[1].text
                        }, 
                        "meals": i.find_all('div')[-1].text.strip().replace("\n", " ")
                }

                accomodation_count += 1


            temp_json["tour_data"]["overview"] = { 
                "route_description": soup.find('div' , class_='tour__content__block tour__content__block--notitle').find('p').text,
                "route_data": [ route_data ],
                "tour_features": [ tour_features ],
                "activities_and_transportation": [ i.find('span').text.strip() for i in soup.find('div', class_='tour__content__block tour__content__block--activities avoid-break-p').find('ul').find_all('li') ],
                "accomodaton_and_meals": [ accomodations ]
            }

            try:
                name = soup.find('h1', class_='serif').text
                imageCover = soup.find('div', class_='imgpagehead imgpagehead--tour').find('source')['data-srcset']
            except:
                imageCover = ""
                name = ""

            temp_json["imageCover"] = imageCover
            temp_json["name"] = name
            temp_json["url"] = f"{self.url_overview}{source_link_number}"

            try:
                price_text = soup.find('div', class_='conversionblock__intro__header').find('p').text
                price_text = price_text.replace(',', '')
                if price_text.find("to") != -1:
                    temp_json["price"] = int(re.findall(r'\d+', price_text)[0])
                    temp_json["max_price"] = int(re.findall(r'\d+', price_text)[1])
                else:
                    temp_json["price"] = int(re.findall(r'\d+', price_text)[0])
                    temp_json["max_price"] = 0
            except:
                temp_json["price"] = 0
                temp_json["max_price"] = 0
        
            try:
                temp_json["ratingsQuantity"] = int(soup.find('span',class_='review-score review-score--white').text.split("(")[1][:-1].split(" ")[0])
            except:
                temp_json['ratingsQuantity'] = 0

            try:
                temp_json["ratingsAverage"] = float(soup.find('span',class_='review-score review-score--white').text.split(" ")[0].strip().split("/")[0].replace("(", "").strip())
            except:
                temp_json["ratingsAverage"] = 0.0
            
            return temp_json

    async def scrape_day_by_day_details(self, session, source_link_number):
        async with session.get(f"{self.url_day_by_day}{source_link_number}", ssl=False) as response:
            body = await response.text()
            soup = BeautifulSoup(body, 'html.parser')
            days = soup.find('div', class_='tour__content__block tour__content__block--daybyday').find_all('div', class_='day')[1:]
            day_by_day = {}

            for index, day_item in enumerate(days):
                
                if index == 6:
                    break

                day_by_day[f"day_{index+1}"] = {
                    "destination" : day_item.find('div',class_='caption').find('h2').text,
                    "image" : day_item.find('picture').find('img')["data-src"] if day_item.find('picture') else "",
                    "description": day_item.find('p', class_='shorten-m').text.strip()
                }
            
            return [ day_by_day ] 

    async def scrape_inclusions_details(self, session,source_link_number):
        temp_json = {}
        async with session.get(f"{self.url_inclusions}{source_link_number} ", ssl=False) as response:
            body = await response.text()
            soup = BeautifulSoup(body, 'html.parser')
            try:
                temp_json["inclusions"] = { 
                    "included": [i.text for i in soup.find_all('div', class_='tour__content__block tour__content__block--inclusions')[0].find('ul').find_all('li')], 
                    "excluded": [i.text for i in soup.find_all('div', class_='tour__content__block tour__content__block--inclusions')[1].find('ul').find_all('li')]
                }
            except:
                temp_json['inclusions'] = {"included": "No Data!", "excluded": "No Data!"}
        return temp_json

    async def scrape_getting_there_details(self, session, source_link_number):
        temp_json = {}
        async with session.get(f"{self.url_getting_there}{source_link_number}", ssl=False) as response:
            body = await response.text()
            soup = BeautifulSoup(body, 'html.parser')
            try:
                temp_json["getting_there"] = [ i.find('span').text.strip() for i in soup.find('div', {"id" : 'gettingthere-tab' }).find('ul').find_all('li') ] 
            except:
                temp_json['getting_there'] = "No getting there data"

        return temp_json['getting_there']

scraper_instance = ScraperBot()