
from fastapi import FastAPI
import requests
import json
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

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


def det(id:int):
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
          popularity
          type
        }
      }
    }
    characters {
      edges {
        id
        role
        name
        voiceActors {
          languageV2
          id
          name {
            first
            full
            last
            native
            userPreferred
          }
          image {
            large
            medium
          }
        }
        node {
          image {
            large
            medium
          }
          name {
            first
            full
            last
            native
            userPreferred
          }
          gender
        }
      }
      nodes {
        id
        image {
          large
          medium
        }
        name {
          full
          first
          last
          native
          userPreferred
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
  return response.json()

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

 return det(id)



@app.get('/watch/{str}')
async def main(str: str):

#   https://api.consumet.org/meta/anilist/watch/{episodeId}
  url=f"https://api-consumet-org-two-opal.vercel.app/meta/anilist/watch/{str}"
 
  # url=f"https://march-api1.vercel.app/meta/anilist/watch/{str}"
  r=requests.get(url,headers=headers)
  k=r.json()
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
@app.get('*')
async def main():
    return "page does not exist"


# https://proxy.ashanime.pro/https://www117.anzeat.pro/streamhls/db98de9dcd8c6a5e3fc38ffe06b647ba/ep.3.1722101690.360.m3u8
