def get_channel_stats(youtube, channel_ids): 
    """
    Get Channel stats
    
    Params:
    ----
    youtube: build object of Youtube API
    channel_ids: list of channel IDs
    
    Returns: 
    ----
    dataframe with all channel stats 
    
    """
    all_data = []
    
    request = youtube.channels().list(
    part="snippet,contentDetails,statistics",
    id=','.join(channel_ids)
    )
    response = request.execute()
    
    #loop through items 
    for item in response['items']:
        data = { 'channelName': item['snippet']['title'],
                 'subscribers': item['statistics']['subscriberCount'],
                 'views': item['statistics']['viewCount'],
                 'totalVideos': item['statistics']['videoCount'],
                 'playlistId': item['contentDetails']['relatedPlaylists']['uploads']
        }
        all_data.append(data)
    
    return(pd.DataFrame(all_data)) 


def get_video_ids(youtube, plalist_ids):
    """
    Get Video IDs
    
    Params:
    ----
    youtube: build object of Youtube API
    plalist_ids: list of playlist IDs
    
    Returns: 
    ----
    list of video IDs 
    
    """
    
    video_ids = []
    
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_ids,
        maxResults = 50
    )
    response = request.execute()
    
    for items in response['items']:
        video_ids.append(items['contentDetails']['videoId'])
        
    next_page_token = response.get('nextPageToken')
    while next_page_token is not None:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_ids,
            maxResults = 50,
            pageToken = next_page_token
        )
        response = request.execute()
        
        for items in response['items']:
            video_ids.append(items['contentDetails']['videoId'])
            
        next_page_token = response.get('nextPageToken')
    
    return video_ids


def get_video_info(youtube, video_ids):
    """
    Get Video info
    
    Params:
    ----
    youtube: build object of Youtube API
    video_ids: list of video IDs
    
    Returns: 
    ----
    dataframe with all the stats kept
    
    """
    
    all_video_info = []
    
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails, statistics",
            id=','.join(video_ids[i:i+50])
       #     id = ','.join(video_ids[0:5])
        )
        response = request.execute()

        for video in response['items']:
            stats_to_keep = {'snippet':['channelTitle', 'title', 'description', 'tags', 'publishedAt'], 
                             'statistics': ['viewCount', 'likeCount', 'favoriteCount', 'commentCount'],
                             'contentDetails': ['duration', 'definition', 'caption']
                            }
            video_info = {}
            video_info['video_id'] = video['id']

            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None 

            all_video_info.append(video_info)

    return (pd.DataFrame(all_video_info))