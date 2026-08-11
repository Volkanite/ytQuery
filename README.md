## ytQuery
I use to use https://commentpicker.com/youtube-channel-id.php but after it started requiring $9.99 a month (or watch ads) to query information about videos, I decided to make my own tool. Now, don't get me wrong! I support projects when I need to. But paying $9.99 a month for something I go months without using, and for something so trivial, seems silly. So I started developing my own.

## Requirements
- Python 2.7 (will be migrated to 3.X later)
- YouTube API key (Do a Google search if you don't have one already)
- Edit ytQuey.py and set API key at var `apiKey` https://github.com/Volkanite/ytQuery/blob/9666006109f13046a3c61be5c31efcf1a380a45f/ytQuery.py#L27

## Usage
- --user <> Prints a playlist of a user
- --playlist <> Prints a playlist from a Youtube playlist
- --query <> Prints a playlist from a search query (Limited to 500 videos)
- --owner <> Prints the channel ID a video belongs to
- --channel <> Prints the uploads playlist from a channel ID

## Examples
`python ytQuery.py --owner RKWrWRFyfYo`  
`python ytQuery.py --channel UCsHzgQRjPzOz_w4HSrNLIVw`  
`python ytQuery.py --playlist UUsHzgQRjPzOz_w4HSrNLIVw`  
`python ytQuery.py --user UserName`
