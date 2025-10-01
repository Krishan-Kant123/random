
 
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import Response
import requests
import json
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import difflib
from difflib import SequenceMatcher
from fastapi.responses import StreamingResponse
from io import BytesIO
from urllib.parse import urljoin, urlparse

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]

app = FastAPI(middleware=middleware)

headers = {
    'authority': 'march-api1.vercel.app',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.5',
    'origin': 'https://www.ashanime.pro',
    'referer': 'https://www.ashanime.pro/',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36',
}

url = 'https://graphql.anilist.co'

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def best_match(query, choices):
    query_lower = query.lower()
    
    # Prioritize exact word matches first
    exact_matches = [i for i, title in enumerate(choices) if query_lower in title.lower()]
    
    if exact_matches:
        return exact_matches[0]  # Return first exact match
    
    # If no exact matches, use similarity score
    return max(range(len(choices)), key=lambda i: similarity(query, choices[i]))

def ep(title:str,dub:str):
  print(title)
  # u=f'https://dev-amvstrm-api.nyt92.eu.org/api/v1/episode/{title}'
  
  u=f'https://stream-pied-five.vercel.app/anime/zoro/{title}'
  r=requests.get(u)
 
  k=r.json()
  possible=k.get("results",[])
  # print(possible)
  candi=[]
  for each in possible:
    candi.append(each.get("title"))
  # print(candi)
  # return k
  closest_index = best_match(title, candi)
  closest_match = candi[closest_index]


  # closest_matches = difflib.get_close_matches(title, candi, n=1, cutoff=0.5)
  # closest_match = closest_matches[0]
  # index = candi.index(closest_match) 
  print(closest_index)
  # return k



  id = k.get("results", [{}])[closest_index].get("id")
  print(id)
  for_episodes=f'https://stream-pied-five.vercel.app/anime/zoro/info?id={id}'
  epi=requests.get(for_episodes)
#   print(epi)
  epi=epi.json()
#   print(epi)
  epi= epi.get("episodes", [])
#   print(epi)
  list=[]
  for every in epi:
    print(every['isSubbed'])
    if(dub=='false'):
      if(every['isSubbed']==True):
        list.append(every)
    else:
      if(every['isDubbed']==True):
        list.append(every)
#   print(list)
  return list




  


def f(st:str,pg:int,ct:int=20):
  query = '''
  query ( $sort: [MediaSort], $page: Int, $perPage: Int) { # Define which variables will be used in the query (id)
 
  Page(page: $page, perPage: $perPage) {
    pageInfo {
      currentPage
      hasNextPage
      total
      lastPage
      }
      media (sort: $sort,type:ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
    id
    title {
      romaji
      english
      native
    }
    idMal
    synonyms
    isLicensed
    isAdult
    countryOfOrigin
    trailer {
      id
      site
      thumbnail
    }
    bannerImage
    coverImage {
      extraLarge
      large
      medium
      color
    }
    description
    status

    episodes
    meanScore
    popularity
    duration
     averageScore
    genres
  
    type
   
    
    
  
    }
  }
   }
   '''
  variables = {
   
    'page': pg,
    'perPage': ct,
    "sort": st
   }
  response = requests.post(url, json={'query': query, 'variables': variables})
  return response.json()


def det(id:int,dub:str):
  query = '''
query ($id: Int) { # Define which variables will be used in the query (id)
  Media (id: $id) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
    id
    title {
      romaji
      english
      native
    }
    idMal
    synonyms
    isLicensed
    isAdult
    countryOfOrigin
    trailer {
      id
      site
      thumbnail
    }
    bannerImage
    coverImage {
      extraLarge
      large
      medium
      color
    }
    description
    status
    startDate {
      day
      month
      year
    }
    endDate {
      day
      month
      year
    }
    episodes
    meanScore
    popularity
    duration
     averageScore
    genres
    season
    studios {
      nodes {
        name
      }
    }
    type
    recommendations {
      nodes {
        mediaRecommendation {
          id
          idMal
          title {
            english
            native
            romaji
            userPreferred
          }
          status
          episodes
          genres
          coverImage {
            color
            extraLarge
            large
            medium
          }
          bannerImage
          isAdult
          meanScore
          averageScore
          popularity
          type
        }
      }
    }
     characterPreview: characters(perPage: 6, sort: [ROLE, RELEVANCE, ID]) {
      edges {
        id
        role
        name
        voiceActors(language: JAPANESE, sort: [RELEVANCE, ID]) {
          id
          name {
            userPreferred
          }
          language: languageV2
          image {
            large
          }
        }
        node {
          id
          name {
            userPreferred
          }
          image {
            large
          }
        }
      }
    }
    relations {
      nodes {
        id
        idMal
        title {
          english
          native
          romaji
          userPreferred
        }
        genres
        status
        episodes
        bannerImage
        coverImage {
          color
          extraLarge
          large
          medium
        }
        popularity
        meanScore
        averageScore
        type
      }
    }
   
  }
}
'''

  variables = {
    'id': id
  }

  response = requests.post(url, json={'query': query, 'variables': variables})
  e= response.json()
  # u=f"https://dev-amvstrm-api.nyt92.eu.org/api/v2/info/{id}"
  # res=requests.get(u,headers=headers)
  # res=res.json()
  # provider=res["id_provider"]
  # e["id_provider"]=provider
  # name=provider["idGogo"]
  # if(dub=="false"):
  #   if(provider["idGogo"]==""):
  #     e['data']['Media']["totalepisodes"]=[]
  #     return e
  # if(dub!="false"):
  #   if(provider["idGogoDub"]==""):
  #     e['data']['Media']["totalepisodes"]=[]
  #     return e
  #   name=provider["idGogoDub"]
  
  nam= e['data']['Media']['title']['english']
  s=(ep(nam,dub))
#   print(s)
  e['data']['Media']["totalepisodes"]=s
#   print(e['data']['Media'])
  
  return e


def ser(st:str,pg:int):
  query = '''
query ($id: Int, $page: Int, $perPage: Int, $search: String) {
    Page (page: $page, perPage: $perPage) {
        pageInfo {
            currentPage
            hasNextPage
            perPage
        }
        media (id: $id, search: $search) {
                id
    title {
      romaji
      english
      native
    }
    idMal
    synonyms
    isLicensed
    isAdult
    countryOfOrigin
    trailer {
      id
      site
      thumbnail
    }
    bannerImage
    coverImage {
      extraLarge
      large
      medium
      color
    }
    description
    status

    episodes
    meanScore
    popularity
    duration
     averageScore
    genres
  
    type
   
    
        }
    }
}
'''
  variables = {
    'search': st,
    'page': pg,
    'perPage': 10
  }
  response = requests.post(url, json={'query': query, 'variables': variables})
  return response.json()


def movie(variables):
  query='''query(
  $page: Int = 1,
  $id: Int,
  $type: MediaType,
  $isAdult: Boolean = false,
  $search: String,
  $format: [MediaFormat],
  $status: MediaStatus,
  $countryOfOrigin: CountryCode,
  $source: MediaSource,
  $season: MediaSeason,
  $seasonYear: Int,
  $year: String,
  $onList: Boolean,
  $yearLesser: FuzzyDateInt,
  $yearGreater: FuzzyDateInt,
  $episodeLesser: Int,
  $episodeGreater: Int,
  $durationLesser: Int,
  $durationGreater: Int,
  $chapterLesser: Int,
  $chapterGreater: Int,
  $volumeLesser: Int,
  $volumeGreater: Int,
  $licensedBy: [Int],
  $isLicensed: Boolean,
  $genres: [String],
  $excludedGenres: [String],
  $tags: [String],
  $excludedTags: [String],
  $minimumTagRank: Int,
  $sort: [MediaSort] = [POPULARITY_DESC, SCORE_DESC]
) {
  Page(page: $page, perPage: 20) {
    pageInfo {
      total
      perPage
      currentPage
      lastPage
      hasNextPage
    }
    media(
      id: $id,
      type: $type,
      season: $season,
      format_in: $format,
      status: $status,
      countryOfOrigin: $countryOfOrigin,
      source: $source,
      search: $search,
      onList: $onList,
      seasonYear: $seasonYear,
      startDate_like: $year,
      startDate_lesser: $yearLesser,
      startDate_greater: $yearGreater,
      episodes_lesser: $episodeLesser,
      episodes_greater: $episodeGreater,
      duration_lesser: $durationLesser,
      duration_greater: $durationGreater,
      chapters_lesser: $chapterLesser,
      chapters_greater: $chapterGreater,
      volumes_lesser: $volumeLesser,
      volumes_greater: $volumeGreater,
      licensedById_in: $licensedBy,
      isLicensed: $isLicensed,
      genre_in: $genres,
      genre_not_in: $excludedGenres,
      tag_in: $tags,
      tag_not_in: $excludedTags,
      minimumTagRank: $minimumTagRank,
      sort: $sort,
      isAdult: $isAdult
    ) {
      id
      title {
       romaji
        english
        native
        userPreferred
      }
      coverImage {
        extraLarge
        large
        color
      }
      startDate {
        year
        month
        day
      }
      endDate {
        year
        month
        day
      }
      bannerImage
      season
      seasonYear
      description
      type
      format
      status(version: 2)
      episodes
      duration
      chapters
      volumes
      genres
      isAdult
      averageScore
      popularity
      nextAiringEpisode {
        airingAt
        timeUntilAiring
        episode
      }
      mediaListEntry {
        id
        status
      }
      studios(isMain: true) {
        edges {
          isMain
          node {
            id
            name
          }
        }
      }
    }
  }
}
'''
 
  response = requests.post(url, json={'query': query, 'variables': variables})
  return response.json()



@app.get("/")
async def main():
  u="https://harrynull.tech/api/wallpapers/random_anime_wallpaper?download=true"
  r=requests.get(u,headers=headers)
  k=r.json()
  return k



@app.get("/trending")
async def main(pgno:int =1):

    return f("TRENDING_DESC",pgno)

@app.get('/trending/{pgno}/{type}')
async def main(pgno:int,type:str):
  
   # https://api.consumet.org/meta/anilist/trending?page={page}&perPage={perPage}
    if(type=="MOVIE"):
      variables={"page":pgno,"type":"ANIME","format":["MOVIE"],"sort":"SCORE_DESC"}
      return movie(variables)
    else:
      variables={"page":pgno,"type":"ANIME","format":[type],"sort":"SCORE_DESC"}
    return movie(variables)



#   url =f"https://api-consumet-org-two-opal.vercel.app/meta/anilist/advanced-search?provider=gogoanime&page={pgno}&perPage=25&sort=[%22SCORE_DESC%22]&format={type}&status=FINISHED"
#   # response = requests.get('https://march-api1.vercel.app/meta/anilist/trending', params=params, headers=headers) 
#   # url=f"https://march-api1.vercel.app/meta/anilist/trending?page={pgno}&provider=gogoanime"
#   r=requests.get(url,headers=headers)
#   k=r.json()
#   return k

@app.get('/ongoing/{pgno}')
async def main(pgno:int):
  variables={"page":pgno,"type":"ANIME","status":"RELEASING","sort":"SCORE_DESC"}
  return movie(variables)


# https://api-consumet-org-two-opal.vercel.app/meta/anilist/advanced-search?provider=gogoanime&page=1&perPage=25&sort=[%22SCORE_DESC%22]&format=MOVIE&status=FINISHED


@app.get('/popular/{pgno}')
async def main(pgno:int=1):

 
   return f("POPULARITY_DESC",pgno)



@app.get('/latestep')
async def main(pgno:int =1):

 
#   url=f"https://api.consumet.org/meta/anilist/recent-episodes?page={pgno}provider=gogoanime&perPage=20"


  url=f"https://march-api1.vercel.app/meta/anilist/recent-episodes?page={pgno}&provider=gogoanime&perPage=20"
  r=requests.get(url,headers=headers)
  k=r.json()
  return k




@app.get('/detail/{id}/{dub}')
async def main(id:int,dub: str):

 return det(id,dub)




@app.get('/watch/{id}/{str}')
async def main(id:str,str: str):

#   https://api.consumet.org/meta/anilist/watch/{episodeId}
  # url=f"https://api-consumet-org-two-opal.vercel.app/meta/anilist/watch/{str}"
  # url=f"https://dev-amvstrm-api.nyt92.eu.org/api/v2/stream/{str}"
 
  # url=f"https://march-api1.vercel.app/meta/anilist/watch/{str}"
#   url=f"https://dev-amvstrm-api.nyt92.eu.org/api/v2/stream/{id}/{str}"
  # url=f'https://stream-pied-five.vercel.app/anime/zoro/watch/{id}?dub={str}'
  if(str=='false'):
    str="sub"
  elif (str=='true'):
    str='dub'
  url=f'https://yumaapi.vercel.app/watch?episodeId={id}&type={str}'
  
  r=requests.get(url,headers=headers)
  k=r.json()
  modified_subtitles = [{"src": item["url"], "label": item["lang"]} for item in k['subtitles']]
  print(k['subtitles'])
  k['subtitles']=modified_subtitles
  

  return k



@app.get('/random')
async def main():
  url=f"https://api-consumet-org-two-opal.vercel.app/meta/anilist/random-anime"
 
  r=requests.get(url,headers=headers)
  k=r.json()
  return k

@app.get('/search/{query}/{pgno}')
async def main(query:str,pgno:int):
  return ser(query,pgno)

# https://api-consumet-org-two-opal.vercel.app/meta/anilist/advanced-search?query=demon+slayer&page=1&perPage=25&type=ANIME

# @app.get("/proxy")
# async def main(p: str = Query(..., description="M3U8 master playlist URL")):
  
#   proxy_url = "https://m3u8-proxy-dnuse.amvstr.me/"

#   print(f"{proxy_url}{p}")


#   response = requests.get(f"{p}",headers=headers)
#   return response.text


@app.get("/proxy")
async def proxy_m3u8(url: str):
    """
    A FastAPI route to proxy M3U8 stream and add CORS headers.
    It converts relative URLs in M3U8 playlists and segment files to absolute URLs,
    except for `.ts` files which will be left unchanged if passed directly.
    Args:
    - url: The M3U8 stream URL (usually master.m3u8)
    """
    try:
        # Check if the provided URL ends with `.ts`
        if url.endswith(".ts"):
            # If it's a `.ts` URL, don't modify or proxy the content. Just fetch and return it.
            response = requests.get(url)
            response.raise_for_status()  # Check for errors
            return StreamingResponse(
                BytesIO(response.content), 
                media_type="video/MP2T",  # Content type for `.ts` files
                headers={
                    "Access-Control-Allow-Origin": "*",  # Allow CORS for all origins
                    "Cache-Control": "no-cache",  # Prevent caching
                }
            )
        
        # Otherwise, proxy M3U8 playlist and modify the content
        response = requests.get(url)
        response.raise_for_status()  # Check for errors
        
        # Read the content of the M3U8 file (playlist)
        m3u8_content = response.text

        # Extract the UUID from the passed URL (the path part before 'master.m3u8')
        base_url = urlparse(url)._replace(path=urlparse(url).path.rsplit('/', 2)[0]).geturl()
        uuid = urlparse(url).path.split('/')[-2]  # Extract UUID from URL path
        
        # Replace all URLs with the proxy URLs, except for `.ts` files
        updated_m3u8_content = []
        for line in m3u8_content.splitlines():
            
            if line.startswith("http") or line.startswith("https"):
                # If it's already an absolute URL, leave it as is (but route through the proxy)
                updated_line = line
            elif line.endswith(".m3u8") or line.endswith(".vtt") or line.endswith(".ts"):
                # Replace relative URLs with proxy URLs for `.m3u8` and `.vtt`
                updated_line = f"http://127.0.0.1:8000/proxy?url={urljoin(f'{base_url}/{uuid}/', line)}"
            else:
                # Just append lines that don't need transformation (e.g., comments)
                updated_line = line

            updated_m3u8_content.append(updated_line)

        # Convert updated M3U8 content back to a stream
        stream = BytesIO("\n".join(updated_m3u8_content).encode('utf-8'))

        # Return the streaming response with added CORS headers
        return StreamingResponse(
            stream,
            media_type="application/vnd.apple.mpegurl",  # Content type for M3U8
            headers={
                "Access-Control-Allow-Origin": "*",  # Allow CORS for all origins
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "GET, POST",  # Allowed methods
                "Cache-Control": "no-cache",  # Prevent caching
            }
        )

    except requests.exceptions.RequestException as e:
        # Handle potential errors (e.g., invalid URL, connection issues)
        return {"error": f"Failed to fetch the stream: {str(e)}"}


@app.get('*')
async def main():
    return "page does not exist"


# https://proxy.ashanime.pro/https://www117.anzeat.pro/streamhls/db98de9dcd8c6a5e3fc38ffe06b647ba/ep.3.1722101690.360.m3u8


